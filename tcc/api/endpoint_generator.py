from fastapi import APIRouter

from tcc.api.dynamic_function_creator import DynamicFunctionCreator
from tcc.api.model import DynamicEndpoint
from tcc.model import APIItem, APIPathItem


class EndpointGenerator:
    def _testing_return_endpoints(
        self, api_item_list: list[APIItem]
    ) -> list[DynamicEndpoint]:
        endpoint_list: list[DynamicEndpoint] = []

        for api_item in api_item_list:
            router = APIRouter()

            if not api_item.servers:
                continue

            url = api_item.servers[0].url

            for path_item in api_item.paths:
                test_endpoint = self._iterate_and_set_endpoints(
                    url, path_item, api_item.uuid, router
                )
                endpoint_list.extend(test_endpoint)

        return endpoint_list

    def create_routes_from_openapi(
        self, api_item_list: list[APIItem]
    ) -> list[APIRouter]:
        routers: list[APIRouter] = []

        for api_item in api_item_list:
            router = APIRouter()

            if not api_item.servers:
                continue

            url = api_item.servers[0].url

            for path_item in api_item.paths:
                self._iterate_and_set_endpoints(url, path_item, api_item.uuid, router)

            routers.append(router)

        return routers

    def _iterate_and_set_endpoints(
        self, url: str, path_item: APIPathItem, uuid: str, router: APIRouter
    ) -> list[DynamicEndpoint]:
        url_path = url + path_item.path
        endpoints: list[DynamicEndpoint] = []

        # Criar cada um dos novos endpoints
        for endpoint in path_item.endpoints:
            parameters = endpoint.parameters
            responses = endpoint.responses

            fastapi_params: dict[str, type] = {}

            for param in parameters:
                param_name = param["name"]
                param_type = param.get("schema", {}).get("type", "string")
                fastapi_params[param_name] = param_type == "string"

            endpoint_function = DynamicFunctionCreator._create_dynamic_function(
                url_path,
                endpoint.method,
                fastapi_params,
                responses,
                uuid,
                path_item.path,
            )

            endpoints.append(endpoint_function)

            router.add_api_route(
                path_item.path,
                endpoint_function,
                methods=[endpoint.method],
                summary=endpoint.summary,
                operation_id=endpoint.operation_id,
            )

        return endpoints