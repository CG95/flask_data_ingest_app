



## Performance optimization on Analytical query on sales by date range, region and product_id

# Query only using date range and region filters

EXPLAIN (ANALYZE,BUFFERS) SELECT region, product_id, product_name, SUM(price* quantity) as total_revenue
FROM sales
Where date between '20230101' AND '20230531' AND region LIKE 'KOREA%'
GROUP BY region, product_id, product_name

                                                                                QUERY PLAN                              
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 GroupAggregate  (cost=7437.78..7438.32 rows=18 width=66) (actual time=9.452..9.453 rows=0 loops=1)
   Group Key: sales.region, sales.product_id, sales.product_name
   Buffers: shared hit=1152
   ->  Sort  (cost=7437.78..7437.83 rows=18 width=44) (actual time=9.450..9.451 rows=0 loops=1)
         Sort Key: sales.region, sales.product_id, sales.product_name
         Sort Method: quicksort  Memory: 25kB
         Buffers: shared hit=1152
         ->  Index Scan using idx_date_region_product_2023 on sales_2023 sales  (cost=0.42..7437.40 rows=18 width=44) (actual time=9.442..9.443 rows=0 loops=1)
               Index Cond: ((date >= '2023-01-01'::date) AND (date <= '2023-05-31'::date) AND ((region)::text ~>=~ 'KOREA'::text) AND ((region)::text ~<~ 'KOREB'::text))
               Filter: ((region)::text ~~ 'KOREA%'::text)
               Buffers: shared hit=1152
 Planning:
   Buffers: shared hit=5
 Planning Time: 0.319 ms
 Execution Time: 9.497 ms
(15 rows)





#====================================================================================
# Query optimization of monthly sales of a given year


#Initial query
EXPLAIN (ANALYZE,BUFFERS) SELECT
            DATE_TRUNC('month', date) AS month,
            SUM(quantity) AS total_quantity,
            SUM(price * quantity) AS total_revenue
        FROM sales
        WHERE EXTRACT(YEAR FROM date)=2023
        GROUP BY month
        ORDER BY month


                                                                    QUERY PLAN                                    
---------------------------------------------------------------------------------------------------------------------------------------------------------------
---
 Finalize GroupAggregate  (cost=19198.15..19435.01 rows=730 width=48) (actual time=204.910..234.899 rows=12 loops=1)
   Group Key: (date_trunc('month'::text, (sales.date)::timestamp with time zone))
   Buffers: shared hit=12243 read=282, temp read=1503 written=1508
   ->  Gather Merge  (cost=19198.15..19407.63 rows=1460 width=48) (actual time=202.203..234.861 rows=36 loops=1)
         Workers Planned: 2
         Workers Launched: 2
         Buffers: shared hit=12243 read=282, temp read=1503 written=1508
         ->  Partial GroupAggregate  (cost=18198.13..18239.09 rows=730 width=48) (actual time=128.463..157.492 rows=12 loops=3)
               Group Key: (date_trunc('month'::text, (sales.date)::timestamp with time zone))
               Buffers: shared hit=12243 read=282, temp read=1503 written=1508
               ->  Sort  (cost=18198.13..18202.83 rows=1879 width=18) (actual time=125.479..133.761 rows=150654 loops=3)
                     Sort Key: (date_trunc('month'::text, (sales.date)::timestamp with time zone))
                     Sort Method: external merge  Disk: 4824kB
                     Buffers: shared hit=12243 read=282, temp read=1503 written=1508
                     Worker 0:  Sort Method: external merge  Disk: 7200kB
                     Worker 1:  Sort Method: quicksort  Memory: 1917kB
                     ->  Parallel Append  (cost=0.00..18095.95 rows=1879 width=18) (actual time=29.432..82.931 rows=150654 loops=3)
                           Buffers: shared hit=12169 read=282
                           ->  Seq Scan on sales_past sales_1  (cost=0.00..0.01 rows=1 width=18) (actual time=0.007..0.007 rows=0 loops=1)
                                 Filter: (EXTRACT(year FROM date) = '2023'::numeric)
                           ->  Seq Scan on sales_2022 sales_2  (cost=0.00..0.01 rows=1 width=18) (actual time=0.004..0.004 rows=0 loops=1)
                                 Filter: (EXTRACT(year FROM date) = '2023'::numeric)
                           ->  Seq Scan on sales_future sales_5  (cost=0.00..0.01 rows=1 width=18) (actual time=0.003..0.003 rows=0 loops=1)
                                 Filter: (EXTRACT(year FROM date) = '2023'::numeric)
                           ->  Parallel Seq Scan on sales_2023 sales_3  (cost=0.00..9080.47 rows=942 width=18) (actual time=0.014..46.128 rows=150654 loops=3)
                                 Filter: (EXTRACT(year FROM date) = '2023'::numeric)
                                 Buffers: shared hit=6251
                           ->  Parallel Seq Scan on sales_2024 sales_4  (cost=0.00..9006.09 rows=934 width=18) (actual time=44.114..44.114 rows=0 loops=2)
                                 Filter: (EXTRACT(year FROM date) = '2023'::numeric)
                                 Rows Removed by Filter: 224114
                                 Buffers: shared hit=5918 read=282
 Planning:
   Buffers: shared hit=6
 Planning Time: 0.315 ms
 Execution Time: 235.334 ms
