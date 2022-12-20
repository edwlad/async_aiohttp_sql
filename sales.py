from aiohttp import web


async def main(req: web.Request) -> web.Response:
    post = await req.post()
    print('run:', __name__, 'url:', req.url, 'post:', post)

    try:
        await req['pool'].execute(f'''
            INSERT INTO sales(item_id, store_id)
            VALUES({post.get('item_id', -1)}, {post.get('store_id', -1)})
            ;
        ''')
        res = await req['pool'].fetch('''
            SELECT id, sale_time::text, item_id, store_id
            FROM sales
            ORDER BY id DESC
            LIMIT 1
        ''')
        res = {'status': 200, 'data': dict(res[0])}
    except Exception as e:
        res = {'status': 400, 'data': {'error': str(e)}}

    return web.json_response(**res)
