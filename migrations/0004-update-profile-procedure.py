from yoyo import step

up = """
CREATE PROCEDURE update_profile_counter(given_username varchar(50), action varchar(50)) 
LANGUAGE plpgsql AS $$
    DECLARE 
        affected_rows integer;
    BEGIN
        CASE action
            WHEN 'inc_followings' THEN 
                UPDATE profile SET followings_count = followings_count + 1 WHERE username = given_username;
                GET DIAGNOSTICS  affected_rows = ROW_COUNT;
            WHEN 'inc_followers' THEN
                UPDATE profile SET followers_count = followers_count + 1 WHERE username = given_username;
                GET DIAGNOSTICS  affected_rows = ROW_COUNT;
            WHEN 'inc_likes' THEN
                UPDATE profile SET likes_count = likes_count + 1 WHERE username = given_username;
                GET DIAGNOSTICS  affected_rows = ROW_COUNT;
        END CASE;
        
        IF affected_rows = 0 THEN
            CASE action
                WHEN 'inc_followings' THEN 
                    INSERT INTO profile(username, followings_count, followers_count, likes_count)
                        VALUES(given_username, 1, 0, 0);
                WHEN 'inc_followers' THEN
                    INSERT INTO profile(username, followings_count, followers_count, likes_count)
                        VALUES(given_username, 0, 1, 0);
                WHEN 'inc_likes' THEN
                    INSERT INTO profile(username, followings_count, followers_count, likes_count)
                        VALUES(given_username, 0, 0, 1);
            END CASE;
        END IF;
    END
$$
"""

down = """
DROP PROCEDURE update_profile_counter;
"""

steps = [step(up, down)]
