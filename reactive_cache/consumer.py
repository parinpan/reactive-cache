import psycopg2
import json


class ProfileChange:
    def __init__(self, db_conn):
        self.db_conn = db_conn
        self.db_conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

        cursor = self.db_conn.cursor()
        cursor.execute("LISTEN profile_change;")

        self.db_conn.commit()
        cursor.close()

    def subscribe(self, callback):
        self.db_conn.poll()
        self.db_conn.commit()

        for message in self.db_conn.notifies:
            try:
                payload = json.loads(message.payload)
                callback(payload)
            except:
                pass

        self.db_conn.notifies.clear()
