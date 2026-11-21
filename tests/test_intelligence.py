"""Exercise release content end to end in a disposable copy."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PUBLICATION = "2026-11-21"


class IntelligenceTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for directory in ("assets", "data", "scripts", "site"):
            shutil.copytree(ROOT / directory, self.root / directory)
        for pattern in ("*.html", "*.js", "*.css"):
            for path in ROOT.glob(pattern):
                shutil.copy(path, self.root / path.name)
        origin = {"organisation": "Fixture publisher", "url": "https://example.invalid/source", "published_at": None}
        self.review = {"reviewer": "Fixture reviewer", "evidence": "Synthetic only", "limitations": "Synthetic scope",
                       "discovered_at": PUBLICATION, "reviewed_at": PUBLICATION, "updated_at": PUBLICATION,
                       "sources": [origin]}
        self.article = dict(id="fixture-story", status="approved", title="Fixture Market Story", category="Housing",
                            kind="PIIK analysis", published=PUBLICATION, event_date=None, region="Kenya",
                            summary="Fixture article.", image="apartments", guide_id="agents",
                            what_happened="Fixture facts.", why="Fixture relevance.", affected="Fixture readers.",
                            next="Fixture checks.", review=self.review)
        self.edition = dict(id="fixture-issue", status="approved", title="Fixture Brief", summary="Fixture edition",
                            reviewed_at=PUBLICATION, reviewer="Fixture editor", published=PUBLICATION,
                            entries=[{"section": "Market Pulse", "article_id": self.article["id"]}])

    def data(self, name, change):
        path = self.root / "data" / f"{name}.json"
        contents = json.loads(path.read_text())
        change(contents)
        path.write_text(json.dumps(contents))

    def run_script(self, name, *args):
        return subprocess.run([sys.executable, f"scripts/{name}.py", *args], cwd=self.root,
                              capture_output=True, text=True)

    def assert_pass(self, name, *args):
        result = self.run_script(name, *args)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result

    def assert_fail(self, name, message, *args):
        result = self.run_script(name, *args)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(message, result.stderr)

    def read(self, path):
        return (self.root / path).read_text()

    def test_publication_updates_home_archive_notices_directory_search_and_feed(self):
        notice = dict(id="fixture-notice", status="approved", title="Fixture Official Notice",
                      date=PUBLICATION, event_date=None, region="Nairobi", kind="Official publication",
                      summary="Fixture notice.", next="Ask the fixture authority.", review=self.review)
        profile = dict(id="fixture-business", status="approved", name="Fixture Property Business",
                       category="Estate agencies", location="Nairobi", website="https://example.invalid/",
                       source="https://example.invalid/source", services="Fixture services", authority_id="earb",
                       checked_at=PUBLICATION, published=PUBLICATION, review=self.review)
        self.data("editorial", lambda data: (
            data["articles"].append(self.article), data["editions"].append(self.edition), data["notices"].append(notice)
        ))
        self.data("directory", lambda data: data["profiles"].append(profile))
        self.assert_pass("build-site")
        self.assert_pass("build-site", "--check")
        self.assert_pass("check-links")
        for path in ("index.html", "weekly.html", "search.html", "feed.xml"):
            self.assertIn("brief-fixture-issue.html", self.read(path))
        self.assertIn("https://wa.me/", self.read("brief-fixture-issue.html"))
        self.assertIn("Fixture publisher", self.read("brief-fixture-issue.html"))
        self.assertIn("Fixture Market Story", self.read("search.html"))
        for path, values in (("watch.html", ["Fixture Official Notice", "Ask the fixture authority"]),
                             ("directory.html", ["Fixture Property Business", "does not represent endorsement"]),
                             ("search.html", ["Fixture Property Business", "Fixture Official Notice"])):
            for value in values:
                self.assertIn(value, self.read(path))
        self.data("directory", lambda data: data["profiles"].append({**profile, "id": "duplicate-fixture"}))
        self.assert_fail("build-site", "duplicate organisation")

    def test_draft_and_incomplete_evidence_do_not_publish(self):
        self.article["status"] = "draft"
        self.article.pop("review")
        self.data("editorial", lambda data: data["articles"].append(self.article))
        self.assert_pass("build-site")
        self.assertNotIn("Fixture Market Story", self.read("search.html"))
        self.assertFalse((self.root / "article-fixture-story.html").exists())
        self.assert_fail("build-site", "Draft records must stay outside", "--check")
        self.data("editorial", lambda data: data["articles"][-1].update(status="approved"))
        self.assert_fail("build-site", "missing evidence review")
        self.assertFalse((self.root / "article-fixture-story.html").exists())

    def test_withdrawal_preserves_url_without_indexing_or_republishing_story(self):
        self.data("editorial", lambda data: data["articles"].append(self.article))
        self.assert_pass("build-site")

        def withdraw(data):
            data["articles"][-1] = dict(id=self.article["id"], status="withdrawn")
            data["corrections"].append(dict(id="fixture-withdrawal", target_kind="article",
                                            target_id=self.article["id"], published=PUBLICATION,
                                            reviewer="Fixture editor", explanation="Fixture withdrawal."))

        self.data("editorial", withdraw)
        self.assert_pass("build-site")
        self.assert_pass("check-links")
        self.assertIn("noindex,follow", self.read("article-fixture-story.html"))
        self.assertIn("Fixture withdrawal", self.read("article-fixture-story.html"))
        for path in ("article-fixture-story.html", "search.html", "feed.xml", "sitemap.xml"):
            self.assertNotIn("Fixture Market Story", self.read(path))
        self.assertNotIn("article-fixture-story.html", self.read("sitemap.xml"))
