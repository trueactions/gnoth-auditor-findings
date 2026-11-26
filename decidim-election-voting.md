# Decidim’s saved vote records matched two election fixtures

Decidim supports civic participation through proposals, assemblies, elections and other processes. The audit compared expected and recorded vote selections in two election fixtures and reviewed five conditional-form tests. It recorded **zero confirmed findings** in the tested scope.

## What was verified

| Check | What the audit observed |
| --- | --- |
| Multiple-selection vote fixture | All three expected selected-response records matched the three observed records. |
| Single-option vote control | Both expected selected-response records matched the two observed records. |
| Conditional-form fixtures | Five reviewed Jest cases passed. Within the simulated form, attachment previews and sort positions were preserved. Hidden disabled fields were excluded from simulated submission and included again when shown. |
| Test application startup | The generated Rails test application booted, and the prepared Rails/PostgreSQL diagnostic completed. |

The vote comparisons found no missing, unexpected, duplicate or differing selected-response values in those fixtures. The saved audit records the results under evidence E3 and E4, with the election fixture and command context in E10 through E12 and the form evidence in E44 through E46 and E52.

## Coverage limits

Broader module RSpec runs reached their time limits, and generators did not produce a complete bounded test report. The vote evidence applies to the tested command-level selections. Voter eligibility, voting receipts and published tallies remain unverified. The conditional-form checks observed simulated submission and previews. Server-side saving and live uploads remain unverified.

## Audit record

The saved report was sealed on November 24, 2026, Toronto time. Snapshot SHA-256 `0347e74370a36197d751fba164607b73f3a5cf58c17fd29406e8b855d3eb7c91`. [Audited Decidim revision](https://github.com/decidim/decidim/tree/58d3cd2919d37a0a09f216b253f4662453eb1c26) · [All audited repositories](README.md#audited-repositories)
