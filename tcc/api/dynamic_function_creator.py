import re
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

        async def endpoint_function(**kwargs):
            url = url_path

            for param_key in list(params.keys()):
                if param_key in list(kwargs["params"].keys()):
                    to_replace = "{" + param_key + "}"
                    url = url.replace(to_replace, str(kwargs["params"][param_key]))

            params_to_request = kwargs.get("params", {})
            json_to_request = kwargs.get("body", None)
            headers_to_request = kwargs.get("headers", {})

            async with AsyncClient() as client:
                response = await client.request(
                    method=method,
                    url=url,
                    params=params_to_request,
                    json=json_to_request,
                    headers=headers_to_request,
                )

            if response.status_code != 200:
                data = f"Error {response.status_code}"
            else:
                data = response.json()

            return {
                "status_code": response.status_code,
                "data": data,
                "parameters": kwargs.get("params", {}),
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
