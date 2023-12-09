from collections.abc import Iterable
from datetime import date
from typing import NamedTuple

__all__ = [
    "InoAgentInformationDto",
]


class InoAgentInformationDto(NamedTuple):
    name: str
    grounds_for_inclusion: str
    address: str | None = None
    birthday: date | None = None
    full_name: Iterable[str] | None = None
    inn: str | None = None
    ogrn: str | None = None
    decision_inclusion_date: date | None = None
    decision_exclusion_date: date | None = None
    information_resource: Iterable[str] = None
    registration_number: str | None = None
    snils: str | None = None
