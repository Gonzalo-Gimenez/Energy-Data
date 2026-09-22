-- Quarter-over-quarter change for gasoline vs diesel (demo sample)
WITH q AS (
  SELECT
    producto,
    date_trunc('quarter', fecha)::date AS trimestre,
    AVG(precio_ars_litro) AS precio_prom
  FROM fuel_prices
  GROUP BY 1, 2
),
lagged AS (
  SELECT
    producto,
    trimestre,
    precio_prom,
    LAG(precio_prom) OVER (PARTITION BY producto ORDER BY trimestre) AS precio_prev
  FROM q
)
SELECT
  producto,
  trimestre,
  ROUND(precio_prom, 2) AS precio_promedio,
  ROUND(
    100.0 * (precio_prom - precio_prev) / NULLIF(precio_prev, 0),
    2
  ) AS variacion_pct_vs_trimestre_anterior
FROM lagged
WHERE precio_prev IS NOT NULL
ORDER BY producto, trimestre;
