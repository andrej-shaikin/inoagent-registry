from collections.abc import Iterable
from datetime import date, datetime
from io import BytesIO

import httpx
from pdfplumber.pdf import PDF, Page
from pydash.strings import clean

from .dto import InoAgentInformationDto
from .exceptions import RegistryFileNotFoundException

__all__ = [
    "get_ino_agent_registry_file_by_search_date",
]


def _download_actual_inoagent_registry_file_by_search_date(search_date: date | None = None) -> BytesIO:
    """Get inoagent registry file by search date or current date."""
    if search_date is None:
        search_date = datetime.now()

    search_date = search_date.strftime("%d%m%Y")
    resp = httpx.get(
        url=f"https://minjust.gov.ru/uploaded/files/reestr-inostrannyih-agentov-{search_date}.pdf",
        verify=False,
    )
    if resp.status_code == 404:
        raise RegistryFileNotFoundException(f"Registry file was not found on the requested date {search_date}")
    return BytesIO(resp.content)


def _parse_actual_inoagent_registry_file_page(page: Page) -> Iterable[InoAgentInformationDto]:
    """Parse actual inoagent registry file page."""
    rows = iter(page.extract_table())
    # skip table header
    next(rows)
    for row in rows:
        (
            _,
            name,
            birthday,
            ogrn,
            inn,
            registration_number,
            snils,
            address,
            information_resource,
            full_name,
            grounds_for_inclusion,
            decision_inclusion_date,
            decision_exclusion_date,
        ) = row

        if birthday:
            birthday = datetime.strptime(birthday, "%d.%m.%Y")
        if full_name:
            full_name = [
                clean(word)
                for word in full_name.strip().split(";")
            ]
        if information_resource:
            information_resource = [
                clean(resource)
                for resource in information_resource.strip().split(";")
            ]
        if decision_inclusion_date:
            decision_inclusion_date = datetime.strptime(decision_inclusion_date, "%d.%m.%Y")
        if decision_exclusion_date:
            decision_exclusion_date = datetime.strptime(decision_exclusion_date, "%d.%m.%Y")

        yield InoAgent(
            name=clean(name),
            birthday=birthday or None,
            ogrn=ogrn or None,
            inn=inn or None,
            registration_number=registration_number and clean(registration_number) or None,
            snils=snils and clean(snils) or None,
            address=address and clean(address) or None,
            information_resource=information_resource or None,
            full_name=full_name or None,
            grounds_for_inclusion=grounds_for_inclusion and clean(grounds_for_inclusion) or None,
            decision_inclusion_date=decision_inclusion_date or None,
            decision_exclusion_date=decision_exclusion_date or None,
        )


def get_ino_agent_registry_file_by_search_date(search_date: date | None = None) -> Iterable[InoAgentInformationDto]:
    """Get actual inoagent registry data."""
    if search_date is None:
        search_date = datetime.now().date()

    registry_file = _download_actual_inoagent_registry_file_by_search_date(search_date=search_date)
    pdf = PDF(registry_file)
    for page in pdf.pages[::-1]:
        yield from _parse_actual_inoagent_registry_file_page(page=page)
