from enum import StrEnum


class PolicyType(StrEnum):
    AUTO = "AUTO"
    HOME = "HOME"
    LIFE = "LIFE"
    HEALTH = "HEALTH"
    TRAVEL = "TRAVEL"
    BUSINESS = "BUSINESS"


class PolicyStatus(StrEnum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    CANCELED = "CANCELED"
    PENDING = "PENDING"
    LAPSED = "LAPSED"


class PaymentFrequency(StrEnum):
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    SEMI_ANNUAL = "SEMI_ANNUAL"
    ANNUAL = "ANNUAL"
    ONE_TIME = "ONE_TIME"


class PaymentMethod(StrEnum):
    CREDIT_CARD = "CREDIT_CARD"
    BANK_TRANSFER = "BANK_TRANSFER"
    CHECK = "CHECK"
    CASH = "CASH"
    PAYPAL = "PAYPAL"
