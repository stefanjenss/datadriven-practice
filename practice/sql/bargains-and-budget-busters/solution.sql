WITH single_stream AS (
  SELECT
    region,
    svc_name,
    amount
  FROM cloud_costs
  UNION ALL
    SELECT
      region,
      svc_name,
      amount
    FROM cost_allocs
),
stream_w_amount_ranking AS (
  SELECT
    region,
    svc_name,
    amount,
    ROW_NUMBER() OVER(PARTITION BY region ORDER BY amount ASC) AS ascending_rank,
    ROW_NUMBER() OVER(PARTITION BY region ORDER BY amount DESC) AS descending_rank
  FROM single_stream
),
most_expensive_by_region AS (
  SELECT
    region,
    svc_name,
    amount,
    CASE
      WHEN descending_rank = 1 THEN svc_name
    END AS most_expensive
  FROM stream_w_amount_ranking
  WHERE descending_rank = 1
),
cheapest_by_region AS (
  SELECT
    region,
    svc_name,
    amount,
    CASE
      WHEN ascending_rank = 1 THEN svc_name
    END AS cheapest
  FROM stream_w_amount_ranking
  WHERE ascending_rank = 1
  )
  SELECT
    e.region,
    e.most_expensive,
    c.cheapest
  FROM most_expensive_by_region AS e
  JOIN cheapest_by_region c ON e.region = c.region;
  




-- cloud spend by region
-- for each region:
--   - bigest line item service: name
--   - single smallest line item service: name
-- grain: one row per region
