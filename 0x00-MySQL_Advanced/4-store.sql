-- Create a trigger that decreases the quantity of an
-- item after adding a new order SQL script to create the trigger:
DELIMITER //

CREATE TRIGGER update_item_quantity AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END;
//

DELIMITER ;
