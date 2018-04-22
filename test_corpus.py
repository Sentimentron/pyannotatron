from unittest import TestCase
import datetime
from pyannotatron import Corpus

class TestCorpus(TestCase):

    def test_corpus(self):
        input_json = {
            "id": 7,
            "name": "VCTK",
            "description": "Contains short utterances from multiple speakers",
            "created": "2018-04-23T18:25:43.511000Z",
            "copyrightAndUsageRestrictions": "Creative Commons Open Data"
        }

        result = Corpus.from_json(input_json)
        self.assertEqual(result.created, datetime.datetime(2018, 4, 23, 18, 25, 43, 511000))

        output_json = result.to_json()
        self.assertDictEqual(input_json, output_json)
