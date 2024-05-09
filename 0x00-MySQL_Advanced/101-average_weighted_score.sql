-- SQL script to create the stored procedure ComputeAverageWeightedScoreForUsers

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE total_weighted_score FLOAT;
    DECLARE total_weight FLOAT;
    DECLARE user_id_value INT;
    DECLARE project_weight INT;
    DECLARE project_score FLOAT;

    -- Initialize variables
    SET total_weighted_score = 0;
    SET total_weight = 0;

    -- Cursor to iterate through users
    DECLARE user_cursor CURSOR FOR
        SELECT id FROM users;
    
    -- Cursor to iterate through projects
    DECLARE project_cursor CURSOR FOR
        SELECT project_id, score FROM corrections WHERE user_id = user_id_value;

    -- Declare handlers
    DECLARE CONTINUE HANDLER FOR NOT FOUND
        SET done = TRUE;

    -- Start loop for users
    OPEN user_cursor;
    user_loop: LOOP
        FETCH user_cursor INTO user_id_value;
        IF done THEN
            LEAVE user_loop;
        END IF;

        -- Reset total_weight for each user
        SET total_weight = 0;

        -- Start loop for projects
        OPEN project_cursor;
        project_loop: LOOP
            FETCH project_cursor INTO project_id, project_score;
            IF done THEN
                LEAVE project_loop;
            END IF;

            -- Get the weight of the project
            SELECT weight INTO project_weight FROM projects WHERE id = project_id;

            -- Update the total weighted score for the user
            SET total_weighted_score = total_weighted_score + (project_score * project_weight);
            SET total_weight = total_weight + project_weight;
        END LOOP project_loop;

        -- Close the cursor
        CLOSE project_cursor;

        -- Calculate the average weighted score and update the users table
        IF total_weight > 0 THEN
            UPDATE users SET average_score = total_weighted_score / total_weight WHERE id = user_id_value;
        ELSE
            UPDATE users SET average_score = 0 WHERE id = user_id_value;
        END IF;
    END LOOP user_loop;

    -- Close the cursor
    CLOSE user_cursor;
END //

DELIMITER ;
