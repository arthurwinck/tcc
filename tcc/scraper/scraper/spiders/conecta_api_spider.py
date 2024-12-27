import re
from typing import Generator
from scrapy import Spider  # type: ignore
from scrapy.http import Response  # type: ignore

from tcc.model import APIDetails, APIDocs
from tcc.utils import SWAGGER, Utils  # type: ignore


class ConectaApiSpider(Spider):
    name = "conecta_api_spider"

    start_urls = ["https://www.gov.br/conecta/catalogo/"]

    def parse(self, response: Response) -> Generator:
        for api_card in response.css(".apis .row a"):
            name = api_card.css("p::text").get()
            api_link = api_card.attrib["href"]

            yield response.follow(
                api_link,
                self.parse_api_details,
                meta={"name": name, "api_link": api_link},
            )

    def parse_api_details(self, response: Response):
        name = response.meta["api_name"]
        api_link = response.meta["api_link"]

        uuid = self.get_uuid(api_link)
        orgao, versao = self.extract_orgao_and_versao(response)
        links = self.extract_links(response)

        item = APIDetails(
            name=name,
            uuid=uuid,
            orgao=orgao,
            versao=versao,
            links=links,
            docs=self.find_doc_link(uuid, links),
            tecnologias=self.extract_tecnologias(response),
            tags=self.extract_tags(response),
            seguranca=self.get_str_list_from_card_id("seguranca", response),
            hospedagem=self.get_str_list_from_card_id("hospedagem", response),
            controle_de_acesso=self.get_str_list_from_card_id(
                "controle-de-acesso", response
            ),
        )

        yield item

    def find_doc_link(self, uuid: str, links: list[str]) -> APIDocs:
        fixed_doc_link = Utils.get_fixed_doc_link_or_none(
            uuid
        )  # Dicionário de links de docs que não estão presentes no catalógo da API

        if fixed_doc_link:
            links.insert(0, fixed_doc_link)

        swagger_links: list[str] = []
        custom_links: list[str] = []

        for link in links:
            # Teste de links para checarmos se possuimos uma documentacao de api
            if SWAGGER in link:
                swagger_links.append(link)
            elif Utils.contains_docs_keywords(link):
                custom_links.append(link)

        return APIDocs(swagger_links, custom_links)

    def extract_orgao_and_versao(self, response: Response) -> tuple[str, str]:
        orgao_versao_list: list[str] = response.css(".order-md-2 p::text").getall()

        try:
            if len(orgao_versao_list) < 3:
                orgao = orgao_versao_list[1]
                versao = "Não informado"
            else:
                orgao, versao = orgao_versao_list[-2:]
        except ValueError:
            orgao, versao = "Não informado", "Não informado"

        return orgao, versao

    def extract_links(self, response: Response) -> list[str]:
        endpoints = response.css(
            ".content.detalhamento-tecnico .api-endpoint-producao span::text"
        ).getall()
        endpoints_and_docs = response.css(
            ".detalhamento-tecnico * a::attr(href)"
        ).getall()

        if endpoints_and_docs:
            endpoints.extend(endpoints_and_docs)

        return Utils.strip_and_filter_none(endpoints)

    def extract_tecnologias(self, response: Response) -> list[str]:
        tecnologias = response.css(
            "#tecnologias .br-card .front .content .conteudo::text"
        ).getall()
        return Utils.strip_nbsp(tecnologias)

    def extract_tags(self, response: Response) -> list[str]:
        tags_list = self.get_str_list_from_card_id("tags", response)

        cleaned_tags: set[str] = set()
        for raw_tag in tags_list:
            matches = re.findall(r"#([^#]+)", raw_tag)
            cleaned_tags.update(Utils.strip_and_filter_none(matches))
        return list(cleaned_tags)

    def get_uuid(self, api_link: str) -> str:
        reversed_url = api_link[::-1]
        return reversed_url[: reversed_url.find("/")][::-1]

    def get_str_list_from_card_id(self, id: str, response: Response) -> list[str]:
        item_list = response.css(
            f"#{id} .br-card .front .content p::text, #{id} .br-card .front .content div::text"
        ).getall()[1:]
        return Utils.strip_nbsp(item_list)
