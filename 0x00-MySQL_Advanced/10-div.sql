-- Create a function SafeDiv that divides the first by the
-- second number or returns 0 if the second number is equal to 0
-- SQL script to create the function:

DELIMITER //

CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS FLOAT
BEGIN
    DECLARE result FLOAT;

    IF b = 0 THEN
        SET result = 0;
    ELSE
        SET result = a / b;
    END IF;

    RETURN result;
END;
//

DELIMITER ;
