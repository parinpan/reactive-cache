import redis
from psycopg2 import pool
from psycopg2.extras import RealDictCursor


class Postgres:
    conn_string = "host={} dbname={} user={} password={}"

    def __init__(self, conn):
        self.connection = pool.ThreadedConnectionPool(
            5,
            25,
            cursor_factory=RealDictCursor,
            port=conn["port"],
            keepalives=1,
            keepalives_idle=100,
            keepalives_interval=10,
            keepalives_count=10,
            dsn=Postgres.conn_string.format(conn["host"], conn["dbname"],
                                            conn["username"], conn["password"])).getconn()

    def get_connection(self):
        return self.connection


class Redis:
    def __init__(self, conn):
        self.connection = redis.Redis(host=conn["host"], port=conn["port"], db=conn["db"], decode_responses=True)

    def get_connection(self):
        return self.connection
