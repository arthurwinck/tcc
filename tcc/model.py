from enum import Enum
from dataclasses import dataclass, field
from typing import Optional


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
    path: str
    method: str
    summary: str
    operation_id: str
    parameters: list[str] = field(default_factory=list)
    responses: dict = field(default_factory=dict)


@dataclass
class APIPathItem:
    path: str
    endpoints: list[APIEndpoint]


@dataclass
class APIItem:
    uuid: str
    paths: list[APIPathItem]
