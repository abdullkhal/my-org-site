"""Synthetic source-review fixtures only; never confirms a real authority."""
import importlib.util
import json
import subprocess
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('confirm_source', ROOT/'scripts/confirm-source.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class SourceConfirmationTests(unittest.TestCase):
    def setUp(self):
        self.source = dict(id='synthetic', title='Example authority', authority='Synthetic fixture',
                           status='awaiting_independent_confirmation', candidate_url='https://example.invalid/',
                           public_url=None, scope='Example only', limitations='Not a real authority',
                           network_observation={'result': 'proxy_connect_403'}, evidence=[])
        self.args = dict(url='https://example.invalid/register', checked_at=date.today().isoformat(),
                         reviewer='Synthetic reviewer', evidence_url='https://example.invalid/about',
                         note='Synthetic corroboration fixture for testing only.',
                         next_review_at=(date.today()+timedelta(days=30)).isoformat())

    def test_human_review_is_independent_of_network(self):
        result = module.confirm_source(self.source, **self.args)
        self.assertEqual(result['status'], 'verified')
        self.assertEqual(result['verification_method'], 'independent_human_review')
        self.assertEqual(result['network_observation']['result'], 'proxy_connect_403')
        self.assertIsNone(self.source['public_url'])

    def test_unsafe_urls_rejected(self):
        for value in ['http://example.invalid/', 'javascript:alert(1)', 'https://user:pass@example.invalid/', 'https://example.invalid:123/']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                module.confirm_source(self.source, **{**self.args, 'url': value})

    def test_evidence_required(self):
        for patch in [{'reviewer':''}, {'note':'insufficient'}, {'evidence_url':'http://example.invalid/'}]:
            with self.subTest(patch=patch), self.assertRaises(ValueError):
                module.confirm_source(self.source, **{**self.args, **patch})

    def test_dates_checked(self):
        for patch in [{'checked_at':(date.today()+timedelta(days=1)).isoformat()}, {'next_review_at':date.today().isoformat()}]:
            with self.subTest(patch=patch), self.assertRaises(ValueError):
                module.confirm_source(self.source, **{**self.args, **patch})

    def test_confirmed_link_renders_despite_network_block(self):
        result = module.confirm_source(self.source, **self.args)
        with tempfile.TemporaryDirectory() as temp:
            temp = Path(temp)
            (temp/'scripts').mkdir(); (temp/'data').mkdir()
            (temp/'scripts/render-content.py').write_text((ROOT/'scripts/render-content.py').read_text())
            (temp/'data/sources.json').write_text(json.dumps({'sources':[result]}))
            (temp/'data/knowledge.json').write_text(json.dumps({'guides':[]}))
            (temp/'index.html').write_text('<!-- SOURCES:START --><!-- SOURCES:END --><!-- KNOWLEDGE:START --><!-- KNOWLEDGE:END -->')
            subprocess.run(['python3',str(temp/'scripts/render-content.py')],check=True)
            self.assertIn('href="https://example.invalid/register"', (temp/'index.html').read_text())

    def test_cli_defaults_to_dry_run(self):
        with tempfile.TemporaryDirectory() as temp:
            temp=Path(temp);(temp/'scripts').mkdir();(temp/'data').mkdir()
            (temp/'scripts/confirm-source.py').write_text((ROOT/'scripts/confirm-source.py').read_text())
            p=temp/'data/sources.json';p.write_text(json.dumps({'sources':[self.source]}));before=p.read_text()
            args=['python3',str(temp/'scripts/confirm-source.py'),'--source-id','synthetic']
            for key,value in self.args.items():args+=['--'+key.replace('_','-'),value]
            output=subprocess.check_output(args,text=True)
            self.assertIn('Dry run only',output)
            self.assertEqual(before,p.read_text())

if __name__ == '__main__': unittest.main()
