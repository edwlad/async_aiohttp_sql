from aiohttp import web


async def main(req: web.Request) -> web.Response:
    print('run:', __name__, 'url:', req.url)

    post = await req.post()
    print('post:', post)

    return web.Response(text='Update')
