---
rating: hard
step: 1
last_reviewed: 2026-10-28
next_review: 2026-10-31
---

# Review: 7-Check Rolling Average

[Problem](./README.md) · [Accepted solution](./solution.sql)

## How it went

DataDriven logged this as accepted on the first submission with no hints. You did get it right before submitting, but only after one nudge, and you answered the follow-up wrong.

- **What you looked up:** how to take a rolling average in SQL.
- **What you got right on the first pass:** `PARTITION BY svc_name` and a 7-row frame written as `6 PRECEDING`. Those are the two traps this problem is built around.
- **What you missed:** the `ORDER BY` inside the window. You had `ORDER BY svc_name, checked` on the output and treated it as if it ordered the window. It doesn't: the output sort runs after the averages are computed. Without a window ordering, "the six rows before" has no defined meaning.
- **Follow-up you answered wrong:** you said that dropping `ROWS BETWEEN` gives a whole-partition average in every row. That's what happens when there's no `ORDER BY`. With an `ORDER BY`, the default frame runs from the start of the partition to the current row, so you get a running average. Rows 1–7 still match the correct answer and row 8 onward goes wrong, which is why spot-checking the first few rows doesn't catch it. You needed the visualization to see this.

## On the redo

Start from a blank editor without opening `solution.sql`.

- [ ] Before writing, name what each part of `OVER` decides:
  - `PARTITION BY` decides whose rows are in the window.
  - `ORDER BY` decides their sequence.
  - `ROWS` decides how many rows count.
- [ ] Say the default frame out loud without looking it up, and say which rows it gets wrong here.
- [ ] Explain why the 2026-01-08 auth-svc row has a `NULL` latency but a rolling average of 279.5.
- [ ] Explain why `ROWS` and not `RANGE`. The question counts checks, not time.

**Likely interviewer follow-ups:**
- Average over the last 24 hours instead of the last seven checks.
- Show `NULL` until a service has seven checks with a latency.
- Keep the result deterministic when two checks share a timestamp.

## Review log

| Date | Rating | Next redo | Notes |
|---|---|---|---|
| 2026-10-28 | hard | 2026-10-31 | First solve. Missed the window ORDER BY; wrong on the default frame. |
