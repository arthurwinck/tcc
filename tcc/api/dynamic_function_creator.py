import re
from fastapi import Request
from httpx import AsyncClient
from tcc.api.model import DynamicEndpoint

class DynamicFunctionCreator:
    
    @staticmethod
    def _create_dynamic_function(
        url_path: str,
        method: str,
        params: dict,
        responses: dict,
        uuid: str,
        only_path: str,
    ) -> DynamicEndpoint:

        async def endpoint_function(request: Request):
            # Adicionar validação para parâmetros

            url = url_path

            try:
                if request.path_params:
                    url = url.format(**request.path_params)
            except:
                return {
                    "status_code": 400,
                    "data": "400 - Bad request. API Wrapper não pôde adicionar parâmetros de path e query.",
                    "url": url,
                }
            
            try:                
                json_to_request = await request.json()
            except:
                json_to_request = None

            async with AsyncClient() as client:
                print(request.query_params)
                print(request.headers)

                response = await client.request(
                    method=method,
                    url=url,
                    params=dict(request.query_params),
                    json=json_to_request,
                    headers=dict(request.headers),
                )

            if response.status_code != 200:
                data = f"Error {response.status_code}"
            else:
                data = response.json()

            return {
                "status_code": response.status_code,
                "data": data,
                "url": url,
            }

        DynamicFunctionCreator._set_metadata_for_function(
            endpoint_function, url_path, method, params, responses, uuid, only_path
        )

        return DynamicEndpoint(
            path=only_path,
            uuid=uuid,
            url_path=url_path,
            method=method,
            parameters=params,
            responses=responses,
            func=endpoint_function,
        )
    
    @staticmethod
    def replace_placeholders(text: str):
        pattern = r"\{([^}]+)\}"

        return re.sub(pattern, lambda match: f"by_{match.group(1)}", text)

    @staticmethod
    def _set_metadata_for_function(
        endpoint_function,
        url_path: str,
        method: str,
        params: dict,
        responses: dict,
        uuid: str,
        only_path: str,
    ) -> None:
        new_path_name = DynamicFunctionCreator.replace_placeholders(
            only_path.strip("/").replace("/", "_")
        )

        endpoint_function.__name__ = f"{method.lower()}_{uuid}_{new_path_name}"
        endpoint_function.__doc__ = (
            f"Endpoint: {url_path}\n\n"
            f"Method: {method}\n\n"
            f"Parameters:\n{params}\n\n"
            f"Responses:\n{responses}\n"
        )
        pass
