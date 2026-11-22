# An investment research report showed Buy for a Review decision

TradingAgents is a research framework in which AI agents analyze market information and produce a portfolio decision. A reader may use the short rating in the report header to decide what deserves closer attention. The source decision and the displayed rating therefore need to agree, including when the decision says **Review**. [Upstream TradingAgents project](https://github.com/TauricResearch/TradingAgents).

We used **GNOTH Auditor**, Trueactions AI’s product for checking whether software delivers the results people rely on, to follow the application’s written decision into its report. [How an outcome audit works](README.md#what-an-outcome-audit-checks).

## Where the decision changed

The version we audited could receive a decision as plain text. That text can contain both the application’s own decision and a quoted opinion from another part of the analysis. Auditor kept the quoted opinion fixed and changed the application’s own decision from **Hold** to **Review**.

| Application’s own decision | Quoted opinion in the same text | Result |
| --- | --- | --- |
| Hold | Buy | The decision reader returned **Hold**. |
| Review | Buy | The decision reader returned **Buy**, and the report displayed **Buy**. |
| No explicit rating | No quoted rating | The decision reader returned **Review**. |

## What Auditor verified

The fallback reader accepted **Hold** as an explicit rating. An explicit **Review** sent it looking for another rating in the text, where it picked up the quoted **Buy**. Auditor followed the result into the reporting component and verified that the changed rating appeared in the report.

Someone who reads the report header first could take **Buy** as the application’s assessment even though its own decision called for review. The check established that change with controlled text, the actual decision reading code and the report component. Live model decisions, market data and trades were outside the test.

## Audit record

The saved comparisons ran on November 13, 2026, using GNOTH Auditor 2.1.3. The audit examined the path that handles free-text decisions.

- Audited copy SHA-256 `c79085200a2748aa7ee2286bf044045b8b79d83c912a4f3a389e1f22df01689f`

## Check the recorded result

Read the [Python checker](checkers/cases/investment_research.py) to see which rule it tests. The [recorded observation](checkers/observations/investment-research.json) contains the measurements from this audit.

From the top folder of this repository, run the checker with Python 3.8 or later. It reads the saved measurements and runs offline.

```sh
python3 checkers/check.py investment-research checkers/observations/investment-research.json
```

The expected last line is `FAIL` (exit code 1). The control checks pass, and the checker identifies where the measured outcome broke the rule. Checking a different version of the project requires measurements from that version.
