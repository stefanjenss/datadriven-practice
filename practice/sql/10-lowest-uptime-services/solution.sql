WITH svc_mins AS (
  SELECT
    svc_name,
    min(uptime) AS min_uptime
  FROM svc_health
  GROUP BY svc_name
  ORDER BY min_uptime
),
svc_mins_ranked AS (
  SELECT
    svc_name,
    min_uptime,
    RANK() OVER (ORDER BY min_uptime ASC) as svc_rank
  FROM svc_mins
)
SELECT
  svc_name,
  min_uptime
FROM svc_mins_ranked
WHERE svc_rank <= 10;
