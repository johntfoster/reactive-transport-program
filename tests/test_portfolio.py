import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('portfolio',ROOT/'tools/portfolio.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class PortfolioTests(unittest.TestCase):
 def test_snapshots_have_four_independent_authorities(self):
  result=mod.audit();self.assertEqual(result['errors'],0);self.assertEqual(len(result['projects']),4);self.assertFalse(result['paper_repositories_modified'])
 def test_missing_checkouts_reported_without_creating_them(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);before=list(p.iterdir());r=mod.audit(papers=p);self.assertEqual(r['errors'],4);self.assertEqual(list(p.iterdir()),before)
 def test_escaping_snapshot_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);(p/'portfolio.json').write_text(json.dumps({'projects':[{'id':'bad','repository':'https://example.org','manifest':'../escape'}]}))
   with self.assertRaises(ValueError):mod.audit(p)
 def test_output_outside_runtime_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaises(ValueError):mod.build(Path(d))
if __name__=='__main__':unittest.main()
