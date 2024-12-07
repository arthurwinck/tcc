import json, os, requests
from typing import Generator

from tcc.model import APIEndpoint, APIPathItem, APIItem, APIServer
from tcc.utils import Utils

JSON_PATH = "../resources/json/selenium-stable.json"


class OpenApiLoader:
    def __init__(self) -> None:
        self.open_api_urls: list[dict]

    def load(self, path: str = JSON_PATH) -> list[APIItem]:
        self.load_json(path)

        api_list: list[APIItem] = list()

        for response, uuid in self.download_open_api_json():
            try:
                response_json: dict = response.json()
                api_path_list: list[APIPathItem] = self.parse_openapi_to_object(
                    response_json
                )

                servers = self.get_servers(response_json)

                if api_path_list and uuid:
                    api_list.append(
                        APIItem(paths=api_path_list, uuid=uuid, servers=servers)
                    )
            except Exception as e:
                Utils.log_error(
                    f"Erro ao decodificar resposta JSON de {uuid}, continuando. Exceção disparada: {e}"
                )

        return api_list

    def load_json(self, path: str) -> None:
        base_path = os.path.dirname(os.path.abspath(__file__))

        with open(os.path.join(base_path, path)) as file:
            self.open_api_urls = json.load(file)

    def download_open_api_json(self) -> Generator:
        for item in self.open_api_urls:
            if item["open_api_link"]:
                response = requests.get(item["open_api_link"])
                uuid: str = item["uuid"]

                if response.status_code == 200:
                    yield response, uuid
                    continue

            yield None, None

    def get_servers(self, json: dict) -> list[APIServer]:
        servers = None
        server_list: list[APIServer] = []

        try:
            servers = json.get("servers", [])
        except Exception as e:
            Utils.log_error(
                f"Erro ao recuperar Urls de servidores - convém passar as urls no webscraping. Exceção disparada: {e}"
            )

        if servers:
            for server in servers:
                server_list.append(
                    APIServer(
                        url=server.get("url", None),
                        description=server.get("description", None),
                    )
                )

        return server_list

    def parse_openapi_to_object(self, json: dict) -> list[APIPathItem]:
        paths: dict = json.get("paths", {})
        api_items: list[APIPathItem] = []

        for path, methods in paths.items():
            endpoints = []
            for method, details in methods.items():
                endpoint = APIEndpoint(
                    method=method.upper(),
                    summary=details.get("summary", ""),
                    operation_id=details.get("operationId", ""),
                    parameters=details.get("parameters", []),
                    responses=details.get("responses", {}),
                )
                endpoints.append(endpoint)
            api_items.append(APIPathItem(path=path, endpoints=endpoints))

        return api_items
