-- Create an index idx_name_first_score on the table
-- names and the first letter of name and the score
-- SQL script to create the index:
CREATE INDEX idx_name_first_score ON names(name(1), score);
