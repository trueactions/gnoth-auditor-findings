# A background job failed and signaled success

RD-Agent automates parts of data and model research. Some work runs in a separate background process, so the rest of the application uses a completion status to determine whether the task succeeded. In this workflow, a process status of **0** means success and a nonzero status signals failure. Later steps can act on that status without reading the full log. [Upstream RD-Agent project](https://github.com/microsoft/RD-Agent).

We used **GNOTH Auditor**, Trueactions AI’s product for checking whether software delivers the results people rely on, to compare the task’s reported status with what happened when it ran. [How an outcome audit works](README.md#what-an-outcome-audit-checks).

## One failure, two statuses

The audit ran the application’s actual task dispatch handler in a child process. In the audit environment, the dispatched task encountered a missing dependency and stopped during startup. The worker printed the error. Its process status was still **0**, and the application’s status reader saw **0**.

| Run | What happened to the task | What the worker reported |
| --- | --- | --- |
| Existing handler | The task stopped during startup and the worker printed the error. | **0**, the code for success. |
| Diagnostic comparison with the same task and error | The task stopped at the same point and the error was allowed to reach the process boundary. | **1**, a failure status. |

## What Auditor verified

The worker caught the task error, printed it and then ended normally. Letting the same error reach the process boundary changed only the way the failure was reported. The comparison showed why downstream software could see a successful completion while the log showed a failure.

A later step could rely on an output that the worker never produced. The audit established the incorrect status in the task handler and its status reader. The full server and any subsequent workflow effects were outside this run.

## Audit record

The saved comparison ran on November 17, 2026, using GNOTH Auditor 2.1.3 and a controlled copy of the task handler.

- Audited copy SHA-256 `f7b5bfd05c3ad95502100e5e2981ebdf8d749e84941b57f4e2ca036fc6c2ed7b`

## Check the recorded result

Read the [Python checker](checkers/cases/background_jobs.py) to see which rule it tests. The [recorded observation](checkers/observations/background-jobs.json) contains the measurements from this audit.

From the top folder of this repository, run the checker with Python 3.8 or later. It reads the saved measurements and runs offline.

```sh
python3 checkers/check.py background-jobs checkers/observations/background-jobs.json
```

The expected last line is `FAIL` (exit code 1). The control checks pass, and the checker identifies where the measured outcome broke the rule. Checking a different version of the project requires measurements from that version.
