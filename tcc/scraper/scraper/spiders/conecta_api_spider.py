from pathlib import Path
from typing import Generator, Any
from scrapy import Spider, Request  # type: ignore

from ..utils import strip_nbsp


class ConectaApiSpider(Spider):
    name = "conecta-api"

    start_urls = ["https://www.gov.br/conecta/catalogo/"]

    def parse(self, response) -> Generator:
        page = response.url.split("/")[-2]

        for api_card in response.css(".apis .row a"):
            api_name = api_card.css("p::text").get()
            api_link = api_card.attrib["href"]

            # yield {"api_name": api_name, "api_link": api_link}

            # https://docs.scrapy.org/en/latest/intro/tutorial.html#following-links
            yield response.follow(
                api_link,
                self.parse_api_details,
                meta={"api_name": api_name, "api_link": api_link},
            )

        self.save_html(page, response)

    def parse_api_details(self, response: Request) -> Generator:
        api_name = response.meta["api_name"]
        api_link = response.meta["api_link"]
        orgao, versao = self.extract_orgao_and_versao(response)

        item = {
            "nome": api_name,
            "link": api_link,
            "orgao": orgao,
            "versao": versao,
            "descricao": "\n".join(response.css("#descricao p::text").getall()),
            "endpoints": self.extract_endpoints(response),
            "tecnologias": self.extract_tecnologias(response),
            "tags": self.get_str_list_from_card_id("tags", response),
            "seguranca": self.get_str_list_from_card_id("seguranca", response),
            "hospedagem": self.get_str_list_from_card_id("hospedagem", response),
            "controle-de-acesso": self.get_str_list_from_card_id(
                "controle-de-acesso", response
            ),
            "como-acessar-api": {
                "indique-interesse": self.extract_como_acessar_api(response),
                "preencha-adesao": self.extract_preencha_adesao(response),
                "recebimento-resultado": self.extract_recebimento_resultado(response),
            },
        }

        yield item

    def extract_como_acessar_api(self, response: Request) -> str:
        return ""

    def extract_preencha_adesao(self, response: Request) -> str:
        return ""

    def extract_recebimento_resultado(self, response: Request) -> str:
        return ""

    def extract_orgao_and_versao(self, response: Request) -> tuple[str, str]:
        return response.css(".order-md-2 p::text").getall()[1:3]

    # Acho que extract endpoints pode receber além de endpoints, pode vir algo como documentação
    def extract_endpoints(self, response: Request) -> list[str]:
        endpoints = response.css(
            ".content.detalhamento-tecnico .api-endpoint-producao span::text"
        ).getall()
        endpoints_and_docs = response.css(
            ".detalhamento-tecnico * a::attr(href)"
        ).getall()

        if endpoints_and_docs:
            endpoints.extend(endpoints_and_docs)

        return [endpoint.strip() for endpoint in endpoints if endpoint]

    def extract_tecnologias(self, response: Request) -> list[str]:
        tecnologias = response.css(
            "#tecnologias .br-card .front .content .conteudo::text"
        ).getall()
        return strip_nbsp(tecnologias)

    def get_str_list_from_card_id(self, id: str, response: Request) -> list[str]:
        item_list = response.css(
            f"#{id} .br-card .front .content p::text, #{id} .br-card .front .content div::text"
        ).getall()[1:]
        return strip_nbsp(item_list)

    def save_html(self, page, response) -> None:
        filename = f"{page}.html"

        file_path = Path(f"html/{filename}")

        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_bytes(response.body)

        self.log(f"Saved file {filename}")
