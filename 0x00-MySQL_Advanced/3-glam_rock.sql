-- List all bands with Glam rock as their main style,
-- ranked by their longevity SQL query to achieve this:
SELECT band_name, (IFNULL(split, 2022) - formed) AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;
