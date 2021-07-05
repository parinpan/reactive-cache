from yoyo import step

up = """
CREATE TABLE profile (
    username VARCHAR(50) PRIMARY KEY,
    followings_count INT NOT NULL DEFAULT 0,
    followers_count INT NOT NULL DEFAULT 0,
    likes_count INT NOT NULL DEFAULT 0 
)
"""

down = """
DROP TABLE IF EXISTS profile;
"""

steps = [step(up, down)]
