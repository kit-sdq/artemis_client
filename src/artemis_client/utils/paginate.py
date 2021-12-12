from typing import Any, AsyncGenerator, Protocol

from aiohttp.client_reqrep import ClientResponse

from artemis_client.utils.serialize import loads


class _RequestFunctionType(Protocol):
    async def __call__(self, api_endpoint: str, **kwargs) -> ClientResponse:
        ...


async def paginate_json(
    get_function: _RequestFunctionType,
    api_endpoint: str,
    http_params={},
    page_size: int = 50,
    max_pages: int = 0,
    **kwargs
) -> AsyncGenerator[Any, None]:
    http_params["page"] = 0
    http_params["pageSize"] = page_size
    while not max_pages or http_params["page"] <= max_pages:
        resp = await get_function(api_endpoint, params=http_params, **kwargs)
        resp_list = await resp.json(loads=loads)
        if not resp_list:
            break
        for obj in resp_list:
            yield obj
        http_params["page"] = http_params["page"] + 1
