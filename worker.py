import asyncio
from waitress import serve
from config import MIGRATION_PATH, DB_CONN, CACHE_CONN
from reactive_cache import migration, consumer, client, repository

if __name__ == '__main__':
    print("starting worker...")
    
    migration.run(DB_CONN, MIGRATION_PATH)
    postgres_conn = client.Postgres(DB_CONN).get_connection()
    redis_conn = client.Redis(CACHE_CONN).get_connection()

    repo = repository.Repository(postgres_conn, redis_conn)
    profile_change_consumer = consumer.ProfileChange(postgres_conn)

    # run a postgres' notify consumer
    loop = asyncio.get_event_loop()
    loop.add_reader(postgres_conn, profile_change_consumer.subscribe, repo.store_profile_cache)
    loop.run_forever()
