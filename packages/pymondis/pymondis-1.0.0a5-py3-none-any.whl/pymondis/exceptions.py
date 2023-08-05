from enum import Enum
from typing import Type


class NotFullyImplementedWarning(UserWarning):
    pass


class RevoteError(Exception):
    def __init__(self, category: str):
        super().__init__("Próbowałeś zagłosować na kategorię '{}' drugi raz".format(category))


class NoEnumMatchError(Exception):
    def __init__(self, enum: Type[Enum], value):
        super().__init__("Nie znaleziono żadnych pasujących elementów w {} dla wartości: {}".format(enum, value))
