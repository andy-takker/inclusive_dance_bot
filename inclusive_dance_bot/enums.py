from enum import StrEnum, unique


@unique
class SubmenuType(StrEnum):
    CHARITY = "CHARITY"
    EDUCATION = "EDUCATION"
    ENROLL = "ENROLL"
    EVENT = "EVENT"
    INFORMATION = "INFORMATION"
    OTHER = "SUBMENU"


@unique
class FeedbackType(StrEnum):
    QUESTION = "QUESTION"
    ADVERTISEMENT = "ADVERTISEMENT"


@unique
class StorageType(StrEnum):
    URL = "URL"
    USER_TYPE = "USER_TYPE"
    SUBMENU = "SUBMENU"
