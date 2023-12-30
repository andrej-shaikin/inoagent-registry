import re
from collections.abc import Iterable
from datetime import date, datetime
from io import BytesIO

import httpx
from bs4 import BeautifulSoup, Tag
from pdfplumber.pdf import PDF

from .dto import InoAgentInformationDto
from .exceptions import RegistryFileNotFoundException
from .utils import parse_actual_inoagent_registry_file_page

__all__ = [
    "get_ino_agent_registry_file_by_search_date",
    "get_actual_inoagent_registry_file_date",
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


def get_actual_inoagent_registry_file_date() -> date:
    """Get actual inoagent registry file date."""
    resp = httpx.get(
        url="https://minjust.gov.ru/ru/activity/directions/998/",
        verify=False,
    )
    if resp.status_code != 200:
        raise ValueError
    soup = BeautifulSoup(resp.content, "lxml")
    tag: None | Tag = soup.select_one("#section-description > div > ul > li:nth-child(2) > a")
    if tag is None:
        raise ValueError
    return datetime.strptime(re.search(r"\d{8}", tag.get("href")).group(0), "%d%m%Y").date()


def get_ino_agent_registry_file_by_search_date(search_date: date | None = None) -> Iterable[InoAgentInformationDto]:
    """Get actual inoagent registry data."""
    if search_date is None:
        search_date = datetime.now().date()

    registry_file = _download_actual_inoagent_registry_file_by_search_date(search_date=search_date)
    pdf = PDF(registry_file)
    for page in pdf.pages:
        yield from parse_actual_inoagent_registry_file_page(page=page)
