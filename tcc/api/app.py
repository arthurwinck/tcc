from fastapi import FastAPI
from tcc.api import endpoint_generator
from tcc.model import APIItem
from tcc.api.open_api_loader import OpenApiLoader
from tcc.api.endpoint_generator import EndpointGenerator

loader = OpenApiLoader()

loader.load()
api_item_list: list[APIItem] = loader.load()

generator = EndpointGenerator()

routers = generator.create_routes_from_openapi(api_item_list)

app = FastAPI()

app = FastAPI(
    title="Conecta API Wrapper API",
    description="Essa api disponibiliza um wrapper para as apis disponíveis do catálogo conecta do governo federal",
    version="1.0",
)

for router in routers:
    app.include_router(router)

# api_router = create_routes_from_openapi(api_item_list)

# app.include_router(api_router)

# print(api_item_list)

# description = """
# Disponibiliza os dados publicados no Portal da Transparência do Governo Federal contendo informações sobre sobre Acordos de Leniência, Auxílio Emergencial, Benefício de Prestação Continuada (BPC), Bolsa Família, Cadastro de Expulsões da Administração Federal (CEAF), Cadastro Nacional de Empresas Inidôneas e Suspensas (CEIS), Cadastro Nacional de Empresas Punidas (CNEP), Contratos do Poder Executivo Federal, Convênios do Poder Executivo Federal, Despesas Públicas, Emendas parlamentares, Entidades Privadas sem Fins Lucrativos Impedidas (CEPIM), Garantia-Safra, Gastos por meio de cartão de pagamento, Licitações do Poder Executivo Federal, Programa de Erradicação do Trabalho Infantil (Peti), Seguro Defeso, Servidores do Poder Executivo Federal e  Viagens a serviço.
# """

# endpoint = "portal-transparencia"
# tags: list[str | Enum] | None = ["Portal Transparência"]


# @app.get(f"/{endpoint}", description=description, tags=tags)
# def read_root():
#     return {"Hello": "World"}