(35 rows)




			 
# query optimization by changing the sql text and leveraging the partitioning of the table
We can see that the the partition sales_2023 is being used. So we jump right to the rows containing the data we want

EXPLAIN (ANALYZE, BUFFERS) SELECT
            DATE_TRUNC('month', date) AS month,
            SUM(quantity) AS total_quantity,
            SUM(price * quantity) AS total_revenue
        FROM sales
        WHERE date BETWEEN '2023-01-01' AND '2023-12-31'
        GROUP BY month
        ORDER BY month
		


  QUERY PLAN                                      
-----------------------------------------------------------------------------------------------------------------------------------------------------------
 Finalize GroupAggregate  (cost=14360.41..14558.13 rows=730 width=48) (actual time=83.178..85.890 rows=12 loops=1)
   Group Key: (date_trunc('month'::text, (sales.date)::timestamp with time zone))
   Buffers: shared hit=6267
   ->  Gather Merge  (cost=14360.41..14530.75 rows=1460 width=48) (actual time=83.167..85.848 rows=36 loops=1)
         Workers Planned: 2
         Workers Launched: 2
         Buffers: shared hit=6267
         ->  Sort  (cost=13360.38..13362.21 rows=730 width=48) (actual time=79.658..79.659 rows=12 loops=3)
               Sort Key: (date_trunc('month'::text, (sales.date)::timestamp with time zone))
               Sort Method: quicksort  Memory: 26kB
               Buffers: shared hit=6267
               Worker 0:  Sort Method: quicksort  Memory: 26kB
               Worker 1:  Sort Method: quicksort  Memory: 26kB
               ->  Partial HashAggregate  (cost=13312.89..13325.66 rows=730 width=48) (actual time=79.628..79.634 rows=12 loops=3)
                     Group Key: date_trunc('month'::text, (sales.date)::timestamp with time zone)
                     Batches: 1  Memory Usage: 49kB
                     Buffers: shared hit=6251
                     Worker 0:  Batches: 1  Memory Usage: 49kB
                     Worker 1:  Batches: 1  Memory Usage: 49kB
                     ->  Parallel Seq Scan on sales_2023 sales  (cost=0.00..10017.34 rows=188317 width=18) (actual time=0.015..42.397 rows=150654 loops=3)
                           Filter: ((date >= '2023-01-01'::date) AND (date <= '2023-12-31'::date))
                           Buffers: shared hit=6251
 Planning:
   Buffers: shared hit=8
 Planning Time: 0.259 ms
 Execution Time: 85.956 ms
(26 rows)



#====================================================================================
# Query optimization of top 5 products by revenue (yearly)
By creating the partition by date range. We can see that our query to get the top 5 products by revenue 
can leverage to jump right to the data necessary.
We could further optimize this query by adding an index on date,product_id,

