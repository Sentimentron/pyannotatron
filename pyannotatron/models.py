import datetime
from enum import Enum

from .utils import generic_from_json, generic_to_json, parse_json_date, date_to_json, base64_to_bytes, bytes_to_base64


class AnnotatronMixin:
    """
        Contains some generic methods.
    """

    MAP = {}

    @classmethod
    def from_json(cls, json_dict):
        return cls(**generic_from_json(json_dict, cls.MAP))

    def to_json(self):
        return generic_to_json(self.__dict__, self.MAP)


class AnnotationSource(Enum):
    """
        Represents where an Annotation comes from.
    """
    REFERENCE = "Reference"
    SYSTEM_GENERATED = "SystemGenerated"
    HUMAN = "Human"
    AGGREGATED = "Aggregated"


class AnnotationKind(Enum):
    """
        Annotatron uses this field to describe the structure of an Annotation's JSON data.
    """
    TIME_SERIES_SEGMENTATION = "TimeSeriesSegmentationAnnotation"
    TIME_SERIES_RANGE = "TimeSeriesRangeAnnotation"
    MULTIPLE_CHOICE = "MultipleChoiceAnnotation"
    GENERIC_JSON = "GenericJSONAnnotation"
    TEXT = "TextAnnotation"

class UserKind(Enum):
    ADMINISTRATOR = "Administrator"
    STAFF = "Staff"
    REVIEWER = "Reviewer"
    ANNOTATOR = "Annotator"

class AbstractAnnotation:
    """
        Abstract class representing everything that an Annotation should have
    """

    def __init__(self, created: datetime.datetime, source: AnnotationSource, kind: AnnotationKind, summary_code: str):
        self.created = created
        self.source = source
        self.kind = kind
        self.summary_code = summary_code


class QuestionKind(Enum):
    TIME_SERIES_SEGMENTATION = "TimeSeriesSegmentationQuestion"
    TIME_SERIES_RANGE = "TimeSeriesRangeQuestion"
    MULTIPLE_CHOICE = "MultipleChoiceQuestion"


class AbstractQuestion:
    def __init__(self, created: datetime.datetime, summary_code: str, human_prompt: str, kind: QuestionKind,
                 annotation_instructions=None, detailed_annotation_instructions=None):
        self.created = created
        self.summary_code = summary_code
        self.human_prompt = human_prompt
        self.kind = kind
        self.annotation_instructions = annotation_instructions
        self.detailed_annotation_instructions = detailed_annotation_instructions


class MultipleChoiceQuestion(AbstractQuestion):
    def __init__(self, created: datetime.datetime, summary_code: str, human_prompt: str, kind: QuestionKind,
                 choices: list, annotation_instructions=None, detailed_annotation_instructions=None):
        super().__init__(created, summary_code, human_prompt, kind, annotation_instructions,
                         detailed_annotation_instructions)
        self.choices = choices

    MAP = {
        "summaryCode": "summary_code",
        "humanPrompt": "human_prompt",
        "annotationInstructions": "annotation_instructions",
        "detailedAnnotationInstructions": "detailed_annotation_instructions",
        "created": ("created", lambda x: parse_json_date(x), lambda x: date_to_json(x)),
        "kind": ("kind", lambda x: QuestionKind(x), lambda x: x.value)
    }

    @classmethod
    def from_json(cls, json_dict):
        return cls(**generic_from_json(json_dict, cls.MAP))

    def to_json(self):
        assert self.kind == QuestionKind.MULTIPLE_CHOICE
        ret = generic_to_json(self.__dict__, self.MAP)
        return ret


