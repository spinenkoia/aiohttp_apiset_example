from typing import List

from aiohttp.web import Request, Response


async def test_handler(request: Request, ids: List[str]) -> Response:
    print(f"Received list: {ids}")

    return Response()
