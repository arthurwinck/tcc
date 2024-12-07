from typing import Union
from enum import Enum

from fastapi import APIRouter, FastAPI

from tcc.model import APIItem
from tcc.api.open_api_loader import OpenApiLoader


def create_dynamic_function(parameters, responses):
    async def endpoint_function(**kwargs):
        # Simulate logic based on parameters
        response_data = {"received": kwargs}

        # Handle responses (you could customize this further)
        example_status = next(
            iter(responses), 200
        )  # Default to the first status code or 200
        example_content = responses.get(example_status, {}).get(
            "description", "No content available."
        )

        return {
            "status_code": example_status,
            "message": example_content,
            "data": response_data,
        }

    return endpoint_function


def create_routes_from_openapi(api_item_list: list[APIItem]):
    router = APIRouter()

    for api_item in api_item_list:
        for path_item in api_item.paths:
            for endpoint in path_item.endpoints:
                parameters = endpoint.parameters
                responses = endpoint.responses

                # Map OpenAPI parameters into FastAPI's parameter system
                # fastapi_params = {}
                for param in parameters:
                    pass

                    # FIX ME

                    # param_name = param["name"]
                    # param_type = param.get("schema", {}).get("type", "string")
                    # fastapi_params[param_name] = (
                    #     str if param_type == "string" else int if param_type == "integer" else float
                    # )

                # Generate the endpoint function
                # endpoint_function = create_dynamic_function(parameters, responses)

                # Add the route
                # router.add_api_route(
                #     endpoint.path,
                #     endpoint_function,
                #     methods=[endpoint.method],
                #     summary=endpoint.summary,
                #     operation_id=endpoint.operation_id,
                # )

    return router


open_api_loader = OpenApiLoader()

open_api_loader.load()
api_item_list: list[APIItem] = open_api_loader.load()

app = FastAPI()

api_router = create_routes_from_openapi(api_item_list)

app.include_router(api_router)

# print(api_item_list)

# app = FastAPI(
#     title="Conecta API Wrapper API",
#     description="Essa api disponibiliza um wrapper para as apis disponíveis do catálogo conecta do governo federal",
#     version="1.0",
# )

# description = """
# Disponibiliza os dados publicados no Portal da Transparência do Governo Federal contendo informações sobre sobre Acordos de Leniência, Auxílio Emergencial, Benefício de Prestação Continuada (BPC), Bolsa Família, Cadastro de Expulsões da Administração Federal (CEAF), Cadastro Nacional de Empresas Inidôneas e Suspensas (CEIS), Cadastro Nacional de Empresas Punidas (CNEP), Contratos do Poder Executivo Federal, Convênios do Poder Executivo Federal, Despesas Públicas, Emendas parlamentares, Entidades Privadas sem Fins Lucrativos Impedidas (CEPIM), Garantia-Safra, Gastos por meio de cartão de pagamento, Licitações do Poder Executivo Federal, Programa de Erradicação do Trabalho Infantil (Peti), Seguro Defeso, Servidores do Poder Executivo Federal e  Viagens a serviço.
# """

# endpoint = "portal-transparencia"
# tags: list[str | Enum] | None = ["Portal Transparência"]


# @app.get(f"/{endpoint}", description=description, tags=tags)
# def read_root():
#     return {"Hello": "World"}
