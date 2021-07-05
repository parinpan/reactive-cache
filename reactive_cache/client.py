import psycopg2
import redis
from psycopg2.extras import RealDictCursor


class Postgres:
    conn_string = "host={} dbname={} user={} password={}"

    def __init__(self, conn):
        self.connection = psycopg2.connect(
            cursor_factory=RealDictCursor,
            keepalives=1,
            keepalives_idle=5,
            keepalives_interval=2,
            keepalives_count=2,
            connect_timeout=3,
            port=conn["port"],
            dsn=Postgres.conn_string.format(conn["host"], conn["dbname"],
                                            conn["username"], conn["password"])
        )

    def get_connection(self):
        return self.connection


class Redis:
    def __init__(self, conn):
        self.connection = redis.Redis(host=conn["host"], port=conn["port"], db=conn["db"], decode_responses=True)

    def get_connection(self):
        return self.connection
