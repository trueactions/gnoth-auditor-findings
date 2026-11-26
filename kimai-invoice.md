# Kimai’s issued invoice matched its three saved timesheets

In an isolated run with synthetic timesheets, Kimai issued invoice **2026/001**. The runner recorded four matching comparisons for that invoice. The audit recorded **zero confirmed findings** in the tested scope.

## What was verified

| Saved entry | Hours | Hourly rate | Amount on the issued invoice |
| --- | ---: | ---: | ---: |
| Entry 1 | 1 | €17.23 | €17.23 |
| Entry 2 | 2 | €22.28 | €44.56 |
| Entry 3 | 3 | €27.78 | €83.34 |

1. The three downloaded lines matched the saved timesheet IDs, hours, rates and amounts.
2. The downloaded invoice matched the totals calculated from the timesheets and template tax. The subtotal was **€145.13**, tax was **€27.57**, and the total was **€172.70**.
3. The totals stored in the database matched that calculation.
4. The IDs marked exported matched the IDs selected from the saved timesheets.

The repository suite reported 5,372 passing cases. The audit credited cases with recorded assertions. The invoice comparison above used the issued document and the saved database records. Evidence E4.

## Coverage limits

The invoice comparison covers one synthetic invoice in the recorded configuration. A separate check verified the captured HTML columns. The report’s monetary checker could not bind the runner’s normalized comparison fields, so its formal billing reliance rating remained limited. Browser time entry, production configuration, integrations, concurrent issuance and failure recovery remain unverified. Evidence E64 and E65.

## Audit record

The saved report was sealed on November 23, 2026. Snapshot SHA-256 `2aef29a0173f6f81eabd3b3d7c387e26c7714f37203a25f123f87971d447b7e1`. [Audited Kimai revision](https://github.com/kimai/kimai/tree/382c618f89ffd8add341ab882e1221fa02ce6fcb) · [All audited repositories](README.md#audited-repositories)
