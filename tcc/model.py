from enum import Enum
from dataclasses import dataclass, field
from typing import Optional

# Scraping models -----------------------------
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
    name: str
    uuid: str
    api_docs: APIDocs


@dataclass
class APIDetails:
    name: str
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


# API Loading models -----------------------------


@dataclass
class APIEndpoint:
    method: str
    summary: str
    operation_id: str
    parameters: list[dict] = field(default_factory=list)
    responses: dict = field(default_factory=dict)

    def __str__(self):
        return (
            f"APIEndpoint(method={self.method}, summary={self.summary}, "
            f"operation_id={self.operation_id}, parameters={self.parameters}, responses={self.responses})"
        )


@dataclass
class APIPathItem:
    path: str
    endpoints: list[APIEndpoint]

    def __str__(self):
        endpoints_str = ", ".join(str(endpoint) for endpoint in self.endpoints)
        return f"APIPathItem(path={self.path}, endpoints=[{endpoints_str}])"


@dataclass
class APIServer:
    url: str
    description: Optional[str]


@dataclass
class APIItem:
    uuid: str
    name: str
    paths: list[APIPathItem]
    servers: list[APIServer]

    def __str__(self):
        paths_str = ", ".join(str(path_item) for path_item in self.paths)
        return f"APIItem(uuid={self.uuid}, paths=[{paths_str}])"
