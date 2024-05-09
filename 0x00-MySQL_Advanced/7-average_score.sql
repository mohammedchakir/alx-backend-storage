-- Create a stored procedure ComputeAverageScoreForUser that
-- computes and stores the average score for a student
-- SQL script to create the stored procedure:
DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE total_projects INT;
    DECLARE average FLOAT;

    SELECT SUM(score) INTO total_score
    FROM corrections
    WHERE user_id = user_id;

    SELECT COUNT(*) INTO total_projects
    FROM corrections
    WHERE user_id = user_id;

    IF total_projects > 0 THEN
        SET average = total_score / total_projects;
    ELSE
        SET average = 0;
    END IF;

    UPDATE users
    SET average_score = average
    WHERE id = user_id;
END;
//

DELIMITER ;