EXPLAIN (ANALYZE, BUFFERS) SELECT
            product_id,
            product_name,
            SUM(price * quantity) AS total_revenue
        FROM sales
        WHERE date BETWEEN '2023-01-01' AND '2023-12-31'
        GROUP BY product_id, product_name
        ORDER BY total_revenue DESC
        LIMIT 5




 QUERY PLAN                                                                    
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
 Limit  (cost=47769.73..47769.75 rows=5 width=55) (actual time=407.929..409.718 rows=5 loops=1)
   Buffers: shared hit=6339, temp read=2558 written=2566
   ->  Sort  (cost=47769.73..47882.72 rows=45196 width=55) (actual time=407.927..409.714 rows=5 loops=1)
         Sort Key: (sum((sales.price * (sales.quantity)::numeric))) DESC
         Sort Method: top-N heapsort  Memory: 25kB
         Buffers: shared hit=6339, temp read=2558 written=2566
         ->  Finalize GroupAggregate  (cost=31726.99..47019.04 rows=45196 width=55) (actual time=319.265..406.222 rows=14000 loops=1)
               Group Key: sales.product_id, sales.product_name
               Buffers: shared hit=6339, temp read=2558 written=2566
               ->  Gather Merge  (cost=31726.99..45550.17 rows=90392 width=55) (actual time=319.216..393.499 rows=41999 loops=1)
                     Workers Planned: 2
                     Workers Launched: 2
                     Buffers: shared hit=6339, temp read=2558 written=2566
                     ->  Partial GroupAggregate  (cost=30726.97..34116.67 rows=45196 width=55) (actual time=305.544..370.615 rows=14000 loops=3)
                           Group Key: sales.product_id, sales.product_name
                           Buffers: shared hit=6339, temp read=2558 written=2566
                           ->  Sort  (cost=30726.97..31197.76 rows=188317 width=33) (actual time=305.394..333.680 rows=150654 loops=3)
                                 Sort Key: sales.product_id, sales.product_name
                                 Sort Method: external merge  Disk: 7096kB
                                 Buffers: shared hit=6339, temp read=2558 written=2566
                                 Worker 0:  Sort Method: external merge  Disk: 7096kB
                                 Worker 1:  Sort Method: external merge  Disk: 6272kB
                                 ->  Parallel Seq Scan on sales_2023 sales  (cost=0.00..9075.76 rows=188317 width=33) (actual time=0.009..26.807 rows=150654 loops=3)
                                       Filter: ((date >= '2023-01-01'::date) AND (date <= '2023-12-31'::date))
                                       Buffers: shared hit=6251
 Planning:
   Buffers: shared hit=29 dirtied=2
 Planning Time: 5.179 ms
 Execution Time: 411.073 ms
(29 rows)


Adding a computed column to have the calculated revenue of every product on every sale record
and then adding a covering Index helps reduce the execution time substantially.

 CREATE INDEX idx_sales_2023_date_revenue_product_id
ON sales_2023 (date, revenue DESC, product_id, product_name)
INCLUDE (quantity, price);


EXPLAIN (ANALYZE, BUFFERS) SELECT
            product_id,
            product_name,
            SUM(revenue) as total_revenue
        FROM sales
        WHERE date BETWEEN '2023-01-01' AND '2023-01-31'
        GROUP BY product_id, product_name
        ORDER BY total_revenue DESC
        LIMIT 5

                                                                            QUERY PLAN                                                                      
------------------------------------------------------------------------------------------------------------------------------------------------------------------
 Limit  (cost=9034.94..9034.95 rows=5 width=55) (actual time=70.668..70.671 rows=5 loops=1)
   Buffers: shared hit=6011
   ->  Sort  (cost=9034.94..9069.39 rows=13780 width=55) (actual time=70.662..70.663 rows=5 loops=1)
         Sort Key: (sum(sales.revenue)) DESC
         Sort Method: top-N heapsort  Memory: 25kB
         Buffers: shared hit=6011
         ->  HashAggregate  (cost=8633.81..8806.06 rows=13780 width=55) (actual time=65.966..68.755 rows=13110 loops=1)
               Group Key: sales.product_id, sales.product_name
               Batches: 1  Memory Usage: 5777kB
               Buffers: shared hit=6011
               ->  Bitmap Heap Scan on sales_2023 sales  (cost=1077.44..8355.02 rows=37172 width=29) (actual time=5.773..20.863 rows=38650 loops=1)
                     Recheck Cond: ((date >= '2023-01-01'::date) AND (date <= '2023-01-31'::date))
                     Heap Blocks: exact=5829
                     Buffers: shared hit=6011
                     ->  Bitmap Index Scan on idx_date_region_product_2023  (cost=0.00..1068.14 rows=37172 width=0) (actual time=5.079..5.079 rows=38650 loops=1)
                           Index Cond: ((date >= '2023-01-01'::date) AND (date <= '2023-01-31'::date))
                           Buffers: shared hit=182
 Planning:
   Buffers: shared hit=5
 Planning Time: 5.360 ms
 Execution Time: 72.668 ms
(21 rows)