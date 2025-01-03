import asyncio
import os

from requests import Request
from tcc.api.endpoint_generator import EndpointGenerator
from tcc.api.model import DynamicEndpoint
from tcc.api.open_api_loader import OpenApiLoader
from tcc.model import APIItem
from tcc.utils import Utils

PORTAL_TRANSPARENCIA_KEY = os.environ.get("PORTAL_TRANSPARENCIA_KEY", None)

PORTAL_TRANSPARENCIA_GOV_UUID = "portal-da-transparencia-do-governo-federal"
PORTAL_TRANSPARENCIA_GOV_FUNC_ID = "get_portal-da-transparencia-do-governo-federal_api-de-dados_contratos_id"

def testing_portal_transparencia_endpoint(endpoint: DynamicEndpoint):
    if not PORTAL_TRANSPARENCIA_KEY:
        Utils.log_error("Não é possível resgatar chave do portal da transparência. Adicione uma chave como variável de ambiente")
        return

    codigo_orgao = "52111"
    data_inicial = "01/01/2018"

    params = {"id": "668113639", "codigoOrgao": codigo_orgao, "quantidade": 100, "dataInicial": data_inicial, "pagina": 1}
    headers = {"accept": "*/*", "chave-api-dados": PORTAL_TRANSPARENCIA_KEY}

    # response = requests.get(endpoint.url_path, params=params, headers=headers)
    # print(response.status_code)

    response = asyncio.run(endpoint.func(Request(method="get", headers=headers, params=params)))
    print(response)

loader = OpenApiLoader()
api_item_list: list[APIItem] = loader.load(use_cached=True)

# Generator transforma a lista de APIITems em endpoints (funções) criadas dinamicamente. Como isso é experimental
generator = EndpointGenerator()

# Production purposes
# routers = generator.create_routes_from_openapi(api_item_list)
# Testing purposes
testing_endpoints = generator._testing_return_endpoints_dict(api_item_list)

portal_transparencia_gov: dict[str, DynamicEndpoint] = testing_endpoints[PORTAL_TRANSPARENCIA_GOV_UUID]

testing_portal_transparencia_endpoint(portal_transparencia_gov[PORTAL_TRANSPARENCIA_GOV_FUNC_ID])