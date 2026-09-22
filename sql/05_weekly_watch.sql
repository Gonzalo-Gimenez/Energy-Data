-- Weekly national basket vs prior week (operations desk watch)
WITH weekly AS (
  SELECT
    DATE_TRUNC(fecha, WEEK(MONDAY)) AS semana,
    producto,
    AVG(precio_ars_litro) AS precio_prom
  FROM {{TABLE}}
  GROUP BY semana, producto
),
lagged AS (
  SELECT
    semana,
    producto,
    precio_prom,
    LAG(precio_prom) OVER (PARTITION BY producto ORDER BY semana) AS precio_sem_ant
  FROM weekly
)
SELECT
  semana,
  producto,
  ROUND(precio_prom, 2) AS precio_promedio_semana,
  ROUND(
    100.0 * (precio_prom - precio_sem_ant) / NULLIF(precio_sem_ant, 0),
    2
  ) AS variacion_pct_wow,
  CASE
    WHEN ABS(
      100.0 * (precio_prom - precio_sem_ant) / NULLIF(precio_sem_ant, 0)
    ) >= 2.0 THEN 'ALERTA'
    ELSE 'OK'
  END AS estado_control
FROM lagged
WHERE precio_sem_ant IS NOT NULL
ORDER BY semana DESC, producto;
