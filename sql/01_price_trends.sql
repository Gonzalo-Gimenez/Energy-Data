-- Monthly average posted price by product (national)
SELECT
  date_trunc('month', fecha)::date AS mes,
  producto,
  ROUND(AVG(precio_ars_litro), 2) AS precio_promedio_ars
FROM fuel_prices
GROUP BY 1, 2
ORDER BY 1, 2;
