from aiohttp import web


async def main(req: web.Request) -> web.Response:
    print('\nrun:', __name__, 'url:', req.url)

    try:
        param = await req.json()

    except Exception as e:
        text = 'JSON error: ' + str(e)
        print(text)
        res = {'status': 400, 'data': {'error': text}}

    else:
        print('param:', param)

        try:
            print(await req['pool'].execute(f'''
                INSERT INTO sales(item_id, store_id)
                VALUES({param.get('item_id', -1)}, {param.get('store_id', -1)})
                ;
            '''))

        except Exception as e:
            text = 'SQL error: ' + str(e)
            print(text)
            res = {'status': 400, 'data': {'error': text}}

        else:
            res = await req['pool'].fetch('''
                SELECT id, sale_time::text, item_id, store_id
                FROM sales
                ORDER BY id DESC
                LIMIT 1
            ''')
            res = {'status': 200, 'data': dict(res[0])}

    return web.json_response(**res)
