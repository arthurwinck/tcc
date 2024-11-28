import re
from typing import Generator, Optional
from scrapy import Spider  # type: ignore
from scrapy.http import Response  # type: ignore
from scrapy_selenium import SeleniumRequest

from tcc.scraper.scraper.items import APIDetails
from ..utils import get_fixed_doc_link_or_none, strip_nbsp


class ConectaApiSpider(Spider):
    name = "conecta-api"

    start_urls = ["https://www.gov.br/conecta/catalogo/"]

    def parse(self, response: Response) -> Generator:
        for api_card in response.css(".apis .row a"):
            api_name = api_card.css("p::text").get()
            api_link = api_card.attrib["href"]

            # https://docs.scrapy.org/en/latest/intro/tutorial.html#following-links
            yield response.follow(
                api_link,
                self.parse_api_details,
                meta={"api_name": api_name, "api_link": api_link},
            )

    def parse_api_details(self, response: Response):
        api_name = response.meta["api_name"]
        api_link = response.meta["api_link"]

        uuid = self.get_uuid(api_link)
        orgao, versao = self.extract_orgao_and_versao(response)

        item = APIDetails(
            api_name=api_name,
            uuid=uuid,
            orgao=orgao,
            versao=versao,
            links=self.extract_links(response),
            tecnologias=self.extract_tecnologias(response),
            tags=self.extract_tags(response),
            seguranca=self.get_str_list_from_card_id("seguranca", response),
            hospedagem=self.get_str_list_from_card_id("hospedagem", response),
            controle_de_acesso=self.get_str_list_from_card_id(
                "controle-de-acesso", response
            ),
        )

        self.extract_and_set_docs(response, item)

    def find_doc_link(self, item: APIDetails) -> Optional[str]:
        doc_link_to_extract: Optional[str] = None

        if not item.links:
            # Dicionário de links de docs que não estão presentes no catalógo da API
            return get_fixed_doc_link_or_none(item.uuid)

        # Iterar sobre os links e tentar buscar o link para a documentação
        for link in item.links:
            pass

        return None

    def extract_and_set_docs(self, response: Response, item: APIDetails):
        # Provavelmente aqui vou precisar dar um response.follow para tentar acessar os links das APIs e verificar se as
        # existe algo que diga que é uma documentação de api

        doc_link = self.find_doc_link(item)

        yield SeleniumRequest(
            url=doc_link,
            callback=self.extract_api_info,
            wait_time=5,
            meta={"item": item, "response": response},
        )

    def extract_api_info(self, response: Response):
        # TODO - Agora nós precisamos acessar o site da API. Por enquanto temos alguns tipos de documentação
        # 1 - Swagger, com o link padrão apontado pelo base url ou por um select field
        # 2 - Próprio, é necessário procurar pelo link na seção de exemplos ou algo do gênero
        pass

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

        return [endpoint.strip() for endpoint in endpoints if endpoint]

    def extract_tecnologias(self, response: Response) -> list[str]:
        tecnologias = response.css(
            "#tecnologias .br-card .front .content .conteudo::text"
        ).getall()
        return strip_nbsp(tecnologias)

    def extract_tags(self, response: Response) -> list[str]:
        tags_list = self.get_str_list_from_card_id("tags", response)

        cleaned_tags: set[str] = set()
        for raw_tag in tags_list:
            matches = re.findall(r"#([^#]+)", raw_tag)
            cleaned_tags.update(tag.strip() for tag in matches)
        return list(cleaned_tags)

    def get_uuid(self, api_link: str) -> str:
        reversed_url = api_link[::-1]
        return reversed_url[: reversed_url.find("/")][::-1]

    def get_str_list_from_card_id(self, id: str, response: Response) -> list[str]:
        item_list = response.css(
            f"#{id} .br-card .front .content p::text, #{id} .br-card .front .content div::text"
        ).getall()[1:]
        return strip_nbsp(item_list)
