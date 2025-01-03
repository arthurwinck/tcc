import requests
import uvicorn
import os
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.testclient import TestClient
from tcc.api.endpoint_generator import EndpointGenerator
from tcc.api.open_api_json_modifier import OpenAPIModifier
from tcc.api.open_api_loader import OpenApiLoader
from tcc.model import APIItem
from tcc.utils import Utils

PORTAL_TRANSPARENCIA_KEY = os.environ.get("PORTAL_TRANSPARENCIA_KEY", None)

PORTAL_TRANSPARENCIA_GOV_UUID = "portal-da-transparencia-do-governo-federal"
PORTAL_TRANSPARENCIA_GOV_FUNC_ID = "get_portal-da-transparencia-do-governo-federal_api-de-dados_contratos_id"

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

client = TestClient(app)

def testing_portal_transparencia_endpoint():
    if not PORTAL_TRANSPARENCIA_KEY:
        Utils.log_error("Não é possível resgatar chave do portal da transparência. Adicione uma chave como variável de ambiente")
        return

    codigo_orgao = "52111"
    data_inicial = "01/01/2018"

    params = {"id": "668113639", "codigoOrgao": codigo_orgao, "quantidade": 100, "dataInicial": data_inicial, "pagina": 1}
    headers = {"accept": "*/*", "chave-api-dados": PORTAL_TRANSPARENCIA_KEY}

    response = requests.get("/api-de-dados/contratos", params=params, headers=headers)
    print(response.status_code)

    # response = asyncio.run(endpoint.func(headers=headers, params=params))
    # print(response)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
    testing_portal_transparencia_endpoint()

