-- SQL script to create the stored procedure ComputeAverageWeightedScoreForUsers

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers ()
BEGIN
    DECLARE user_id INT;
    DECLARE done INT DEFAULT FALSE;
    DECLARE cur CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cur;
    read_loop: LOOP
        FETCH cur INTO user_id;
        IF done THEN
            LEAVE read_loop;
        END IF;

        DECLARE total_score FLOAT DEFAULT 0;
        DECLARE total_weight FLOAT DEFAULT 0;

        -- Calculate the total weighted score for the current user
        SELECT SUM(c.score * p.weight)
        INTO total_score
        FROM corrections c
        JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = user_id;

        -- Calculate the total weight
        SELECT SUM(weight)
        INTO total_weight
        FROM projects;

        -- Calculate the average weighted score
        UPDATE users
        SET average_score = total_score / total_weight
        WHERE id = user_id;

    END LOOP;
    CLOSE cur;
END //

DELIMITER ;
