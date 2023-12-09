from collections.abc import Iterable
from datetime import date, datetime
from io import BytesIO

import httpx
from pdfplumber.pdf import PDF

from .dto import InoAgentInformationDto
from .exceptions import RegistryFileNotFoundException
from .utils import parse_actual_inoagent_registry_file_page

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


def get_ino_agent_registry_file_by_search_date(search_date: date | None = None) -> Iterable[InoAgentInformationDto]:
    """Get actual inoagent registry data."""
    if search_date is None:
        search_date = datetime.now().date()

    registry_file = _download_actual_inoagent_registry_file_by_search_date(search_date=search_date)
    pdf = PDF(registry_file)
    for page in pdf.pages:
        yield from parse_actual_inoagent_registry_file_page(page=page)
