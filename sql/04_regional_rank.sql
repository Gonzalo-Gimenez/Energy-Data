-- Top provinces by latest-month average price per product
WITH latest AS (
  SELECT MAX(fecha) AS max_fecha FROM {{TABLE}}
),
last_month AS (
  SELECT f.*
  FROM {{TABLE}} AS f
  CROSS JOIN latest AS l
  WHERE DATE_TRUNC(f.fecha, MONTH) = DATE_TRUNC(l.max_fecha, MONTH)
)
SELECT
  producto,
  provincia,
  ROUND(AVG(precio_ars_litro), 2) AS precio_promedio_ultimo_mes
FROM last_month
GROUP BY producto, provincia
ORDER BY producto, precio_promedio_ultimo_mes DESC;
