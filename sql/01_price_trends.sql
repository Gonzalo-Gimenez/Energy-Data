-- Monthly average posted price by product (national)
SELECT
  DATE_TRUNC(fecha, MONTH) AS mes,
  producto,
  ROUND(AVG(precio_ars_litro), 2) AS precio_promedio_ars
FROM {{TABLE}}
GROUP BY mes, producto
ORDER BY mes, producto;
