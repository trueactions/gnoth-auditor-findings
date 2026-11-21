# The same usage records produced two different totals

Two sample usage counts added up to 12,450 tokens. A reporting tool returned 8,300 tokens, then 4,150 when the same two counts were presented in reverse order.

## What should have happened

The two records counted 4,150 and 8,300 tokens. Adding them should give 12,450 in either order.

## What Auditor observed

| Input to the same reporting code | Reported total |
| --- | ---: |
| A single record of 12,450 tokens | 12,450 |
| Two records of 4,150 and 8,300 tokens | 8,300 |
| The same two records in reverse order | 4,150 |

The code treated both records as entries for the same measure. The later one replaced the earlier one during processing, so the result depended on which record came last.

## Why it matters

Usage counts can feed capacity planning or cost estimates. If this undercount reached those reports, a team could make decisions based on too little recorded usage.

## What was tested

The saved check ran the relevant Go code with a controlled variation of a supplied usage sample. It measured the reported count at that step. It was run on November 6, 2026 using GNOTH Auditor 2.1.1.

- Audited copy SHA-256 `bd3f1c9196e6aba744f77775c423bcb897032e51b8b0e415c22a9b0c5ee9cfb6`
- [Upstream AITRA Meter project](https://github.com/aitra-ai/aitra-meter)
