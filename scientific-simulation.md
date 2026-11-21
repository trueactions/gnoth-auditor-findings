# A 20-second request returned an earlier 8-second result

Software for a scientific simulation reused a shorter result when the reviewer asked for a 20-second run.

## What should have happened

When a request specifies 20 seconds of simulated time, any stored result reused for that request should cover those 20 seconds. Results from a shorter test run belong to a different request.

## What Auditor observed

The test stored eight seconds of sample data in the cache, where the software keeps results for later reuse. A request for 20 seconds retrieved that same sample. Bypassing the cache returned a 20-second sample. The difference was reproduced at the point where the software retrieved saved results.

## Why it matters

A researcher could compare two results believing that they cover the same time period. The difference could instead reflect which run happened to fill the cache first.

## What was tested

The saved diagnostic used the actual code that stores and retrieves results with substitute time-series data. It checked the result length in that component. The underlying simulation and its scientific outputs were outside the run’s scope. The audit was run on November 6, 2026 using GNOTH Auditor 2.1.1.

- Audited copy SHA-256 `79183173b1c3deec8129a7bccee379ea580dd92392dd135c124bab77f2c8267f`
- [Upstream ion-exchange-neural-mass project](https://github.com/grabuffo/ion-exchange-neural-mass)
