import json


class Repository:
    _profile_cache_key_fmt = "{}_profile"

    def __init__(self, db_conn, cache_conn):
        self.db_conn = db_conn
        self.cache_conn = cache_conn

    def increase_counter(self, username, counter_action):
        cursor = self.db_conn.cursor()
        query = "CALL update_profile_counter(%s, %s);"
        cursor.execute(query, (username, counter_action,))
        cursor.close()

    def store_profile_cache(self, profile):
        key = self._profile_cache_key_fmt.format(profile["username"])
        self.cache_conn.set(key, json.dumps(profile))
        print("key of {} was successfully cached...".format(key))

    def get_profile_cache(self, username):
        key = self._profile_cache_key_fmt.format(username)
        data = self.cache_conn.get(key)
        return json.loads(data) if data else {}
