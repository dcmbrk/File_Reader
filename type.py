from enum import StrEnum, auto

class Type(StrEnum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name.upper()

    INVOICE = auto()