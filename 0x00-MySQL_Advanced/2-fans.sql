-- Rank country origins of bands by the number of (non-unique)
-- fans SQL query to achieve this:
SELECT origin, COUNT(*) as nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;
