from aiohttp import web
from datetime import date


async def main(req: web.Request) -> web.Response:
    print('\nrun:', __name__, 'url:', req.url)

    cnt = int(req.query.get('cnt', 10))
    mm = int(req.query.get('mm', date.today().month))

    res = await req['pool'].fetch(f'''
        SELECT store.*, SUM(item.price) AS income
        FROM sales, store, item
        WHERE store.id = sales.store_id
            AND item.id = sales.item_id
            AND extract(month from sales.sale_time) = {mm}
        GROUP BY store.id
        ORDER BY income DESC
        LIMIT {cnt}
        ;
    ''')

    return web.json_response(list(map(dict, res)))
