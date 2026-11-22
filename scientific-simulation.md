# A full simulation request reused a short test result

This neuroscience research project provides code for simulating the activity of neurons and reproducing figures from a study. A researcher can run a quick test to see whether the workflow runs, then request a longer run to generate data for a figure. The code can save earlier results in a cache so that matching requests can reuse them. [Upstream ion-exchange neural-mass project](https://github.com/grabuffo/ion-exchange-neural-mass).

We used **GNOTH Auditor**, Trueactions AI’s product for checking whether software delivers the results people rely on, to check whether the stored results matched the requested duration. [How an outcome audit works](README.md#what-an-outcome-audit-checks).

## What came back

The workflow for one figure used **8 seconds** of simulated time in its quick mode and **20 seconds** in its full mode. Auditor put an eight-second sample in the cache and used the actual cache helper to make the full-mode request. The test supplied sample time-series data in place of the scientific simulation so it could measure what the retrieval step returned.

| Action | Data returned |
| --- | --- |
| Request the full result after storing the eight-second sample | The earlier eight-second sample. |
| Make the same 20-second request with cache reuse bypassed | A 20-second sample. |

## What Auditor verified

The cache used the same lookup identifier for both durations. When the short run filled that slot first, the longer request found the short data and used it. The comparison with cache reuse bypassed isolated that behavior in the saved-results code.

A researcher could proceed with figure generation believing the data covers the full requested interval. Auditor measured the data returned by the storage code using stand-in samples. The solver and figure generation were outside this test.

## Audit record

The diagnostic ran on November 6, 2026, using GNOTH Auditor 2.1.1. It used the audited project’s actual saved-results helper and the durations specified by its Figure 2 workflow.

- Audited copy SHA-256 `79183173b1c3deec8129a7bccee379ea580dd92392dd135c124bab77f2c8267f`

## Check the recorded result

Read the [Python checker](checkers/cases/scientific_simulation.py) to see which rule it tests. The [recorded observation](checkers/observations/scientific-simulation.json) contains the measurements from this audit.

From the top folder of this repository, run the checker with Python 3.8 or later. It reads the saved measurements and runs offline.

```sh
python3 checkers/check.py scientific-simulation checkers/observations/scientific-simulation.json
```

The expected last line is `FAIL` (exit code 1). The control checks pass, and the checker identifies where the measured outcome broke the rule. Checking a different version of the project requires measurements from that version.
