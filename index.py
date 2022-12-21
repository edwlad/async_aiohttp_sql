from aiohttp import web


async def main(req: web.Request, status: int = 200) -> web.Response:
    print('\nrun:', __name__, 'url:', req.url)

    return web.Response(
        status=status,
        text=f'Home page.\n\nRun script: {__name__}, status code {status}'
    )
