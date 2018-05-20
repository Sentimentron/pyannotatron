from unittest import TestCase
from pyannotatron.models import Question, MultipleChoiceQuestion, TimeSeriesSegmentationQuestion, TimeSeriesRangeQuestion, QuestionKind
import datetime


class TestQuestion(TestCase):

    def test_multiple_choice(self):
        input_json = {
            "created": "2018-04-23T18:25:43.511000Z",
            "summaryCode": "SENTIMENT",
            "humanPrompt": "Judge whether this text is positive",
            "kind": "MultipleChoiceQuestion",
            "annotationInstructions": "Select the best match.",
            "detailedAnnotationInstructions": "If unsure, write a note explaining why",
            "choices": ["positive", "negative"],
            "assets": [99199291, 1132231]
        }
        result = Question.from_json(input_json)
        self.assertEqual(type(result), MultipleChoiceQuestion)
        self.assertEqual(result.created, datetime.datetime(2018, 4, 23, 18, 25, 43, 511000))
        self.assertEqual(result.summary_code, "SENTIMENT")
        self.assertEqual(result.human_prompt, "Judge whether this text is positive")
        self.assertEqual(result.kind, QuestionKind.MULTIPLE_CHOICE)
        self.assertEqual(result.annotation_instructions, "Select the best match.")
        self.assertEqual(result.detailed_annotation_instructions, "If unsure, write a note explaining why")
        self.assertEqual(result.assets[0], 99199291)
        self.assertEqual(result.assets[1], 1132231)

        output_json = result.to_json()
        self.assertDictEqual(input_json, output_json)

    def test_time_series_range(self):
        input_json = {
            "created": "2018-04-23T18:25:43.511000Z",
            "summaryCode": "REGIONS",
            "humanPrompt": "Select regions with background noise",
            "kind": "TimeSeriesRangeQuestion",
            "annotationInstructions": "Click between each word",
            "detailedAnnotationInstructions": "So much more to say",
            "canOverlap": True,
            "assets": None,
        }
        result = Question.from_json(input_json)
        self.assertEqual(type(result), TimeSeriesRangeQuestion)
        self.assertEqual(result.created, datetime.datetime(2018, 4, 23, 18, 25, 43, 511000))
        self.assertEqual(result.summary_code, "REGIONS")
        self.assertEqual(result.human_prompt, "Select regions with background noise")
        self.assertEqual(result.kind, QuestionKind.TIME_SERIES_RANGE)

        self.assertTrue(result.can_overlap)

        output_json = result.to_json()
        self.assertDictEqual(input_json, output_json)

    def test_time_series_segmentation(self):
        input_json = {
            "created": "2018-04-23T18:25:43.511000Z",
            "summaryCode": "WORDS",
            "humanPrompt": "Divide this audio file into words",
            "kind": "TimeSeriesSegmentationQuestion",
            "annotationInstructions": "Click between each word",
            "detailedAnnotationInstructions": "So much more to say",
            "maximumSegments": 5,
            "minimumSegments": 1,
            "segmentChoices": ["hi", "world"],
            "freeFormAllowed": True,
            "assets": None,
        }
        result = Question.from_json(input_json)

        self.assertEqual(type(result), TimeSeriesSegmentationQuestion)
        self.assertEqual(result.created, datetime.datetime(2018, 4, 23, 18, 25, 43, 511000))
        self.assertEqual(result.summary_code, "WORDS")
        self.assertEqual(result.human_prompt, "Divide this audio file into words")
        self.assertEqual(result.kind, QuestionKind.TIME_SERIES_SEGMENTATION)
        self.assertEqual(result.maximum_segments, 5)
        self.assertEqual(result.minimum_segments, 1)
        self.assertEqual(result.segment_choices[0], "hi")
        self.assertEqual(result.segment_choices[1], "world")
        self.assertEqual(result.annotation_instructions, "Click between each word")
        self.assertEqual(result.detailed_annotation_instructions, "So much more to say")
        self.assertTrue(result.free_form_allowed, True)

        output_json = result.to_json()
        self.assertDictEqual(input_json, output_json)
