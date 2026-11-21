# A screening tool shortlisted a treatment its own source rejected

The version we adapted passed all 114 supplied tests. Its screening step still shortlisted a treatment that the cited source said did not effectively remove the target contaminant.

## What should have happened

The software was supposed to exclude treatments when the cited source showed they did not work for the contaminant being screened. A treatment could be considered only if its source supported the intended result.

## What Auditor observed

In the check, the software ranked one such treatment second among three shortlisted options. The source described no reduction in the concentration of the contaminant. The screening step missed that wording and treated the option as eligible. The finding compares the recommendation with the source it relied on.

## Why it matters

A reviewer could carry an unsupported option into the next review while believing the screening requirement had been satisfied. Passing the supplied tests answered a different question from checking whether that specific source and recommendation agreed.

## What was tested

We tested the founder-adapted OpenAqua2 version through the screening code in a controlled diagnostic. This check covered how the software interpreted its source and produced a shortlist. The saved run was on November 17, 2026 using GNOTH Auditor 2.1.3.

- Adapted version commit `49e2813a8c6d3244a0b4930a9ff875466ab53793`
- Audited copy SHA-256 `65186d315fcf2ab8a2d7769261c1d4ae693eda93e2ca3dea0a6e9b110e6ec31b`
- [Upstream OpenAqua project](https://github.com/zhaorui-bi/OpenAqua)
