# Reversing two AI usage records changed the total

AITRA Meter measures the efficiency of AI inference, the work a deployed model does to generate a response. To calculate measures such as energy per unit of output, it needs a count of the model’s output tokens, the pieces of text the model generates. A model can serve traffic through more than one engine, and each engine can report its own counter. [Upstream AITRA Meter project](https://github.com/aitra-ai/aitra-meter).

We used **GNOTH Auditor**, Trueactions AI’s product for checking whether software delivers the results people rely on, to verify the usage count when the same total was split across engine records. [How an outcome audit works](README.md#what-an-outcome-audit-checks).

## The check

The project supplied a sample with a count of **12,450 tokens**. In a controlled comparison, the audit represented the same count as two records for the same model, labeled as different engines. Their counts were **4,150** and **8,300**. The software should return **12,450** both times, whichever record comes first.

| Input to the same counting code | Expected total | Returned total |
| --- | ---: | ---: |
| One record of 12,450 tokens | 12,450 | 12,450 |
| Engine records of 4,150 and 8,300 tokens | 12,450 | 8,300 |
| The same engine records in reverse order | 12,450 | 4,150 |

## What Auditor verified

Auditor ran the existing component that reads usage counters from vLLM, a service for running language models. The test supplied sample records in place of a live connection. Reversing the records was enough to change the answer. A newly started copy of the reader also returned 4,150 for the reversed records.

The code kept one value for a metric name and dropped the labels that distinguished the engines. Each new row overwrote the prior value. The result was the last count the program read.

A team could use the resulting count to compare deployments or budget for capacity. An undercount can distort anything calculated per token, even when the energy measurement itself is correct. This check measured the counting component with test inputs. Live traffic and actual bills were outside the test.

## Audit record

The saved comparison ran on November 6, 2026, using GNOTH Auditor 2.1.1 and the audited Go counting code.

- Audited copy SHA-256 `bd3f1c9196e6aba744f77775c423bcb897032e51b8b0e415c22a9b0c5ee9cfb6`

## Check the recorded result

Read the [Python checker](checkers/cases/ai_usage_reporting.py) to see which rule it tests. The [recorded observation](checkers/observations/ai-usage-reporting.json) contains the measurements from this audit.

From the top folder of this repository, run the checker with Python 3.8 or later. It reads the saved measurements and runs offline.

```sh
python3 checkers/check.py ai-usage-reporting checkers/observations/ai-usage-reporting.json
```

The expected last line is `FAIL` (exit code 1). The control checks pass, and the checker identifies where the measured outcome broke the rule. Checking a different version of the project requires measurements from that version.
