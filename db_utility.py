import asyncpg

DB_NAME = 'course'
DB_USER = 'postgres'
DB_PASS = 'postgres'
DB_HOST = 'localhost'
DB_PORT = '5432'


async def pool():
    return await asyncpg.create_pool(
        database=DB_NAME,
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASS
    )


async def cursor(conn: asyncpg.Pool, sql: str):
    return await conn.cursor(sql)


async def fetch(conn: asyncpg.Pool, sql: str):
    return await conn.fetch(sql)


async def close(val: asyncpg.Pool):
    return await val.close()


async def create():
    _pool: asyncpg.Pool = await pool()
    await _pool.execute('DROP TABLE IF EXISTS sales CASCADE')
    await _pool.execute('DROP TABLE IF EXISTS item')
    await _pool.execute('DROP TABLE IF EXISTS store')

    await _pool.execute('''
        CREATE TABLE store (
            id serial PRIMARY KEY,
            address VARCHAR
        );
    ''')
    await _pool.execute('''
        CREATE TABLE item (
            id serial PRIMARY KEY,
            name VARCHAR,
            price float
        );
    ''')
    await _pool.execute('''
        CREATE TABLE sales (
            id serial PRIMARY KEY,
            sale_time timestamp NOT NULL DEFAULT 'now()',
            item_id integer REFERENCES item (id),
            store_id integer REFERENCES store (id)
        );
    ''')

    await close(_pool)
