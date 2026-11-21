"""Exercise public-source monitoring with local HTTP response fixtures."""
from contextlib import redirect_stdout
from email.message import Message
import importlib.util
from io import BytesIO, StringIO
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

spec = importlib.util.spec_from_file_location(
    "source_monitor", Path(__file__).resolve().parents[1] / "scripts/monitor-sources.py"
)
monitor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(monitor)


def response(content):
    body = BytesIO(content.encode())
    body.headers = Message()
    body.headers["Content-Type"] = "text/html; charset=utf-8"
    return body


class SourceMonitorTests(unittest.TestCase):
    def test_fingerprint_ignores_scripts_and_whitespace(self):
        url = "https://example.invalid/notice"
        robots = "User-agent: *\nAllow: /\n"
        with patch.object(monitor, "request", side_effect=[
            response(robots), response("<main>Notice   one</main><script>session=1</script>"),
            response(robots), response("<main>Notice one</main><script>session=2</script>"),
        ]):
            self.assertEqual(monitor.snapshot(url), monitor.snapshot(url))

    def test_respects_robots_before_requesting_page(self):
        with patch.object(monitor, "request", return_value=response("User-agent: *\nDisallow: /private")) as request:
            with self.assertRaisesRegex(ValueError, "robots.txt"):
                monitor.snapshot("https://example.invalid/private/notice")
            request.assert_called_once_with("https://example.invalid/robots.txt")

    def test_broken_and_inconclusive_links_are_distinct(self):
        url = "https://example.invalid/notice"
        for status, outcome in [(404, "broken"), (403, "inconclusive"), (301, "redirect; review destination")]:
            with self.subTest(status=status), patch.object(
                monitor, "request", side_effect=HTTPError(url, status, "Fixture", {}, None)
            ):
                self.assertEqual(monitor.link_status(url)["outcome"], outcome)

    def test_identical_changes_are_queued_once_and_baseline_is_reusable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data = root / "data"
            data.mkdir()
            sources = [
                {"id": key, "url": f"https://example.invalid/{key}", "enabled": True}
                for key in ("one", "two")
            ]
            (data / "monitoring.json").write_text(json.dumps({"sources": sources}))
            output, baseline = root / "output", root / "baseline.json"
            with patch.object(monitor, "ROOT", root), patch.object(monitor, "official_links", return_value=[]), patch.object(
                monitor, "snapshot", return_value="same-hash"
            ), patch("sys.argv", ["monitor", "--output", str(output), "--baseline", str(baseline)]), redirect_stdout(StringIO()):
                monitor.main()
                report = output / "review-queue.json"
                self.assertEqual(len(json.loads(report.read_text())["review_candidates"]), 1)
                self.assertEqual(json.loads(baseline.read_text()), {"one": "same-hash", "two": "same-hash"})
                monitor.main()
                self.assertEqual(json.loads(report.read_text())["review_candidates"], [])
