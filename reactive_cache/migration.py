from yoyo import read_migrations
from yoyo import get_backend


def run(conn, migration_path):
    conn_str = "postgres://{}:{}@{}:{}/{}".format(conn["username"], conn["password"], conn["host"], conn["port"], conn["dbname"])
    backend = get_backend(conn_str)
    migrations = read_migrations(migration_path)

    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))
        backend.commit()
