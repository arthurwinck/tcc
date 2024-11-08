from typing import Union

from fastapi import FastAPI

app = FastAPI(
    title="Conecta API Wrapper API",
    description="Essa api disponibiliza um wrapper para as apis disponíveis do catálogo conecta do governo federal",
    version="1.0",
)

description = """
Disponibiliza os dados publicados no Portal da Transparência do Governo Federal contendo informações sobre sobre Acordos de Leniência, Auxílio Emergencial, Benefício de Prestação Continuada (BPC), Bolsa Família, Cadastro de Expulsões da Administração Federal (CEAF), Cadastro Nacional de Empresas Inidôneas e Suspensas (CEIS), Cadastro Nacional de Empresas Punidas (CNEP), Contratos do Poder Executivo Federal, Convênios do Poder Executivo Federal, Despesas Públicas, Emendas parlamentares, Entidades Privadas sem Fins Lucrativos Impedidas (CEPIM), Garantia-Safra, Gastos por meio de cartão de pagamento, Licitações do Poder Executivo Federal, Programa de Erradicação do Trabalho Infantil (Peti), Seguro Defeso, Servidores do Poder Executivo Federal e  Viagens a serviço.
"""

endpoint = "portal-transparencia"
tags: list[str] = list("Portal Transparência")


@app.get(f"/{endpoint}", description=description, tags=tags)
def read_root():
    return {"Hello": "World"}
