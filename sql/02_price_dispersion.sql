-- Price spread (max - min) by product across provinces in the sample
SELECT
  producto,
  ROUND(MIN(precio_ars_litro), 2) AS min_provincia,
  ROUND(MAX(precio_ars_litro), 2) AS max_provincia,
  ROUND(MAX(precio_ars_litro) - MIN(precio_ars_litro), 2) AS spread_ars
FROM {{TABLE}}
GROUP BY producto
ORDER BY spread_ars DESC;
