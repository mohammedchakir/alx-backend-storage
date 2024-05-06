-- List all bands with Glam rock as their main style,
-- ranked by their longevity SQL query to achieve this:
SELECT band_name, YEAR(FROM_UNIXTIME(splitted[2])) - formed as lifespan
FROM metal_bands
WHERE main_style = 'Glam rock'
ORDER BY lifespan DESC;
