import asyncio
import signal
import threading
from reactive_cache import migration, consumer, client, repository, web

MIGRATION_PATH = "migrations/"

CACHE_CONN = {
    "host": "66.42.59.156",
    "port": 6379,
    "db": 0
}

DB_CONN = {
    "host": "localhost",
    "port": 5433,
    "username": "postgres",
    "password": "",
    "dbname": "twitter_clone"
}


def run_funcs(funcs):
    for func in funcs:
        func()


if __name__ == '__main__':
    migration.run(DB_CONN, MIGRATION_PATH)
    postgres_conn = client.Postgres(DB_CONN).get_connection()
    redis_conn = client.Redis(CACHE_CONN).get_connection()

    repo = repository.Repository(postgres_conn, redis_conn)
    profile_change_consumer = consumer.ProfileChange(postgres_conn)

    # run a web server
    web.dependency.repo = repo
    threading.Thread(target=web.app.run, daemon=True, kwargs={"host": "localhost",
                                                              "port": 8081,
                                                              "debug": False,
                                                              "threaded": True,
                                                              "use_reloader": False}).start()

    # run a postgres' notify consumer
    loop = asyncio.get_event_loop()
    loop.add_reader(postgres_conn, profile_change_consumer.subscribe, repo.store_profile_cache)

    loop.add_signal_handler(signal.SIGINT, lambda: run_funcs([loop.stop, postgres_conn.close, redis_conn.close]))
    loop.run_forever()
