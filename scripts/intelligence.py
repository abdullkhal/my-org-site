"""Validate release records shared by the static publisher and operations."""
from datetime import date
import hashlib
import json
import re
from urllib.parse import urlsplit

SECTIONS = ("The Big Story", "Market Pulse", "Regulatory Watch",
            "Positive Developments", "Before You Commit")
# Preserve the exact launch material with its historical review limitations.
BASELINE = {
    ("article", "estate-agent-gazette"): "6e5e5315bec61537d3dd3a466fcd0efdaeed662a3e02c7508b89ad190d23bb00",
    ("article", "land-search-and-site-check"): "12c5c2e8d49413d1a64742807637b029ffa7057315f8abc0aae8bce3c15c3dc3",
    ("notice", "earb-2026-publication"): "5ccad31ff702a2b1ac1446f904603cc7f4fbaec015a0cd8a3ba0797ac0682d40",
    ("notice", "changed-payment-details"): "d6d55f9fe087835952843fc758f35984756de3e01368c5745ad1c0f2ae712c78",
    ("guide", "land-searches"): "9f8631f792300b281d7e9fa8dca5d66aa604439a3bd34fe13dd9bfffaf2438b5",
    ("guide", "agents"): "2c870411c87d682fa110038b9fdd38e82bea6e158da2e57c04665115bec6bb58",
    ("guide", "developers"): "0cec216f65864ba22af82a72282d4ab52202f01e401b7b61c2c5a270f8aa2fab",
    ("guide", "off-plan"): "eccf18202f0ce1338fc769c7359c2601ffcbde5be039379cee33003295e7bf82",
    ("guide", "fraud"): "b93ecd2508f13154c6b7be7ea56df0ca08b4798e0f77c3e731be850d9a5cecde",
    ("guide", "independent-team"): "0b3fd039aa96b299ca03c5fa7a37a323d4edd0da2c692bde0a7fd70906759393",
    ("guide", "diaspora"): "08ee2c3656f6c3ded1c73abf66e72067fa91d5d720d8b580e4730c5490a712fb",
    ("guide", "companies"): "7c0f2c0474ccabfc2e5d1a01340b94cc5af44f6744d02b8c1cb6026fd6cb52c4",
    ("guide", "rental-deposit"): "857ce54f42544955ecc044aff21f3879c1bebe6dc0f57bed29f4a2f48cb87d10",
    ("guide", "commercial-costs"): "a36b9cf9287228b6150a2603fc0e78b29fea24d403f225ba14644b3a4aa23280",
    ("guide", "construction-approvals"): "6d3cf5f53259360a2e08c6c2abb6b06aaa0cdd30e42e72a2b294988789e647c4",
    ("guide", "buying-checks"): "573446d5cf0a4afff98ff50c9ba4979dc10853ede5a0d4fb8941d6f675d6e159",
}


def require(condition, label):
    if not condition:
        raise ValueError(label)


def fields(record, names, label):
    for name in names.split():
        value = record.get(name)
        require(isinstance(value, str) and value.strip(), f"{label}: missing {name}")


def iso(value, label):
    require(isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value), f"{label}: expected ISO date")
    return date.fromisoformat(value)


def https_url(value, label):
    url = urlsplit(value or "")
    require(url.scheme == "https" and url.hostname and not url.username and
            not url.password and url.port in {None, 443}, f"{label}: expected public HTTPS URL")
    return url


def evidence(record, label, publish_date):
    review = record.get("review")
    require(isinstance(review, dict), f"{label}: missing evidence review")
    fields(review, "reviewer evidence limitations", label)
    discovered, reviewed, updated = (
        iso(review.get(key), f"{label} {key}")
        for key in ("discovered_at", "reviewed_at", "updated_at")
    )
    require(discovered <= reviewed <= publish_date <= updated <= date.today(), f"{label}: invalid review chronology")
    origins = review.get("sources")
    require(isinstance(origins, list) and origins, f"{label}: missing original sources")
    for origin in origins:
        fields(origin, "organisation url", label)
        https_url(origin["url"], label)
        require("published_at" in origin, f"{label}: source date must be recorded or null")
        if origin["published_at"] is not None:
            require(iso(origin["published_at"], label) <= reviewed, f"{label}: source date follows review")
    return origins


def approved(records, kind, date_key, *, required=""):
    result = []
    for key, record in records.items():
        label = f"{kind} {key}"
        status = record.get("status")
        require(status in {"approved", "draft", "withdrawn"}, f"{label}: unknown approval status")
        if status != "approved":
            continue
        fields(record, required, label)
        published = iso(record.get(date_key), label)
        require(published <= date.today(), f"{label}: future publication")
        if record.get("baseline_review") == "existing_publication":
            digest = hashlib.sha256(json.dumps(record, sort_keys=True).encode()).hexdigest()
            require(digest == BASELINE.get((kind, key)), f"{label}: edited baseline record needs evidence")
        elif kind != "edition":
            evidence(record, label, published)
            if kind in {"article", "notice"}:
                require("event_date" in record, f"{label}: event date must be recorded or null")
                if record["event_date"] is not None:
                    iso(record["event_date"], label)
        result.append(record)
    return sorted(result, key=lambda record: record[date_key], reverse=True)


