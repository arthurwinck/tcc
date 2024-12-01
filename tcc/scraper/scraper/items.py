from enum import Enum
from dataclasses import dataclass
from typing import Optional


class AuthType(Enum):
    NONE = 0
    API_KEY = 1


class HealthType(Enum):
    UNKNOWN = 0
    HEALTHY = 1
    UNHEALTHY = 2


@dataclass
class APIDocs:
    swagger_links: list[str]
    custom_links: list[str]


@dataclass
class API2ParseDto:
    uuid: str
    api_docs: APIDocs


@dataclass
class APIDetails:
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
    docs: Optional[APIDocs] = None
    health: int = HealthType.UNKNOWN.value


@dataclass
class APIEndpoint:
    endpoint: str
    desc: str


@dataclass
class APIEndpointGroup:
    name: str
    endpoints: list[APIEndpoint]


@dataclass
class APIItem:
    url: str
    auth: AuthType
    endpoint_groups: list[APIEndpointGroup]
