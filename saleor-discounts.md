# Saleor split a $1.01 discount into two $0.51 portions

Saleor is an e-commerce platform. When a merchant applies one fixed discount to an order, Saleor can divide it between the merchandise and shipping for a tax calculation. Whichever portion receives the extra cent, the two portions should add up to the discount the merchant entered. [Saleor project](https://github.com/saleor/saleor).

Trueactions AI used GNOTH Auditor to compare Saleor’s original discount calculation with that simple accounting rule. The test used a $10 merchandise subtotal, $10 shipping and US dollars.

| Fixed discount | Allocated to merchandise | Allocated to shipping | Sum of the portions |
| ---: | ---: | ---: | ---: |
| $1.00 | $0.50 | $0.50 | $1.00 |
| $1.01 | $0.51 | $0.51 | **$1.02** |

An even split of $1.01 is 50½ cents per portion. The component rounded both portions up independently. A separate Saleor calculation applied the $1.01 discount to $20 and returned $18.99 as expected. With zero shipping, the allocation also put the full $1.01 on merchandise. These comparisons locate the extra cent in how the component divided the discount.

## Audit record

On November 20, 2026, Auditor exercised Saleor’s discount component in an offline test. The result describes the values returned for a tax calculation. The test stopped before a tax service, invoice or customer payment, so it establishes no customer charge. The saved report records this as finding F1. [Audited upstream revision](https://github.com/saleor/saleor/tree/4974a295ddd33b1a34ebac1b1d6c0730d7edc8ee).

- Audited copy SHA-256 `c3ef46e363ddef58b63c2f89816e67e39317fbfedbe48c3b8d951eb72544104f`
- [How GNOTH Auditor checks outcomes](README.md#what-an-outcome-audit-checks) · [All audited repositories](README.md#audited-repositories)

## Check the recorded result

Read the [Python checker](checkers/cases/saleor_discounts.py) to see which rule it tests. The [recorded observation](checkers/observations/saleor-discounts.json) contains the measurements from this audit.

From the top folder of this repository, run the checker with Python 3.8 or later. It reads the saved measurements and runs offline.

```sh
python3 checkers/check.py saleor-discounts checkers/observations/saleor-discounts.json
```

The expected last line is `FAIL` (exit code 1). The control checks pass, and the checker identifies where the measured outcome broke the rule. Checking a different version of the project requires measurements from that version.
