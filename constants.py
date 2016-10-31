import enum


class MarketType(enum.Enum):
    COEFFICIENT = "Coefficient"
    PARAMETRIC = "Parametric"


class EvaluationStatus(enum.Enum):
    NEW = 0
    ACCEPTED = 1
    RESOLVED = 2
    KILLED = 3


class Result(enum.Enum):
    NULL = 0
    HOME_WIN = 1
    AWAY_WIN = 2
    DRAW = 3
    NOT_PLAYED = 4
