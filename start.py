#! python3

from aiohttp import web
import index
import items
import items_top
import stores
import stores_top
import sales

cnt = 0  # счётчик запросов


async def handle(request: web.Request) -> web.Response:
    global cnt
    cnt += 1
    path = request.match_info.get('path', '')
    resp: web.Response | None = None

    request['db'] = 'Connect DB'  # добавление параметров соединения с базой данных

    match path, request.method:
        case '', *_: resp = await index.main(request)
        case 'items/', 'GET': resp = await items.main(request)
        case 'items/top/', 'GET': resp = await items_top.main(request)
        case 'stores/', 'GET': resp = await stores.main(request)
        case 'stores/top/', 'GET': resp = await stores_top.main(request)
        case 'sales/', 'POST': resp = await sales.main(request)
        case _: resp = await index.main(request, 404)

    # обработка Response
    if resp is None:
        resp = web.Response(status=404, charset='utf-8')
    if resp.content_type == 'text/plain':
        resp.text += f'\n\n=== Запрос № {cnt} ===\n'

    return resp


app = web.Application()
app.router.add_route('*', '/{path:.*}', handle)
web.run_app(app)
