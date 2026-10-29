---
rating: again
step: 0
last_reviewed: 2026-10-29
next_review: 2026-10-30
---

# Review: Bargains and Budget-Busters

[Problem](./README.md) · [Accepted solution](./solution.sql)

## How it went

DataDriven logged this as accepted on the first submission with no hints, in 1 h 33 min. The key ideas came from nudges spread across that time, so it's logged as **again**. It's your first Hard problem and introduced four new concepts.

- **Misread the prompt twice.** First you summed amounts per service, when the question asks for the single biggest and smallest line items. Then you assumed `most_expensive` had to come from allocations and `cheapest` from costs. The prompt says to treat both tables as one combined stream, so a charge's source doesn't matter.
- **New concept: stacking rows.** `UNION ALL` puts one table's rows under the other's, like `pd.concat`. A `JOIN` adds columns side by side, like `pd.merge`. Use `UNION ALL` rather than `UNION`, because two identical charges are two real line items.
- **New concept: `MAX` doesn't carry its row.** `GROUP BY region` with a bare `svc_name` errors, because a number like `MAX(amount)` can't tell SQL which service it came from. The fix is to rank the rows within each region and keep rank 1. You chose `ROW_NUMBER` correctly, since it guarantees exactly one row per region.
- **New concept: long to wide.** Your first ranked query returned two labeled rows per region. Joining the "most expensive" set to the "cheapest" set on `region` reshaped it into one row per region.
- **Accepted, but with gaps:**
  - Neither window breaks ties by `svc_name`, which the page asks for.
  - There's no final `ORDER BY`.
  - The `CASE` expressions are redundant, because the `WHERE` already keeps only rank-1 rows.
  - DataDriven rated the query 337% above optimal. Its big-O is already optimal (O(n log n)), so the gap is extra work: the ranked rows get read twice and joined back together.

## On the redo

Start from a blank editor without looking at `solution.sql`.

- [ ] Before writing, read the prompt and say what one line item is and what one output row is.
- [ ] Build the stacked stream first, then run it alone and check that the row count is the two tables combined.
- [ ] Break ties with `svc_name` in both windows, and end with an `ORDER BY`.
- [ ] Get both service names onto every row in a single pass with `FIRST_VALUE`, then collapse to one row per region. That avoids the second read and the join.
- [ ] Explain the single-line-item edge case: why a `CASE` label loses `most_expensive`, and why the join and `FIRST_VALUE` versions don't.

**Likely interviewer follow-ups:**
- What if allocations re-cut the same dollars as the cost ledger? Would combining them double-count?
- Return the amounts alongside the service names.
- Find the top three line items per region instead of the top one.

## Review log

| Date | Rating | Next redo | Notes |
|---|---|---|---|
| 2026-10-29 | again | 2026-10-30 | First solve, 1h33m. Needed nudges on combined stream, UNION ALL, ranking for svc_name, and long-to-wide. |