def validate_editions(editions, articles):
    published = {article["id"]: article for article in articles}
    for edition in editions:
        label = f'edition {edition["id"]}'
        entries = edition.get("entries")
        require(isinstance(entries, list) and 1 <= len(entries) <= 5, f"{label}: requires one to five stories")
        seen = set()
        for entry in entries:
            key = entry.get("article_id")
            require(entry.get("section") in SECTIONS and key in published and key not in seen,
                    f"{label}: invalid or duplicate story")
            article = published[key]
            require(article.get("review") and article["published"] <= edition["published"],
                    f"{label}: story needs current reviewed evidence")
            seen.add(key)
        reviewed = iso(edition.get("reviewed_at"), label)
        require(all(iso(published[key]["review"]["reviewed_at"], label) <= reviewed for key in seen),
                f"{label}: edition reviewed before story evidence")
        fields(edition, "reviewer", label)
        require(edition["reviewed_at"] <= edition["published"], f"{label}: publication precedes review")


def validate_profiles(profiles, categories, authorities):
    names, websites = set(), set()
    for profile in profiles:
        label = f'profile {profile["id"]}'
        require(profile["category"] in categories, f"{label}: unknown category")
        require(profile.get("authority_id") in authorities, f"{label}: unknown registration authority")
        require(profile["checked_at"] == profile["review"]["reviewed_at"], f"{label}: last review dates disagree")
        site = https_url(profile["website"], label).hostname.lower().removeprefix("www.")
        name = " ".join(re.findall(r"\w+", profile["name"].casefold()))
        require(name and name not in names and site not in websites, f"{label}: duplicate organisation")
        names.add(name)
        websites.add(site)
        sources = {item["url"] for item in profile["review"]["sources"]}
        require(profile["source"] in sources, f"{label}: business source missing from evidence")
        if profile.get("public_contact"):
            require(profile.get("contact_source") in sources, f"{label}: contact source missing from evidence")
        if registration := profile.get("official_registration"):
            fields(registration, "scope source checked_at", label)
            require(registration["source"] in sources, f"{label}: registration source missing from evidence")
            require(iso(registration["checked_at"], label) <= iso(profile["checked_at"], label),
                    f"{label}: registration check follows profile review")


def validate_registry(records):
    require(sum(record.get("enabled") is True for record in records) <= 12,
            "source registry: at most 12 monitored sources per run")
    seen = set()
    for record in records:
        fields(record, "id owner url category reliability status method expected_frequency access_limitations", "source registry")
        key = record["id"]
        require(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", key) and key not in seen,
                f"source registry: invalid or duplicate ID {key}")
        seen.add(key)
        url = https_url(record["url"], key)
        require(not url.fragment and not url.query, f"{key}: monitor URL must be stable")
        require(record["status"] in {"pending_review", "verification_link_only", "monitoring_approved"},
                f"{key}: unknown research status")
        require(isinstance(record.get("enabled"), bool) and "last_successful_check" in record,
                f"{key}: missing access state")
        if record["last_successful_check"] is not None:
            require(iso(record["last_successful_check"], key) <= date.today(), f"{key}: future check")
        if record["enabled"]:
            require(record["status"] == "monitoring_approved" and record["last_successful_check"],
                    f"{key}: monitoring approval and successful review required")
            fields(record, "access_review path_prefix", key)
            require(record["path_prefix"].startswith("/") and not record["path_prefix"].startswith("//"),
                    f"{key}: invalid item path prefix")
            require(record["method"] in {"notice_index", "rss", "atom"}, f"{key}: unsupported monitoring method")


def publication_controls(groups, corrections):
    notes = {}
    for key, correction in corrections.items():
        label = f"correction {key}"
        fields(correction, "target_kind target_id explanation reviewer published", label)
        identity = (correction["target_kind"], correction["target_id"])
        target = groups.get(identity[0], {}).get(identity[1])
        require(target and target["status"] in {"approved", "withdrawn"}, f"{label}: unknown public target")
        published = iso(correction["published"], label)
        require(published <= date.today(), f"{label}: future correction")
        notes.setdefault(identity, []).append(correction)
    for kind, records in groups.items():
        for key, record in records.items():
            if record["status"] == "withdrawn":
                require(set(record) == {"id", "status"}, f"{kind} {key}: remove withdrawn content from the record")
                require((kind, key) in notes, f"{kind} {key}: withdrawal requires a public explanation")
    return {key: sorted(records, key=lambda item: item["published"], reverse=True)
            for key, records in notes.items()}
