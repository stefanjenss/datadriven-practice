WITH lowest_uptimes AS(
    SELECT
        svc_name,
        MIN(uptime) AS min_uptime
    FROM svc_health
    GROUP BY svc_name
),
lowest_uptimes_ranked AS (
    SELECT
        svc_name,
        min_uptime,
        RANK() OVER (ORDER BY min_uptime ASC) AS uptime_rank
    FROM lowest_uptimes
)
SELECT
    svc_name,
    min_uptime
FROM lowest_uptimes_ranked
WHERE uptime_rank <= 10
ORDER BY min_uptime;
