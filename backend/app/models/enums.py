from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    STUDENT = "student"


class QuestionType(str, Enum):
    FILL_BLANK = "fill_blank"
    CODE_OUTPUT = "code_output"
    SHORT_ANSWER = "short_answer"


class LessonStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class SubmissionStatus(str, Enum):
    RECEIVED = "received"
    ACCEPTED = "accepted"
    WRONG_ANSWER = "wrong_answer"
    RUNTIME_ERROR = "runtime_error"
    TIME_LIMIT_EXCEEDED = "time_limit_exceeded"