class TimeSeriesRangeQuestion(AbstractQuestion):
    def __init__(self, created: datetime.datetime, summary_code: str, human_prompt: str, kind: QuestionKind,
                 annotation_instructions = None, detailed_annotation_instructions = None, can_overlap: bool = False):
        super().__init__(created, summary_code, human_prompt, kind, annotation_instructions, detailed_annotation_instructions)
        self.can_overlap = can_overlap

    MAP = {
        "summaryCode": "summary_code",
        "humanPrompt": "human_prompt",
        "canOverlap": "can_overlap",
        "detailedAnnotationInstructions": "detailed_annotation_instructions",
        "annotationInstructions": "annotation_instructions",
        "created": ("created", lambda x: parse_json_date(x), lambda x: date_to_json(x)),
        "kind": ("kind", lambda x: QuestionKind(x), lambda x: x.value)
    }

    @classmethod
    def from_json(cls, json_dict):
        return cls(**generic_from_json(json_dict, cls.MAP))

    def to_json(self):
        assert self.kind == QuestionKind.TIME_SERIES_RANGE
        ret = generic_to_json(self.__dict__, self.MAP)
        return ret


class TimeSeriesSegmentationQuestion(AbstractQuestion):
    def __init__(self, created: datetime.datetime, summary_code: str, human_prompt: str, kind: QuestionKind,
                 annotation_instructions=None, detailed_annotation_instructions=None,
                 maximum_segments: int = 0, minimum_segments: int = 0, segment_choices: list = [],
                 free_form_allowed: bool = False,):
        super().__init__(created, summary_code, human_prompt, kind, annotation_instructions,
                         detailed_annotation_instructions)
        self.maximum_segments = maximum_segments
        self.minimum_segments = minimum_segments
        self.segment_choices = segment_choices
        self.free_form_allowed = free_form_allowed

    MAP = {
        "summaryCode": "summary_code",
        "humanPrompt": "human_prompt",
        "maximumSegments": "maximum_segments",
        "minimumSegments": "minimum_segments",
        "segmentChoices": "segment_choices",
        "freeFormAllowed": "free_form_allowed",
        "annotationInstructions": "annotation_instructions",
        "detailedAnnotationInstructions": "detailed_annotation_instructions",
        "created": ("created", lambda x: parse_json_date(x), lambda x: date_to_json(x)),
        "kind": ("kind", lambda x: QuestionKind(x), lambda x: x.value)
    }

    @classmethod
    def from_json(cls, json_dict):
        assert QuestionKind(json_dict["kind"]) == QuestionKind.TIME_SERIES_SEGMENTATION
        return cls(**generic_from_json(json_dict, cls.MAP))

    def to_json(self):
        assert self.kind == QuestionKind.TIME_SERIES_SEGMENTATION
        ret = generic_to_json(self.__dict__, self.MAP)
        return ret


class TimeSeriesSegmentationAnnotation(AbstractAnnotation):
    def __init__(self, created: datetime, source: AnnotationSource, summary_code: str,
                 segments: list, annotations: list, kind=AnnotationKind.TIME_SERIES_SEGMENTATION):
        super().__init__(created, source, kind, summary_code)
        self.segments = segments
        self.annotations = annotations

    MAP = {
        "summaryCode": "summary_code",
        "source": ("source", lambda x: AnnotationSource(x), lambda x: x.value),
        "kind": ("kind", lambda x: AnnotationKind(x), lambda x: x.value),
        "created": ("created", lambda x: parse_json_date(x), lambda x: date_to_json(x))
    }

    @classmethod
    def from_json(cls, json_dict):
        return cls(**generic_from_json(json_dict, cls.MAP))

    def to_json(self):
        assert self.kind == AnnotationKind.TIME_SERIES_SEGMENTATION
        ret = generic_to_json(self.__dict__, self.MAP)
        return ret


class TimeSeriesRangeTuple(AnnotatronMixin):
    def __init__(self, label: str, start: float, end: float):
        self.label = label
        self.start = start
        self.end = end

    MAP = {}

    @classmethod
    def convert_from_json_list(cls, x):
        return [cls.from_json(i) for i in x]

    @classmethod
    def convert_to_json_list(cls, x):
        return [i.to_json() for i in x]


