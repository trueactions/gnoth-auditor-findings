# A failed task returned a success status

A background task stopped with an error. The process still returned the status the application uses to indicate success.

## What should have happened

A task that cannot finish should leave an error status that later steps can use. Printing the error is useful to an operator. The job’s completion status must also reflect the failure.

## What Auditor observed

In the tested copy, a task failed while starting because a dependency was missing in the audit environment. The worker showed the error and then returned zero, the normal success status. In a diagnostic comparison, letting the same error reach the process boundary returned one, a failure status. This isolated the way the worker reported failure.

## Why it matters

A later step can consult the status without reading the full error log. A success status may lead that step to rely on work that never finished.

## What was tested

The saved check exercised an actual task-dispatch handler and observed the child process’s status. The scope was worker behavior in this diagnostic. The full server workflow was outside the test. The audit was run on November 17, 2026 using GNOTH Auditor 2.1.3.

- Audited copy SHA-256 `f7b5bfd05c3ad95502100e5e2981ebdf8d749e84941b57f4e2ca036fc6c2ed7b`
- [Upstream RD-Agent project](https://github.com/microsoft/RD-Agent)
