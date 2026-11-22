---
rating: hard
step: 1
last_reviewed: 2026-10-28
next_review: 2026-10-31
---

# Review: 10 Lowest Uptime Services

[Problem](./README.md) · [Accepted solution](./solution.sql)

## How it went

DataDriven logged this as accepted on the first submission with no hints. That's accurate, but it was the first time you wrote a CTE or used `RANK()`, so the problem was harder for you than that log suggests.

- **Where you started:** you didn't know how to begin. You tried a plain `GROUP BY`, then `OVER (PARTITION BY ...)`, and neither worked.
- **What you looked up:** the minimum value per group, CTE syntax, chaining two CTEs, and `RANK()`.
- **What broke the deadlock:** asking what each output row is. It's one row per service, so you collapse with `GROUP BY` first and rank the result afterward.
- **Slip you fixed before submitting:** the `ORDER BY` was inside the first CTE and missing from the final `SELECT`. A sort inside a CTE doesn't carry through to the output.
- **Left open:** you picked `RANK()` and never said why it fits better than `DENSE_RANK()` or `ROW_NUMBER()`.

**Redo on Oct 28 (three days early):** failed the first submission and fixed it yourself.
- **What broke:** you wrote `MIN(uptime) OVER (PARTITION BY svc_name)` instead of `GROUP BY svc_name`. The number was right, but the window kept one row per check. `RANK()` then gave each service's duplicate rows the same rank, which pushed the next service's rank past 10.
- **How you found it:** you ran one CTE at a time until the output looked wrong. That's the method to keep using.
- **What it shows:** the shape question tripped you on both attempts. Before you write a query, decide whether you need one row per group or every row.

## On the redo

Start from a blank editor without opening `solution.sql`.

- [ ] Before writing anything, say what one output row is.
- [ ] Put the `ORDER BY` on the outer query.
- [ ] Say out loud which of `ROW_NUMBER`, `RANK` and `DENSE_RANK` matches "include every service tied for 10th," and what the other two would return if two services tied for 3rd.
- [ ] Stretch: write it with one CTE. Window functions run after `GROUP BY`, so `RANK() OVER (ORDER BY MIN(uptime))` can share a `SELECT` with the grouping.

**Likely interviewer follow-ups:**
- Rank by average uptime instead of the lowest.
- Return exactly ten rows, breaking ties by name.
- Find the ten worst services per region.

## Review log

| Date | Rating | Next redo | Notes |
|---|---|---|---|
| 2026-10-28 | hard | 2026-10-31 | First solve. Learned CTEs and RANK() mid-problem. |
| 2026-10-28 | hard | 2026-10-31 | Redo. Failed first submission: window MIN instead of GROUP BY. Fixed it alone by running each CTE. |
