from typing import Optional
from scrapy.http import Response  # type: ignore
from pathlib import Path

# Posteriormente isso vai ser carregado de outro lugar
FIXED_DOC_LINKS = {
    "portal-da-transparencia-do-governo-federal": "https://api.portaldatransparencia.gov.br/swagger-ui/index.html",
}

KEYWORDS = ["api-docs", "openapi", "rest", "docs"]
SWAGGER = "swagger"


class Utils:
    @staticmethod
    def get_base_url(url: str) -> str:
        split_url = url.split("/")

        # ['https:', '', 'teste.br', ...]
        return split_url[0] + "//" + split_url[2]

    @staticmethod
    def contains_docs_keywords(link: str) -> bool:
        return any(keyword in link.lower() for keyword in KEYWORDS)

    @staticmethod
    def contains_swagger_keyword(links: list[str]) -> list[str]:
        return [link for link in links if SWAGGER in link.lower()]

    @staticmethod
    def get_fixed_doc_link_or_none(uuid: str) -> Optional[str]:
        try:
            return FIXED_DOC_LINKS[uuid]
        except KeyError:
            return None

    @staticmethod
    def strip_nbsp(string_list: list[str]) -> list[str]:
        return [item.strip().strip("\xa0") for item in string_list if item]

    @staticmethod
    def save_html(name: str, content):
        with open(f"html/{name}.html", "w", encoding="utf-8") as file:
            file.write(content)

    @staticmethod
    def strip_and_filter_none(list: list[str]) -> list:
        return [item.strip() for item in list if item]
