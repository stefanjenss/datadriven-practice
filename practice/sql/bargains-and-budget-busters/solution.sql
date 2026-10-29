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
cheapest_and_most_expensive AS (
  SELECT
    region,
    FIRST_VALUE(svc_name) OVER (
      PARTITION BY region 
      ORDER BY amount DESC, svc_name ASC
    ) AS most_expensive,
    FIRST_VALUE(svc_name) OVER (
      PARTITION BY region 
      ORDER BY amount ASC, svc_name ASC
    ) AS cheapest
    FROM single_stream
  )
  SELECT DISTINCT
    *
  FROM cheapest_and_most_expensive;





-- cloud spend by region
-- for each region:
--   - bigest line item service: name
--   - single smallest line item service: name
-- grain: one row per region
