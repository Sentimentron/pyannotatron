from unittest import TestCase
from pyannotatron.models import BinaryAsset, BinaryAssetKind, AssetCorpusLink
import datetime
import hashlib


class TestAsset(TestCase):

    def test_link(self):
        input_json = {
            "uniqueName": "001/001_221.wav",
            "assetId": 42,
            "corpusId": 5
        }

        result = AssetCorpusLink.from_json(input_json)
        self.assertEqual(result.unique_name, "001/001_221.wav")
        self.assertEqual(result.asset_id, 42)
        self.assertEqual(result.corpus_id, 5)

        output_json = result.to_json()
        self.assertDictEqual(input_json, output_json)

    def test_asset(self):

        m = hashlib.sha512()
        m.update("hello world".encode("utf8"))
        m = m.hexdigest()

        input_json = {
            "id": 7,
            "userIdWhoUploaded": 5,
            "content": "aGVsbG8gd29ybGQ=",
            "metadata": {
                "arbitraryKey": "arbitraryValue"
            },
            "dateUploaded": "2018-04-23T18:25:43.511000Z",
            "copyrightAndUsageRestrictions": "No redistribution",
            "checksum": m,
            "mimeType": "text/plain",
            "typeDescription": "UTF8Text"
        }

        result = BinaryAsset.from_json(input_json)
        self.assertEqual(result.id, 7)
        self.assertEqual(result.uploader_id, 5)
        self.assertEqual(result.content, "hello world".encode("utf8"))
        self.assertDictEqual(result.metadata, input_json["metadata"])
        self.assertEqual(result.date_uploaded, datetime.datetime(2018, 4, 23, 18, 25, 43, 511000))
        self.assertEqual(result.copyright, "No redistribution")
        self.assertEqual(result.checksum, m)
        self.assertEqual(result.mime_type, "text/plain")
        self.assertEqual(result.type_description, BinaryAssetKind.UTF8_TEXT)

        output_json = result.to_json()
        self.assertDictEqual(input_json, output_json)
