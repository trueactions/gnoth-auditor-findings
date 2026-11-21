# A report displayed Buy for a decision that said Review

An investment research application prepared a report from a written decision. The decision called for **Review**. One reporting path displayed **Buy** after picking up a second opinion quoted in the text.

## What should have happened

The report should preserve the application’s own decision. A quoted opinion can provide context, but it should have no effect on whether the decision was ready to act on.

## What Auditor observed

In a controlled check, a written decision marked **Hold**, with a quoted **Buy** opinion, produced a **Hold** report. Changing the application’s own decision to **Review** while leaving that second opinion in place produced a **Buy** report. A separate check with no quoted rating returned **Review**. These comparisons isolated the conditions that changed the displayed result.

## Why it matters

A person scanning the report could interpret **Buy** as the application’s decision even though the original decision called for more review.

## What was tested

The saved check covered how the application reads its written decision and how the reporting code displays the resulting rating. The audit exercised those components with controlled text. The saved run was on November 13, 2026 using GNOTH Auditor 2.1.3.

- Audited copy SHA-256 `c79085200a2748aa7ee2286bf044045b8b79d83c912a4f3a389e1f22df01689f`
- [Upstream TradingAgents project](https://github.com/TauricResearch/TradingAgents)
