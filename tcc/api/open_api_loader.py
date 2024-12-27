import json, os, requests
from typing import Generator

from tcc.model import APIEndpoint, APIPathItem, APIItem, APIServer
from tcc.utils import Utils, CACHED_API_ITEM_LIST_FILE, JSON_PATH


class OpenApiLoader:
    """
    Classe responsável por carregar as informações dos endpoints a partir dos links disponibilizados pelo webscraper

    Caso já possua as informações cacheadas, as carrega a partir do arquivo "api_item_list.json"
    """

    def __init__(self) -> None:
        self.open_api_urls: list[dict]

    def load(self, use_cached: bool = True, path: str = JSON_PATH) -> list[APIItem]:
        """
        Carrega as informações dos arquivos OpenAPI e as retorna como objetos APIItem

        Parâmetros:
            - use_cached: usa as informações cacheadas em "api_item_list.json" caso seja possível. Default = True
            - path: path para o json dos links OpenAPI, gerado pelo crawler api_selenium_spider. Default = "../resources/json/selenium-stable.json"
        """

        if use_cached:
            cached_api_list = self._load_cached()

            if cached_api_list:
                return cached_api_list

        self._load_json(path)
        return self._download_and_parse_json(use_cached)

    def _load_cached(self) -> list[APIItem] | None:
        try:
            return Utils.load_api_item_json(CACHED_API_ITEM_LIST_FILE)
        except Exception as e:
            Utils.log_error(
                f"Não foi possível carregar informações cacheadas. Exceção disparada: {e}"
            )
            return None

    def _download_and_parse_json(self, use_cached: bool) -> list[APIItem]:
        api_list: list[APIItem] = list()

        for open_api_dict in self._download_open_api_json():
            uuid = open_api_dict.get("uuid", None)
            name = open_api_dict.get("name", None)

            try:
                response_json: dict = open_api_dict["response"].json()
                api_path_list: list[APIPathItem] = self._parse_openapi_to_object(
                    response_json
                )

                servers = self._get_servers(response_json)

                if api_path_list and uuid:
                    api_list.append(
                        APIItem(
                            name=name, paths=api_path_list, uuid=uuid, servers=servers
                        )
                    )
            except Exception as e:
                Utils.log_error(
                    f"Erro ao decodificar resposta JSON de {uuid}, continuando. Exceção disparada: {e}"
                )

        if not use_cached:
            Utils.save_json(api_list, "api_item_list.json")

        return api_list

    def _load_json(self, path: str) -> None:
        base_path = os.path.dirname(os.path.abspath(__file__))

        with open(os.path.join(base_path, path)) as file:
            self.open_api_urls = json.load(file)

    def _download_open_api_json(self) -> Generator:
        for item in self.open_api_urls:
            if item["open_api_link"]:
                response = requests.get(item["open_api_link"])
                uuid: str = item["uuid"]
                name: str = item["name"]

                if response.status_code == 200:
                    yield {"response": response, "uuid": uuid, "name": name}
                    continue

            yield None

    def _get_servers(self, json: dict) -> list[APIServer]:
        servers = None
        server_list: list[APIServer] = []

        servers = json.get("servers", [])

        if servers:
            for server in servers:
                server_list.append(
                    APIServer(
                        url=server.get("url", None),
                        description=server.get("description", None),
                    )
                )

        return server_list

    def _parse_openapi_to_object(self, json: dict) -> list[APIPathItem]:
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
