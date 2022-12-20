from aiohttp import web


async def main(req: web.Request) -> web.Response:
    print('run:', __name__, 'url:', req.url)

    res = await req['pool'].fetch("SELECT * FROM item")

    return web.json_response(list(map(dict, res)))
