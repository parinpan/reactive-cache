from yoyo import step

up = """
CREATE OR REPLACE FUNCTION notify_profile_change() RETURNS TRIGGER AS $$
    BEGIN
        IF tg_op = 'UPDATE' OR tg_op = 'INSERT' THEN
            PERFORM pg_notify('profile_change', row_to_json(NEW)::text);
        ELSEIF tg_op = 'DELETE' THEN
            PERFORM pg_notify('profile_change', concat('{"username":"', OLD.username, '"}')::text);
        END IF;
        
        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;
"""

down = """
DROP FUNCTION IF EXISTS notify_profile_change;
"""

steps = [step(up, down)]
