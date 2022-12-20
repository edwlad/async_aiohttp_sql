from aiohttp import web


async def main(req: web.Request) -> web.Response:
    print('run:', __name__, 'url:', req.url)

    cnt = int(req.query.get('cnt', 10))
    res = await req['pool'].fetch(f'''
        SELECT item.id, item.name, COUNT(sales.id) AS sales_amount
        FROM sales, item
        WHERE item.id = sales.item_id
        GROUP BY item.id
        ORDER BY sales_amount DESC
        LIMIT {cnt}
        ;
    ''')

    return web.json_response(list(map(dict, res)))
