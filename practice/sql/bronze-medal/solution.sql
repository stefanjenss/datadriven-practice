SELECT
    amount
FROM cloud_costs
GROUP BY amount
ORDER BY amount DESC
LIMIT 3;
