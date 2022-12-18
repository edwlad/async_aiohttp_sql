from aiohttp import web


async def main(rec: web.Request, status: int = 200) -> web.Response:
    print(__name__)
    return web.Response(
        status=status,
        text=f'Run script: {__name__}'
    )