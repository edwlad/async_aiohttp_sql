from aiohttp import web
from datetime import date


async def main(req: web.Request) -> web.Response:
    print('run:', __name__, 'url:', req.url)

    cnt = int(req.query.get('cnt', 10))
    mm = int(req.query.get('mm', date.today().month))

    res = await req['pool'].fetch(f'''
        SELECT
            st.*,
            ROUND(SUM(it.price)*100)/100 AS income
        FROM sales AS sa, store AS st, item AS it
        WHERE st.id = sa.store_id
            AND it.id = sa.item_id
            AND extract(month from sa.sale_time) = {mm}
        GROUP BY sa.sale_time, st.id
        ORDER BY income DESC
        LIMIT {cnt}
        ;
    ''')

    return web.json_response([dict(v.items()) for v in res])
