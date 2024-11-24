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


@dataclass
class APIEndpoint(Item):
    url: str
    desc: str


class APIEndpointGroup(Item):
    name: str = Field()
    endpoints: list[APIEndpoint] = Field()


class APIItem(Item):
    url: str = Field()
    auth: AuthType = Field()
    endpoint_groups: list[APIEndpointGroup] = Field()
