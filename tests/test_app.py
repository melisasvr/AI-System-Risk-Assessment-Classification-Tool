import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest

class AppTests(unittest.TestCase):
    def test_example_submission_and_downloads(self):
        at=AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app/main.py')).run()
        self.assertFalse(at.exception)
        at.sidebar.selectbox[0].select('Candidate ranking assistant').run()
        at.button[0].click().run()
        self.assertFalse(at.exception)
        self.assertEqual(at.metric[0].value,'High Risk')
        self.assertEqual(at.metric[1].value,'70 / 100')
        self.assertEqual(len(at.get('download_button')),2)
    def test_empty_form_validation(self):
        at=AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app/main.py')).run()
        at.button[0].click().run()
        self.assertFalse(at.exception)
        self.assertGreater(len(at.error),0)
if __name__=='__main__': unittest.main()
