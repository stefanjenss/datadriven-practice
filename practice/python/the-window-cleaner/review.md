---
rating: again
step: 0
last_reviewed: 2026-10-28
next_review: 2026-10-29
---

# Review: The Window Cleaner

[Problem on DataDriven](https://datadriven.io/problems/the_window_cleaner). Your solution lands in this folder once DataDriven syncs it.

## How it went

You needed a lot of help on this one, so it's logged as **again**. It's your first Python problem on the path: the length of the longest substring with no repeated characters, solved with a sliding window and a set.

- **Where you started:** you knew it was a sliding window and had already read the solution. You still didn't see why it works, even after googling sliding windows.
- **What unlocked it:** writing the brute-force version first. That version restarts at every left index and walks right until it hits a repeat, so it rescans characters it has already cleared. The sliding window is the same idea without the rescan. When a duplicate comes in, you evict characters from the left until it's gone, and the right edge never moves backward.
- **Corrected along the way:**
  - The set holds characters (`s[right]`), not indexes. Indexes are always unique, so a set of indexes would never catch a repeat.
  - The `+1` in `right - left + 1` isn't about zero-indexing. It's a fencepost count: positions 2 through 4 hold three characters.

## On the redo

Start from a blank editor without looking at the solution.

- [ ] Write the brute force in a couple of minutes, say what it rescans, then turn it into the sliding window.
- [ ] Say the two rules that keep the set in sync with the window: when `right` moves, add a character; when `left` moves, remove one.
- [ ] Explain why the inner loop is a `while` and not an `if`. Trace the last two characters of `"abcabcbb"` to show it.
- [ ] Give the time complexity of both versions, and say why the sliding window is O(n) even though it has a nested loop.

**Likely interviewer follow-ups:**
- Return the substring itself, not its length.
- Allow at most k distinct characters instead of none repeated.
- Use a dict of last-seen indexes so `left` jumps ahead instead of stepping one character at a time.

## Review log

| Date | Rating | Next redo | Notes |
|---|---|---|---|
| 2026-10-28 | again | 2026-10-29 | First solve. Had read the solution first; needed the brute force walkthrough, set-of-characters and +1 corrections. |
