-- Analytic warehouse table (same grain as the public CSV)
CREATE TABLE IF NOT EXISTS fuel_prices (
    fecha DATE NOT NULL,
    producto TEXT NOT NULL,
    provincia TEXT NOT NULL,
    precio_ars_litro NUMERIC(10, 2) NOT NULL
);

CREATE INDEX IF NOT EXISTS fuel_prices_fecha_idx ON fuel_prices (fecha);
CREATE INDEX IF NOT EXISTS fuel_prices_producto_idx ON fuel_prices (producto);
