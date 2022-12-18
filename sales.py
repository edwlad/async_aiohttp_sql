from aiohttp import web


async def main(rec: web.Request) -> web.Response:
    print(__name__)
    return web.Response(
        text=f'Run script: {__name__}'
    )
