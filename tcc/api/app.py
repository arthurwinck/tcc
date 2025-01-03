import asyncio, pytest
from typing import Callable, Dict
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from tcc.api import endpoint_generator
from tcc.api.dynamic_function_creator import DynamicFunctionCreator
from tcc.api.model import DynamicEndpoint
from tcc.model import APIItem
from tcc.api.open_api_loader import OpenApiLoader
from tcc.api.endpoint_generator import EndpointGenerator

loader = OpenApiLoader()
generator = EndpointGenerator()

api_item_list: list[APIItem] = loader.load(use_cached=False)

for api_item in api_item_list:
    print(api_item.name)

# Generator transforma a lista de APIITems em endpoints (funções) criadas dinamicamente.
generator = EndpointGenerator()

# routers = generator.create_routers_from_openapi(api_item_list)
dict = generator._testing_return_endpoints_dict(api_item_list)

# for key, value in dict.items():
#     for skey, svalue in value.items():
#         print(svalue)

# app = FastAPI(title="API Wrapper do Catálogo Conecta")

# for router in routers:
#     app.include_router(router)
