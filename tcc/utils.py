from dataclasses import asdict, is_dataclass
import os, json
from typing import Optional, TypeAlias
from scrapy.http import Response  # type: ignore
from pathlib import Path

# Posteriormente isso vai ser carregado de outro lugar
FIXED_DOC_LINKS = {
    "portal-da-transparencia-do-governo-federal": "https://api.portaldatransparencia.gov.br/swagger-ui/index.html",
}

KEYWORDS = ["api-docs", "openapi", "rest", "docs"]
SWAGGER = "swagger"

Json: TypeAlias = list | dict


class Utils:
    @staticmethod
    def log_error(msg: str):
        print("-----------------------------")
        print(f"ERROR - {msg}")
        print("-----------------------------")

    @staticmethod
    def transform_to_json_compliant(data: Json):
        json_data = None

        if is_dataclass(data):
            json_data = asdict(data)
        else:
            try:
                json_data = [asdict(obj) for obj in data]
            except:
                Utils.log_error(
                    "Tipo não permitido para conversão de Dataclass em JSON"
                )

        return json_data

    @staticmethod
    def save_json(content: Json, filename: str, path: str = "resources/json"):
        json_data = Utils.transform_to_json_compliant(content)

        base_path = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(base_path, path)

        os.makedirs(path, exist_ok=True)

        file_path = os.path.join(folder_path, filename)

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(json_data, file)

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
