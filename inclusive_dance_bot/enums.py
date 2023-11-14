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


@unique
class StorageType(StrEnum):
    URL = "URL"
    USER_TYPE = "USER_TYPE"
    SUBMENU = "SUBMENU"


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