class TimeSeriesRangeAnnotation(AbstractAnnotation):
    def __init__(self, created: datetime, source: AnnotationSource, summary_code: str,
                 ranges: list, kind=AnnotationKind.TIME_SERIES_RANGE):
        super().__init__(created, source, kind, summary_code)
        self.ranges = ranges

    MAP = {
        "summaryCode": "summary_code",
        "created": ("created", lambda x: parse_json_date(x), lambda x: date_to_json(x)),
        "source": ("source", lambda x: AnnotationSource(x), lambda x: x.value),
        "kind": ("kind", lambda x: AnnotationKind(x), lambda x: x.value),
        "ranges": ("ranges", lambda x: TimeSeriesRangeTuple.convert_from_json_list(x),
                  lambda x: TimeSeriesRangeTuple.convert_to_json_list(x))
    }

    @classmethod
    def from_json(cls, json_dict):
        assert AnnotationKind(json_dict["kind"]) == AnnotationKind.TIME_SERIES_RANGE
        return cls(**generic_from_json(json_dict, cls.MAP))

    def to_json(self):
        assert self.kind == AnnotationKind.TIME_SERIES_RANGE
        ret = generic_to_json(self.__dict__, self.MAP)
        return ret


class GenericJSONAnnotation(AbstractAnnotation):
    def __init__(self, created: datetime, source: AnnotationSource, summary_code: str,
                 content, kind=AnnotationKind.GENERIC_JSON):
        super().__init__(created, source, kind, summary_code)
        self.content = content

    MAP = {
        "summaryCode": "summary_code",
        "source": ("source", lambda x: AnnotationSource(x), lambda x: x.value),
        "kind": ("kind", lambda x: AnnotationKind(x), lambda x: x.value),
        "created": ("created", lambda x: parse_json_date(x), lambda x: date_to_json(x)),
    }

    @classmethod
    def from_json(cls, json_dict):
        assert AnnotationKind(json_dict["kind"]) == AnnotationKind.GENERIC_JSON
        return cls(**generic_from_json(json_dict, cls.MAP))

    def to_json(self):
        assert self.kind == AnnotationKind.GENERIC_JSON
        ret = generic_to_json(self.__dict__, self.MAP)
        return ret


class MultipleChoiceAnnotation(AbstractAnnotation):
    def __init__(self, created: datetime, source: AnnotationSource, summary_code: str,
                 choices: list, kind=AnnotationKind.MULTIPLE_CHOICE):
        super().__init__(created, source, kind, summary_code)
        self.choices = choices

    MAP = {
        "summaryCode": "summary_code",
        "source": ("source", lambda x: AnnotationSource(x), lambda x: x.value),
        "kind": ("kind", lambda x: AnnotationKind(x), lambda x: x.value),
        "created": ("created", lambda x: parse_json_date(x), lambda x: date_to_json(x)),
    }

    @classmethod
    def from_json(cls, json_dict):
        return cls(**generic_from_json(json_dict, cls.MAP))

    def to_json(self):
        assert self.kind == AnnotationKind.MULTIPLE_CHOICE
        ret = generic_to_json(self.__dict__, self.MAP)
        return ret


class TextAnnotation(AbstractAnnotation):
    def __init__(self, created: datetime, source: AnnotationSource, summary_code: str,
                 content: str, kind=AnnotationKind.MULTIPLE_CHOICE):
        super().__init__(created, source, kind, summary_code)
        self.content = content

    MAP = {
        "summaryCode": "summary_code",
        "source": ("source", lambda x: AnnotationSource(x), lambda x: x.value),
        "kind": ("kind", lambda x: AnnotationKind(x), lambda x: x.value),
        "created": ("created", lambda x: parse_json_date(x), lambda x: date_to_json(x))
    }

    @classmethod
    def from_json(cls, json_dict):
        return cls(**generic_from_json(json_dict, cls.MAP))

    def to_json(self):
        assert self.kind == AnnotationKind.TEXT
        ret = generic_to_json(self.__dict__, self.MAP)
        return ret


