-- Top provinces by latest-month average price per product
WITH latest AS (
    SELECT MAX(fecha) AS max_fecha FROM fuel_prices
),
last_month AS (
    SELECT f.*
    FROM fuel_prices f
    CROSS JOIN latest l
    WHERE date_trunc('month', f.fecha) = date_trunc('month', l.max_fecha)
)
SELECT
    producto,
    provincia,
    ROUND(AVG(precio_ars_litro), 2) AS precio_promedio_ultimo_mes
FROM last_month
GROUP BY producto, provincia
ORDER BY producto, precio_promedio_ultimo_mes DESC;
