from enum import StrEnum


class EntityType(StrEnum):
    CHARITY = "CHARITY"
    EDUCATION = "EDUCATION"
    ENROLL = "ENROLL"
    EVENT = "EVENT"
    INFORMATION = "INFORMATION"
    SUBMENU = "SUBMENU"


class FeedbackType(StrEnum):
    QUESTION = "QUESTION"
    SUGGESTION = "SUGGESTION"
