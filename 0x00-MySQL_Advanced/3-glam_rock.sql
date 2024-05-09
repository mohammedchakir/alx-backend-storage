-- List all bands with Glam rock as their main style,
-- ranked by their longevity SQL query to achieve this:
SELECT band_name, 
       IF(split IS NOT NULL AND formed IS NOT NULL, 2022 - YEAR(formed), 0) AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;
