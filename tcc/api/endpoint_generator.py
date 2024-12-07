from httpx import AsyncClient
from fastapi import APIRouter

from tcc.api.model import DynamicEndpoint
from tcc.model import APIItem


class EndpointGenerator:
    def create_dynamic_function(
        self, url_path: str, method: str, params: dict, responses: dict
    ) -> DynamicEndpoint:

        # Usar biblioteca de inspection para possivelmente mudar os parametros
        async def endpoint_function(**kwargs):
            async with AsyncClient() as client:

                # Mandar a requisição pra API original
                response = await client.request(
                    method=method,
                    url=url_path,
                    params=kwargs.get("query_params", {}),
                    json=kwargs.get("body", {}),
                    headers=kwargs.get("headers", {}),
                )

                return {
                    "status_code": response.status_code,
                    "message": responses.get(response.status_code, {}).get(
                        "description", "No content available."
                    ),
                    "data": response.json(),
                }

        self.set_metadata_for_function(
            endpoint_function, url_path, method, params, responses
        )

        return DynamicEndpoint(
            url_path=url_path,
            method=method,
            parameters=params,
            responses=responses,
            func=endpoint_function,
        )

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

                url_path = url + path_item.path

                # Criar cada um dos novos endpoints
                for endpoint in path_item.endpoints:
                    parameters = endpoint.parameters
                    responses = endpoint.responses

                    fastapi_params: dict[str, type] = {}

                    for param in parameters:
                        param_name = param["name"]
                        param_type = param.get("schema", {}).get("type", "string")
                        fastapi_params[param_name] = (
                            str
                            if param_type == "string"
                            else int
                            if param_type == "integer"
                            else float
                        )

                    endpoint_function = self.create_dynamic_function(
                        url_path, endpoint.method, fastapi_params, responses
                    )

                    router.add_api_route(
                        path_item.path,
                        endpoint_function,
                        methods=[endpoint.method],
                        summary=endpoint.summary,
                        operation_id=endpoint.operation_id,
                    )

            routers.append(router)

        return routers

    def set_metadata_for_function(
        self,
        endpoint_function,
        url_path: str,
        method: str,
        params: dict,
        responses: dict,
    ) -> None:
        endpoint_function.__name__ = (
            f"{method.lower()}_{url_path.strip('/').replace('/', '_')}"
        )
        endpoint_function.__doc__ = (
            f"Endpoint: {url_path}\n\n"
            f"Method: {method}\n\n"
            f"Parameters:\n{params}\n\n"
            f"Responses:\n{responses}\n"
        )
        pass
