from typing import Any
from tcc.model import APIItem


class OpenAPIModifier:
    @staticmethod
    def execute(openapi_schema: dict[str, Any], api_item_list: list[APIItem]):
        for api_item in api_item_list:
            for path in api_item.paths:
                for endpoint in path.endpoints:
                    if openapi_schema["paths"].get(path.path, None):
                        endpoint_item = openapi_schema["paths"][path.path][
                            endpoint.method.lower()
                        ]

                        endpoint_item["parameters"] = endpoint.parameters
                        endpoint_item["responses"] = endpoint.responses

        # Lembrar aqui de mudar tambem o schema, adicionando os dtos faltantes. Se necessário adicionar os
        # dtos no scrape dos dados

        return openapi_schema
