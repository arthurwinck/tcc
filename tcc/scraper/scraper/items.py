# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from enum import Enum
from dataclasses import dataclass
from typing import Optional
from scrapy import Item, Field  # type: ignore


class AuthType(Enum):
    NONE = 0
    API_KEY = 1


class HealthType(Enum):
    UNKNOWN = 0
    HEALTHY = 1
    UNHEALTHY = 2


@dataclass
class APIDetails(Item):
    api_name: str
    uuid: str
    orgao: str
    versao: str
    links: list[str]
    tecnologias: list[str]
    tags: list[str]
    seguranca: list[str]
    hospedagem: list[str]
    controle_de_acesso: list[str]
    docs: Optional[list[str]] = None
    health: HealthType = HealthType.UNKNOWN


@dataclass
class APIEndpoint(Item):
    url: str
    desc: str


@dataclass
class APIEndpointGroup(Item):
    name: str
    endpoints: list[APIEndpoint]


@dataclass
class APIItem(Item):
    url: str
    auth: AuthType
    endpoint_groups: list[APIEndpointGroup]
