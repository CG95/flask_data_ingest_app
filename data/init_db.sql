
CREATE TABLE IF NOT EXISTS sales (
  id            SERIAL NOT NULL,
  sale_id       INTEGER    NOT NULL,
  product_id    INTEGER    NOT NULL,
  product_name  VARCHAR(255) NOT NULL,
  quantity      INTEGER    NOT NULL,
  price         NUMERIC(10,2) NOT NULL,
  date          DATE  NOT NULL DEFAULT CURRENT_TIMESTAMP,
  customer_id   INTEGER    NOT NULL,
  region        VARCHAR(100) NOT NULL,
  created_at    TIMESTAMP  NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP  NOT NULL DEFAULT CURRENT_TIMESTAMP
)PARTITION BY RANGE (date);

ALTER TABLE sales
ADD COLUMN revenue NUMERIC GENERATED ALWAYS AS (price * quantity) STORED;


/*partition with year 2022*/
CREATE TABLE sales_2022 PARTITION OF sales
  FOR VALUES FROM ('2022-01-01') TO ('2023-01-01');

ALTER TABLE sales_2022
  ADD CONSTRAINT sales_2022_pkey PRIMARY KEY (id);

CREATE INDEX idx_sales_2022_date_revenue_product_id
ON sales_2022 (date, revenue DESC, product_id, product_name)
INCLUDE (quantity, price);  

CREATE INDEX idx_date_region_product_2022 ON sales_2022
  USING btree (date, region varchar_pattern_ops, product_id);

/*partition with year 2023*/
CREATE TABLE sales_2023 PARTITION OF sales
  FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');

ALTER TABLE sales_2023
  ADD CONSTRAINT sales_2023_pkey PRIMARY KEY (id);

CREATE INDEX idx_date_region_product_2023 ON sales_2023
  USING btree (date, region varchar_pattern_ops, product_id);

CREATE INDEX idx_sales_2023_date_revenue_product_id
ON sales_2023 (date, revenue DESC, product_id, product_name)
INCLUDE (quantity, price);  


/*partition with year=2024*/
CREATE TABLE sales_2024 PARTITION OF sales
  FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

ALTER TABLE sales_2024
  ADD CONSTRAINT sales_2024_pkey PRIMARY KEY (id);

CREATE INDEX idx_date_region_product_2024 ON sales_2024
  USING btree (date, region varchar_pattern_ops, product_id);

CREATE INDEX idx_sales_2024_date_revenue_product_id
ON sales_2024 (date, revenue DESC, product_id, product_name)
INCLUDE (quantity, price);  

/* Default future partition*/
CREATE TABLE sales_future PARTITION OF sales
  FOR VALUES FROM ('2025-01-01') TO (MAXVALUE);

ALTER TABLE sales_future
  ADD CONSTRAINT sales_future_pkey PRIMARY KEY (id);

CREATE INDEX idx_date_region_product_future ON sales_future
  USING btree (date, region varchar_pattern_ops, product_id);

CREATE INDEX idx_sales_future_date_revenue_product_id
ON sales_future (date, revenue DESC, product_id, product_name)
INCLUDE (quantity, price);  



/*Default partition for dates older than 2022-01-01*/
CREATE TABLE sales_past PARTITION OF sales
  FOR VALUES FROM (MINVALUE) TO ('2022-01-01');

ALTER TABLE sales_past
  ADD CONSTRAINT sales_past_pkey PRIMARY KEY (id);

CREATE INDEX idx_sales_past_date_region_product ON sales_past
  USING btree (date, region varchar_pattern_ops, product_id);

CREATE INDEX idx_sales_past_date_revenue_product_id
ON sales_future (date, revenue DESC, product_id, product_name)
INCLUDE (quantity, price);  