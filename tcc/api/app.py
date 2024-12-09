import asyncio, pytest
from typing import Callable, Dict
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from tcc.api import endpoint_generator
from tcc.api.dynamic_function_creator import DynamicFunctionCreator
from tcc.model import APIItem
from tcc.api.open_api_loader import OpenApiLoader
from tcc.api.endpoint_generator import EndpointGenerator
from tcc.utils import Utils

loader = OpenApiLoader()

api_item_list: list[APIItem] = loader.load(use_cached=True)

# Generator transforma a lista de APIITems em endpoints (funções) criadas dinamicamente. Como isso é experimental
generator = EndpointGenerator()

# # routers = generator.create_routes_from_openapi(api_item_list)

# DynamicEndpoint(
#   url_path='https://api.portaldatransparencia.gov.br/api-de-dados/acordos-leniencia/{id}',
#   method='GET',
#   parameters={'id': False},
#   responses={'400': {'description': 'Bad Request', 'content': {'*/*': {'schema': {'type': 'object'}}}}, '401': {'description': 'Unauthorized', 'content': {'*/*': {'schema': {'type': 'object'}}}}, '500': {'description': 'Internal Server Error', 'content': {'*/*': {'schema': {'type': 'object'}}}}, '200': {'description': 'OK', 'content': {'*/*': {'schema': {'$ref': '#/components/schemas/AcordosLenienciaDTO'}}}}},
#   func=get_https:__api.portaldatransparencia.gov.br_api-de-dados_acordos-leniencia_{id}
# )

# DynamicEndpoint(
#   uuid='cep-codigo-de-enderecamento-postal',
#   url_path='https://h-apigateway.conectagov.estaleiro.serpro.gov.br/api-cep/v1/consulta/cep/{cep}',
#   method='GET',
#   parameters={'x-cpf-usuario': True, 'cep': True},
#   responses={'200': {'description': 'Retorna os dados de endereço do referentes ao CEP', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/ConsultaCep'}}}}, '400': {'description': 'CEP inválido.'}, '404': {'description': 'CEP não encontrado'}, '500': {'description': 'Erros do backend e/ou dos servidores de dados'}},
#   func=get_cep-codigo-de-enderecamento-postal_consulta_cep_by_cep
# )

testing_endpoints = generator._testing_return_endpoints(api_item_list)

for endpoint in testing_endpoints:
    if endpoint.uuid == "cep-codigo-de-enderecamento-postal":
        response = asyncio.run(endpoint.func(params={"cep": 1}))
        print(response)

    # if "cep" in endpoint.path:
    #     print(endpoint)
    # response = asyncio.run(endpoint.func(params={"id": 1}))


# app = FastAPI()

# for router in routers:
#     app.include_router(router)

# Utils.save_json(app.openapi(), "openapi_schema.json")

# {
#     "openapi": "3.1.0",
#     "info": {
#         "title": "FastAPI",
#         "version": "0.1.0"
#     },
#     "paths": {
#         "/items/": {
#             "get": {
#                 "responses": {
#                     "200": {
#                         "description": "Successful Response",
#                         "content": {
#                             "application/json": {


# def add_paths_to_openapi(openapi_schema: dict, api_item_list: list[APIItem]):
#     for api in api_item_list:
#         for path in api.paths:
#             openapi_schema["paths"][path.path] = {

#             }

# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema
#     openapi_schema = get_openapi(
#         title="Custom title",
#         version="2.5.0",
#         summary="This is a very custom OpenAPI schema",
#         description="Here's a longer description of the custom **OpenAPI** schema",
#         routes=app.routes,
#     )


#     app.openapi_schema = openapi_schema
#     return app.openapi_schema


# app.openapi = custom_openapi #type: ignore
