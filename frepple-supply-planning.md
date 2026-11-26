# frePPLe’s repeated forecast runs changed net demand

frePPLe helps planners balance demand, inventory and production capacity. GNOTH Auditor recorded four confirmed findings in the audited revision. The planning checks found that net demand changed when the same inputs were processed again, and that some constraint selections lost their effective flags.

## Confirmed findings

| Finding | What the audit observed | Follow-up |
| --- | --- | --- |
| **F1 · Repeated forecast consumption** | Three of five supplied forecast cases produced 90 units of net demand on the first solve and 80 on the identical second solve. A fresh-process control showed the difference depended on retained solver state. Evidence E48. | Reset the affected consumption measures before netting again and keep a regression check for identical repeated inputs. |
| **F2 · Constraint flag handling** | Repeated or overlapping constraint names produced an effective native mask of zero in the tested cases. Evidence E48 and E58. | Combine unique supported flags or explicitly reject ambiguous selections. |
| **F3 · Negative benchmark holdout** | The supplied M3 benchmark accepted a negative holdout and reported a percentage-error score of 478.88 for it. The audit recomputed the score using the recorded forecast and holdout. Evidence E68 and E70. | Define which negative observations the benchmark accepts and how it scores them. |
| **F4 · Transport header condition** | The Django middleware added the transport-security header to an insecure request fixture. The observed result establishes the response behavior for the tested requests. Evidence E77 and E80. | Check the request’s security state against the intended header policy and add a response test. |

## What was verified

- Ordinary nonoverlapping selections preserved the requested capacity and lead-time flags at the native solver interface. Evidence E58.
- A fresh run of the supplied rounding fixture matched its saved reference output in the prepared macOS runtime. Evidence E57 and E59.
- The as-shipped management entry ran to its help output. The forecast and constraint controls above ran in a separately prepared macOS environment. Evidence E9 and E48.

## Coverage limits

The prepared supply solver crashed, PostgreSQL socket access was blocked, and the frontend build could not start without pnpm. End-to-end production scheduling and the operational effects of the transport header remain unverified.

## Audit record

The saved report was sealed on November 22, 2026. Snapshot SHA-256 `332b36b94b85034532470baeb0b0df848d2e2d361685139de4f241223b120f79`. [Audited frePPLe revision](https://github.com/frePPLe/frepple/tree/fdecacb2d5c169121e749c0120536ea556c8dcc4) · [All audited repositories](README.md#audited-repositories)