class Annotation:
    """
        Factory class that returns AbstractAnnotation subclasses.
    """

    CONVERSION_TABLE = {
        AnnotationKind.MULTIPLE_CHOICE: MultipleChoiceAnnotation,
        AnnotationKind.GENERIC_JSON: GenericJSONAnnotation,
        AnnotationKind.TIME_SERIES_RANGE: TimeSeriesRangeAnnotation,
        AnnotationKind.TIME_SERIES_SEGMENTATION: TimeSeriesSegmentationAnnotation,
        AnnotationKind.TEXT: TextAnnotation
    }

    @classmethod
    def from_json(cls, json_dict):
        return cls.CONVERSION_TABLE[AnnotationKind(json_dict['kind'])].from_json(json_dict)


class AssetCorpusLink(AnnotatronMixin):

    def __init__(self, unique_name: str, asset_id: int, corpus_id: int):
        self.unique_name = unique_name
        self.asset_id = asset_id
        self.corpus_id = corpus_id

    MAP = {
        "uniqueName": "unique_name",
        "assetId": "asset_id",
        "corpusId": "corpus_id"
    }


class Assignment(AnnotatronMixin):

    def __init__(self, user_id: int, question_id: int, created=datetime.datetime.now(),
                 assigned_reviewer_id: int = 0, actual_reviewer_id: int = None,
                 completed=None, reviewed=None, annotator_notes: str = None, reviewer_notes: str = None,
                 original_annotation_id: int = None, corrected_annotation_id: int = None
                 ):
        self.user_id = user_id
        self.question_id = question_id
        self.created = created
        self.assigned_reviewer_id = assigned_reviewer_id
        self.actual_reviewer_id = actual_reviewer_id
        self.completed = completed
        self.reviewed = reviewed
        self.annotator_nots = annotator_notes
        self.reviewer_notes = reviewer_notes
        self.original_annotation_id = original_annotation_id
        self.corrected_annotation_id = corrected_annotation_id

    MAP = {
        "userId": "user_id",
        "questionId": "question_id",
        "assignedReviewerId": "assigned_reviewer_id",
        "actualReviewerId": "assigned_reviewer_id",
        "annotatorNotes": "annotator_notes",
        "reviewerNotes": "reviewer_notes",
        "originalAnnotationId": "original_annotation_id",
        "correctedAnnotationId": "corrected_annotation_id",
    }


class BinaryAssetKind(Enum):
    UTF8_TEXT = "UTF8Text"
    AUDIO = "Audio"
    IMAGE = "Image"
    VIDEO = "Video"
    OTHER = "Other"


class BinaryAsset(AnnotatronMixin):
    """
        Represents Annotatron's idea of a document, stored in a Corpus.

        Derived from BinaryAsset and BinaryAssetDescription in the OpenAPI spec.
    """

    def __init__(self, content: bytes, mime_type, type_description: BinaryAssetKind, copyright, checksum,
                 uploader_id: int = 0, date_uploaded=datetime.datetime.now(), id: int = 0,
                 metadata=None):
        self.content = content
        self.mime_type = mime_type
        self.type_description = type_description
        self.copyright = copyright
        self.checksum = checksum
        self.uploader_id = uploader_id
        self.date_uploaded = date_uploaded
        self.id = id
        self.metadata = metadata

    MAP = {
        "userIdWhoUploaded": "uploader_id",
        "dateUploaded": ("date_uploaded", lambda x: parse_json_date(x), lambda x: date_to_json(x)),
        "copyrightAndUsageRestrictions": "copyright",
        "content": ("content", lambda x: base64_to_bytes(x), lambda x: bytes_to_base64(x)),
        "mimeType": "mime_type",
        "typeDescription": ("type_description", lambda x: BinaryAssetKind(x), lambda x: x.value)
    }


