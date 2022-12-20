#! python3

from aiohttp import web
import db_asyncpg as db
import index
import items
import items_top
import stores
import stores_top
import sales

DB_KEY = 'pool'

cnt = 0  # счётчик запросов


async def create_pool(app: web.Application) -> None:
    app[DB_KEY] = await db.pool()


async def close_pool(app: web.Application) -> None:
    await app[DB_KEY].close()


async def handle(request: web.Request) -> web.Response:
    global cnt
    cnt += 1
    path = request.match_info.get('path', '')
    request['pool'] = app[DB_KEY]
    resp: web.Response | None = None

    match path, request.method:
        case '', *_: resp = await index.main(request)
        case 'items/', 'GET': resp = await items.main(request)
        case 'items/top/', 'GET': resp = await items_top.main(request)
        case 'stores/', 'GET': resp = await stores.main(request)
        case 'stores/top/', 'GET': resp = await stores_top.main(request)
        case 'sales/', 'POST': resp = await sales.main(request)
        case 'clear/', 'GET':
            await db.clear(request['pool'])
            resp = web.Response(text='Tables clear')
        case 'create/', 'GET':
            await db.create(request['pool'])
            resp = web.Response(text='Tables clear and create')
        case _: resp = await index.main(request, 404)

    # обработка Response
    if resp is None:
        resp = web.Response(status=404, text='Error')
    if resp.content_type == 'text/plain':
        resp.text += f'\n\n=== Запрос № {cnt} ===\n'

    return resp


app = web.Application()
app.router.add_route('*', '/{path:.*}', handle)
app.on_startup.append(create_pool)
app.on_cleanup.append(close_pool)
web.run_app(app)
