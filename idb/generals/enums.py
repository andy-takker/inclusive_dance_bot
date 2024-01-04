from enum import StrEnum, unique


@unique
class SubmenuType(StrEnum):
    CHARITY = "CHARITY"
    EDUCATION = "EDUCATION"
    ENROLL = "ENROLL"
    EVENT = "EVENT"
    INFORMATION = "INFORMATION"
    OTHER = "OTHER"


@unique
class FeedbackType(StrEnum):
    QUESTION = "QUESTION"
    ADVERTISEMENT = "ADVERTISEMENT"


FEEDBACK_TYPE_MAPPING = {
    FeedbackType.QUESTION: "Вопрос",
    FeedbackType.ADVERTISEMENT: "Предложение",
}


@unique
class FeedbackStatus(StrEnum):
    NEW = "NEW"
    ARCHIVED = "ARCHIVED"


@unique
class FeedbackField(StrEnum):
    TITLE = "title"
    TEXT = "text"
    TYPE = "type"


@unique
class RegistrationField(StrEnum):
    NAME = "name"
    REGION = "region"
    PHONE = "phone"
    USER_TYPE_IDS = "user_type_ids"


@unique
class MailingStatus(StrEnum):
    SCHEDULED = "SCHEDULED"
    SENT = "SENT"
    CANCELLED = "CANCELLED"
