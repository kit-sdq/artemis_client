from typing import Any, AsyncGenerator, Callable, Coroutine

from aiohttp.client_reqrep import ClientResponse


async def paginate_json(
    request_function: Callable[[str, dict], Coroutine[Any, Any, ClientResponse]],
    api_endpoint: str,
    http_params={},
    page_size: int = 50,
    **args
) -> AsyncGenerator[Any, None]:
    http_params["page"] = 0
    http_params["pageSize"] = page_size
    while True:
        resp = await request_function(api_endpoint, params=http_params, **args)
        resp_list = await resp.json()
        if not resp_list:
            break
        for obj in resp_list:
            yield obj
        http_params["page"] = http_params["page"] + 1
