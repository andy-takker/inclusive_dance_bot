from enum import StrEnum, unique


@unique
class EntityType(StrEnum):
    CHARITY = "CHARITY"
    EDUCATION = "EDUCATION"
    ENROLL = "ENROLL"
    EVENT = "EVENT"
    INFORMATION = "INFORMATION"
    SUBMENU = "SUBMENU"


@unique
class FeedbackType(StrEnum):
    QUESTION = "QUESTION"
    ADVERTISEMENT = "ADVERTISEMENT"


@unique
class StorageType(StrEnum):
    URL = "URL"
    USER_TYPE = "USER_TYPE"
    ENTITY = "ENTITY"
