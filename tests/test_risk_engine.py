import json
import unittest
from pathlib import Path
from pydantic import ValidationError
from app.risk_engine import assess
from app.risk_card import generate_markdown
from app.schemas import SystemInput, Tier

EXAMPLES=json.loads((Path(__file__).resolve().parents[1]/'data/examples.json').read_text())
class EngineTests(unittest.TestCase):
    def system(self, **changes):
        return SystemInput.model_validate(EXAMPLES[0] | changes)
    def test_example_tiers(self):
        self.assertEqual([assess(SystemInput.model_validate(e)).tier for e in EXAMPLES],list(Tier))
    def test_high_stakes_floor(self):
        for autonomy in ['Human decides','Human approves','Fully autonomous']:
            a=assess(self.system(high_stakes=True,autonomy=autonomy))
            self.assertEqual(a.tier,Tier.HIGH)
            self.assertGreaterEqual(a.score,60)
    def test_transparency_floor(self):
        self.assertEqual(assess(self.system(public_facing=True)).score,20)
    def test_sensitive_data_not_automatic_high(self):
        self.assertEqual(assess(self.system(data_type='Sensitive / biometric')).tier,Tier.LIMITED)
    def test_domain_alone_not_high(self):
        self.assertEqual(assess(self.system(domain='Healthcare')).tier,Tier.MINIMAL)
    def test_prohibited_overrides(self):
        self.assertEqual(assess(self.system(prohibited_practices=['social_scoring'])).score,100)
    def test_incomplete_screening(self):
        self.assertTrue(any('INCOMPLETE' in x for x in assess(self.system(screening_complete=False)).review_notes))
    def test_invalid_input(self):
        for changes in [dict(purpose=' '),dict(domain='invalid'),dict(prohibited_practices=['unknown'])]:
            with self.assertRaises(ValidationError): self.system(**changes)
    def test_json_roundtrip(self):
        a=assess(self.system())
        self.assertEqual(type(a).model_validate_json(a.model_dump_json()),a)
    def test_card_trace(self):
        a=assess(self.system(high_stakes=True))
        card=generate_markdown(a)
        for value in [a.assessment_id,'H02','Human oversight','not legal advice']:
            self.assertIn(value,card)
    def test_thresholds_and_cap(self):
        self.assertEqual(assess(self.system(data_type='Personal')).tier,Tier.MINIMAL)
        a=assess(self.system(high_stakes=True,safety_component=True,consequential_decisions=True,domain='Healthcare',autonomy='Fully autonomous',data_type='Sensitive / biometric',vulnerable_people=True))
        self.assertGreater(a.raw_score,100)
        self.assertEqual(a.score,100)
        self.assertEqual(a.tier,Tier.HIGH)
if __name__=='__main__': unittest.main()
