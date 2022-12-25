from aiohttp import web
from datetime import date


async def main(req: web.Request) -> web.Response:
    print('\nrun:', __name__, 'url:', req.url)

    query = req.query
    cnt = int(query.get('cnt', 10))
    mm = int(query.get('mm', date.today().month))
    gg = int(query.get('gg', date.today().year))

    res = await req['pool'].fetch(f'''
        SELECT store.*, SUM(item.price) AS income
        FROM sales
        JOIN store ON store.id = sales.store_id
        JOIN item ON item.id = sales.item_id
        WHERE to_char(sales.sale_time, 'YYYYMM') = '{gg}{mm:02}'
        GROUP BY store.id
        ORDER BY income DESC
        LIMIT {cnt}
        ;
    ''')

    return web.json_response(list(map(dict, res)))
