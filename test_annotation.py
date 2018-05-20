from unittest import TestCase
from pyannotatron.models import Annotation, TimeSeriesSegmentationAnnotation, TimeSeriesRangeAnnotation, GenericJSONAnnotation
from pyannotatron.models import MultipleChoiceAnnotation, TextAnnotation, AnnotationKind, AnnotationSource
import datetime


class TestAnnotation(TestCase):

    def test_time_series_segmentation(self):
        input_json = {
            "created": "2018-04-23T18:25:43.511000Z",
            "kind": "TimeSeriesSegmentationAnnotation",
            "source": "Human",
            "summaryCode": "WORDS",
            "segments": [
                0.1, 2.0
            ],
            "annotations": [
                "hello", "world"
            ]
        }

        result = Annotation.from_json(input_json)
        self.assertEqual(type(result), TimeSeriesSegmentationAnnotation)
        self.assertEqual(result.created, datetime.datetime(2018, 4, 23, 18, 25, 43, 511000))
        self.assertEqual(result.kind, AnnotationKind.TIME_SERIES_SEGMENTATION)
        self.assertEqual(result.source, AnnotationSource.HUMAN)
        self.assertEqual(result.summary_code, "WORDS")
        self.assertAlmostEqual(result.segments[0], 0.1)
        self.assertAlmostEqual(result.segments[1], 2.0)

        self.assertAlmostEqual(result.annotations[0], "hello")
        self.assertAlmostEqual(result.annotations[1], "world")

        output_json = result.to_json()
        self.assertDictEqual(input_json, output_json)

    def test_time_series_range(self):
        input_json = {
            "created": "2018-04-23T18:25:43.511000Z",
            "kind": "TimeSeriesRangeAnnotation",
            "source": "SystemGenerated",
            "summaryCode": "AMBIENT",
            "ranges": [
                {"label": "noisy", "start": 0.0, "end": 0.1},
                {"label": "talking", "start": 0.1, "end": 0.25}
            ]
        }

        result = Annotation.from_json(input_json)
        self.assertEqual(type(result), TimeSeriesRangeAnnotation)
        self.assertEqual(result.created, datetime.datetime(2018, 4, 23, 18, 25, 43, 511000))
        self.assertEqual(result.kind, AnnotationKind.TIME_SERIES_RANGE)
        self.assertEqual(result.source, AnnotationSource.SYSTEM_GENERATED)
        self.assertEqual(result.summary_code, "AMBIENT")
        self.assertEqual(result.ranges[0].label, "noisy")
        self.assertEqual(result.ranges[1].label, "talking")
        self.assertAlmostEqual(result.ranges[0].start, 0.0)
        self.assertAlmostEqual(result.ranges[1].start, 0.1)
        self.assertAlmostEqual(result.ranges[0].end, 0.1)
        self.assertAlmostEqual(result.ranges[1].end, 0.25)

        output_json = result.to_json()
        self.assertDictEqual(input_json, output_json)

    def test_generic_json(self):
        input_json = {
            "created": "2018-04-23T18:25:43.511000Z",
            "kind": "GenericJSONAnnotation",
            "source": "Reference",
            "summaryCode": "TRANSCRIPT",
            "content": {
                "arbitraryKey": {
                    "some": "arbitrary",
                    "values": [1, 2, 3]
                }
            }
        }

        result = Annotation.from_json(input_json)
        self.assertEqual(type(result), GenericJSONAnnotation)
        self.assertEqual(result.created, datetime.datetime(2018, 4, 23, 18, 25, 43, 511000))
        self.assertEqual(result.kind, AnnotationKind.GENERIC_JSON)
        self.assertEqual(result.source, AnnotationSource.REFERENCE)
        self.assertEqual(result.summary_code, "TRANSCRIPT")
        self.assertEqual(result.content, input_json["content"])

        output_json = result.to_json()
        self.assertDictEqual(input_json, output_json)

    def test_multiple_choice(self):
        input_json = {
            "created": "2018-04-23T18:25:43.511000Z",
            "kind": "MultipleChoiceAnnotation",
            "source": "Aggregated",
            "summaryCode": "SENTIMENT",
            "choices": ["positive"]
        }

        result = Annotation.from_json(input_json)
        self.assertEqual(type(result), MultipleChoiceAnnotation)
        self.assertEqual(result.created, datetime.datetime(2018, 4, 23, 18, 25, 43, 511000))
        self.assertEqual(result.kind, AnnotationKind.MULTIPLE_CHOICE)
        self.assertEqual(result.source, AnnotationSource.AGGREGATED)
        self.assertEqual(result.summary_code, "SENTIMENT")
        self.assertEqual(result.choices[0], "positive")

        output_json = result.to_json()
        self.assertDictEqual(input_json, output_json)

    def test_text(self):
        input_json = {
            "created": "2018-04-23T18:25:43.511000Z",
            "kind": "TextAnnotation",
            "source": "Human",
            "summaryCode": "EVALUATION",
            "content": "?"
        }

        result = Annotation.from_json(input_json)
        self.assertEqual(type(result), TextAnnotation)
        self.assertEqual(result.created, datetime.datetime(2018, 4, 23, 18, 25, 43, 511000))
        self.assertEqual(result.kind, AnnotationKind.TEXT)
        self.assertEqual(result.source, AnnotationSource.HUMAN)
        self.assertEqual(result.summary_code, "EVALUATION")
        self.assertEqual(result.content, "?")

        output_json = result.to_json()
        self.assertDictEqual(input_json, output_json)
