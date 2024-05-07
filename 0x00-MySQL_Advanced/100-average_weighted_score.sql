-- SQL script to create the stored procedure ComputeAverageWeightedScoreForUser

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser (IN user_id INT)
BEGIN
    DECLARE total_score FLOAT DEFAULT 0;
    DECLARE total_weight FLOAT DEFAULT 0;

    -- Calculate the total weighted score
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

END //

DELIMITER ;
