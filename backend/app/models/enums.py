from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    STUDENT = "student"


class QuestionType(str, Enum):
    FILL_BLANK = "fill_blank"
    CODE_OUTPUT = "code_output"
    SHORT_ANSWER = "short_answer"
