from yoyo import step

up = """
CREATE TRIGGER publish_profile_change AFTER INSERT OR UPDATE
ON profile FOR EACH ROW EXECUTE PROCEDURE notify_profile_change();
"""

down = """
DROP TRIGGER IF EXISTS publish_profile_change;
"""

steps = [step(up, down)]
