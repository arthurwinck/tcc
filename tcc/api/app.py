import asyncio, pytest
from typing import Callable, Dict
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from tcc.api import endpoint_generator
from tcc.api.dynamic_function_creator import DynamicFunctionCreator
from tcc.api.model import DynamicEndpoint
from tcc.api.open_api_json_modifier import OpenAPIModifier
from tcc.model import APIItem
from tcc.api.open_api_loader import OpenApiLoader
from tcc.api.endpoint_generator import EndpointGenerator

loader = OpenApiLoader()
generator = EndpointGenerator()

api_item_list: list[APIItem] = loader.load(use_cached=False)

# Generator transforma a lista de APIITems em endpoints (funções) criadas dinamicamente.
generator = EndpointGenerator()

routers = generator.create_routers_from_openapi(api_item_list)

app = FastAPI()

for router in routers:
    app.include_router(router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="API Wrapper do Catálogo Conecta",
        version="0.1.0",
        summary="API Wrapper gerada automaticamente a partir do Catálogo Conecta GOV.BR. Uso do Projeto Céos ",
        description="""
            Todos os endpoints fornecidos aqui foram gerados automaticamente a paritr de um processo de extração de dados,
            transformação desses dados capturados em endpoints dinâmicos e posteriormente fornecidos aqui.
            """,
        routes=app.routes,
    )

    app.openapi_schema = OpenAPIModifier.execute(openapi_schema, api_item_list)
    return app.openapi_schema


app.openapi = custom_openapi  # type: ignore
