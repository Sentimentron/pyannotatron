from unittest import TestCase
from pyannotatron.models import Assignment
import datetime


class TestAssignment(TestCase):

    def test_assignment(self):
        self.max_diff = None
        response_input_json = {
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
        question_input_json = {
            "created": "2018-04-23T18:25:43.511000Z",
            "summaryCode": "SENTIMENT",
            "humanPrompt": "Judge whether this text is positive",
            "kind": "MultipleChoiceQuestion",
            "annotationInstructions": "Select the best match.",
            "detailedAnnotationInstructions": "If unsure, write a note explaining why",
            "choices": ["positive", "negative"],
            "assets": [99199291, 1132231]
        }
        input_json = {
            "assets": [1, 22],
            "assignedUserId": 47,
            "assignedAnnotatorId": 12,
            "question": question_input_json,
            "response": response_input_json,
            "assignedReviewerId": 47,
            "created": "2018-04-23T18:25:43.511000Z",
            "completed": "2018-04-23T18:25:43.511000Z",
        }

        a = Assignment.from_json(input_json)
        self.assertEqual(a.assets, [1, 22])
        self.assertEqual(a.assigned_user_id, 47)
        self.assertEqual(a.assigned_annotator_id, 12)
        self.assertEqual(a.assigned_reviewer_id, 47)
        self.assertEqual(a.created, datetime.datetime(2018, 4, 23, 18, 25, 43, 511000))
        self.assertEqual(a.completed, datetime.datetime(2018, 4, 23, 18, 25, 43, 511000))

        b = a.to_json()
        self.maxDiff = None
        self.assertDictEqual(b, input_json)

