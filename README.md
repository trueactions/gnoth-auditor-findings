# GNOTH Auditor findings

What happened when Trueactions AI used GNOTH Auditor to check whether software delivered the result its rules or inputs called for.

| Case | What Auditor found |
| --- | --- |
| [Water-treatment research](water-treatment-research.md) | An adapted screening tool passed 114 tests and shortlisted a treatment that its own source said did not effectively remove the target contaminant. |
| [AI usage reporting](ai-usage-reporting.md) | Two records totaling 12,450 tokens produced totals of 8,300 or 4,150 depending on their order. |
| [Investment research](investment-research.md) | One report showed **Buy** for a decision that said **Review**. |
| [Scientific simulation](scientific-simulation.md) | A request for 20 seconds of data returned an earlier 8-second result. |
| [Background jobs](background-jobs.md) | A task stopped with an error and returned a success status. |
| [Social-media simulation](social-media-simulation.md) | Two posts were logged as successful. The test recorder captured one submission. |

Each page gives the expected result, the observed result, the test scope, and an identifier for the software copy tested. The upstream project links give context for those snapshots. The observations apply to the checks described in the case.

[Trueactions AI Advisory](https://trueactions.ai/advisory)
