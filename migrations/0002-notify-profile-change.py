from yoyo import step

up = """
CREATE OR REPLACE FUNCTION notify_profile_change() RETURNS TRIGGER AS $$
    BEGIN
        PERFORM pg_notify('profile_change', row_to_json(NEW)::text);
        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;
"""

down = """
DROP FUNCTION IF EXISTS notify_profile_change;
"""

steps = [step(up, down)]
