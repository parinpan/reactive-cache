from waitress import serve
from config import MIGRATION_PATH, DB_CONN, CACHE_CONN
from reactive_cache import migration, consumer, client, repository, web


if __name__ == '__main__':
    print("starting server...")
    
    migration.run(DB_CONN, MIGRATION_PATH)
    postgres_conn = client.Postgres(DB_CONN).get_connection()
    redis_conn = client.Redis(CACHE_CONN).get_connection()

    repo = repository.Repository(postgres_conn, redis_conn)
    profile_change_consumer = consumer.ProfileChange(postgres_conn)

    # run server
    web.dependency.repo = repo
    serve(web.app, host='0.0.0.0', port=8081, threads=250)
