from yoyo import step

up = """
CREATE PROCEDURE update_profile_counter(given_username varchar(50), action varchar(50)) 
LANGUAGE plpgsql AS $$
    BEGIN
        CASE action
            WHEN 'inc_followings' THEN 
                UPDATE profile SET followings_count = followings_count + 1 WHERE username = given_username;
            WHEN 'inc_followers' THEN
                UPDATE profile SET followers_count = followers_count + 1 WHERE username = given_username;
            WHEN 'inc_likes' THEN
                UPDATE profile SET likes_count = likes_count + 1 WHERE username = given_username;
        END CASE;
    END
$$
"""

down = """
DROP PROCEDURE update_profile_counter;
"""

steps = [step(up, down)]