class ConfigurationResponse(AnnotatronMixin):
    """
        Contains information about whether Annotatron's ready to use, or whether it requires
        further information.
    """

    MAP = {
        "requiresSetup": "requires_setup"
    }

    def __init__(self, requires_setup: bool):
        self.requires_setup = requires_setup

    @classmethod
    def from_json(cls, json):
        return cls(**generic_from_json(json, cls.MAP))


class Corpus:
    """
        Represents Annotatron's concept of a corpus, which is a collection of Assets.
    """

    MAP = {
        "created": ("created", lambda x: parse_json_date(x), lambda x: date_to_json(x)),
        "copyrightAndUsageRestrictions": "copyright"
    }

    def __init__(self, name, description=None, created=datetime.datetime.now(),
                 copyright=None, id=0):
        self.name = name
        self.description = description
        self.id = id
        self.copyright = copyright
        self.created = created

    def to_json(self) -> dict:
        """
        Converts this object to an API-compatible form.
        :return: A dict, ready for conversion to JSON.
        """

        return generic_to_json(self.__dict__, self.MAP)

    @classmethod
    def from_json(cls, dict):
        return Corpus(**generic_from_json(dict, cls.MAP))


class DataLossReason(Enum):
    ASSET_STILL_LINKED_TO_CORPUS = "AssetStillLinkedToCorpus"
    ASSET_CONTAINS_ANNOTATIONS_IN_CORPUS = "AssetContainsAnnotationsInCorpus"
    QUESTION_HAS_ANNOTATIONS = "QuestionHasAnnotations"


class FieldError(AnnotatronMixin):
    def __init__(self, name, error, warning=False):
        self.name = name
        self.error = error
        self.warning = warning


class SuccessfulInsert(AnnotatronMixin):
    def __init__(self, id):
        self.id = id

    MAP = {
        "insertedId": "id"
    }

class Question:
    """
        Factory class that returns AbstractQuestion subclasses.
    """
    CONVERSION_TABLE = {
        QuestionKind.MULTIPLE_CHOICE: MultipleChoiceQuestion,
        QuestionKind.TIME_SERIES_SEGMENTATION: TimeSeriesSegmentationQuestion,
        QuestionKind.TIME_SERIES_RANGE: TimeSeriesRangeQuestion
    }

    @classmethod
    def from_json(cls, json_dict):
        return cls.CONVERSION_TABLE[QuestionKind(json_dict['kind'])].from_json(json_dict)


class NewUserRequest(AnnotatronMixin):
    MAP = {
        "role": ("role", lambda x: UserKind(x), lambda x: x.value)
    }

    def __init__(self, username, email, role, password):
        self.username = username
        self.email = email
        self.role = role
        self.password = password


class FieldError(AnnotatronMixin):

    def __init__(self, name: str, error: str, warning: bool):
        self.name = name
        self.error = error
        self.warning = warning


class ValidationError:

    def __init__(self, errors):
        self.errors = errors

    def __iter__(self):
        for err in self.errors:
            yield err

    @classmethod
    def from_json(cls, json):
        ret = []
        for item in json:
            ret.append(FieldError.from_json(item))
        return cls(ret)

    def to_json(self):
        ret = []
        for item in self:
            ret.append(item.to_json())
        return ret

class LoginResponse(AnnotatronMixin):

    def __init__(self, token):
        self.token = token

class LoginRequest(AnnotatronMixin):

    def __init__(self, username, password):
        self.username = username
        self.password = password


class AnnotatronUser(AnnotatronMixin):
    MAP = {
        "role": ("role", lambda x: UserKind(x), lambda x: x.value),
        "created": ("created", lambda x: parse_json_date(x), lambda x: date_to_json(x))
    }

    def __init__(self, username, email, role, password, created, id):
        self.username = username
        self.email = email
        self.role = role
        self.password = password
        self.created = created
        self.id = id