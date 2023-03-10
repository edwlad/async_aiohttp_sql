import asyncpg
from random import randint
from datetime import date

DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASS = ''
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


async def clear(pool):
    await pool.execute('DROP TABLE IF EXISTS sales CASCADE')
    await pool.execute('DROP TABLE IF EXISTS item')
    await pool.execute('DROP TABLE IF EXISTS store')

    await pool.execute('''
        CREATE TABLE store (
            id serial PRIMARY KEY,
            address VARCHAR
        );
    ''')

    await pool.execute('''
        CREATE TABLE item (
            id serial PRIMARY KEY,
            name varchar,
            price integer
        );
    ''')
    await pool.execute('''
        CREATE TABLE sales (
            id serial PRIMARY KEY,
            sale_time timestamp NOT NULL DEFAULT 'now()',
            item_id integer REFERENCES item (id),
            store_id integer REFERENCES store (id)
        );
    ''')


async def create(pool):
    await clear(pool)

    await pool.execute(
        "INSERT INTO store (address) "
        + "VALUES ("
        + "), (".join(f"'store-{v+1}'" for v in range(50))
        + ");"
    )

    await pool.execute(
        "INSERT INTO item (name, price) "
        + "VALUES ("
        + "), (".join(f"'item-{v+1}', {randint(100, 10000)}" for v in range(50))
        + ");"
    )

    gg = date.today().year
    for mm in range(1, 13):
        await pool.execute(
            "INSERT INTO sales (sale_time, item_id, store_id) "
            + "VALUES ("
            + "), (".join(
                f"'{gg}-{mm:02}-{randint(1, 28):02}'::timestamp, {randint(1, 50)}, {randint(1, 50)}"
                for _ in range(300))
            + ");"
        )
