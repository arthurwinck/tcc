from typing import Callable


class DynamicEndpoint:
    def __init__(
        self,
        path: str,
        uuid: str,
        url_path: str,
        method: str,
        parameters: dict,
        responses: dict,
        func: Callable,
    ):
        self.path = path
        self.uuid = uuid
        self.url_path = url_path
        self.method = method
        self.parameters = parameters
        self.responses = responses
        self.func = func

    def __str__(self):
        return (
            f"DynamicEndpoint(\n"
            f"  uuid='{self.uuid}',\n"
            f"  url_path='{self.url_path}',\n"
            f"  method='{self.method}',\n"
            f"  parameters={self.parameters},\n"
            f"  responses={self.responses},\n"
            f"  func={self.func.__name__ if hasattr(self.func, '__name__') else str(self.func)}\n"
            f")"
        )

    async def __call__(self, **kwargs):
        return await self.func(**kwargs)

    @property
    def __name__(self):
        return self.func.__name__ if hasattr(self.func, "__name__") else "Unknown"

    @property
    def __docs__(self):
        return self.func.__name__ if hasattr(self.func, "__docs__") else "Unknown"
