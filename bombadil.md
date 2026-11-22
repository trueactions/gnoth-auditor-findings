# Bombadil reported that three new test actions already existed

Bombadil tests browser interfaces. A team can teach it a custom action, such as searching, so the tester can exercise behavior specific to that application. Each action needs a unique name. A duplicate warning is useful when two actions share a name, because the tester needs to know which action to run. [Bombadil project](https://github.com/antithesishq/bombadil).

Trueactions AI used GNOTH Auditor to check whether the custom-action component could distinguish a genuinely repeated name from a first registration. The test captured the component’s response at registration, before any browser action ran.

| What the test asked the component to register | What it reported |
| --- | --- |
| An ordinary name for the first time | Registration succeeded. |
| The same name a second time | Rejected it as a duplicate, as expected. |
| Three other names, each on its first registration | Rejected all three as duplicates. |

The three names were already present as built-in JavaScript names. The component counted those inherited names when it looked for earlier registrations. In each of those cases the message said the action already existed, although the team had never registered it. A test author encountering the message would reasonably look for a duplicate in their own tests.

## Audit record

On November 19, 2026, Auditor called the project’s browser-side TypeScript interface locally in Deno. The three names above were tested through the public interface. A separate, lower-level check observed the same rejection for 12 previously unused names. The Rust runner, its embedded runtime, a complete browser test and replay were outside these checks. The saved report records this as finding F1. [Audited upstream revision](https://github.com/antithesishq/bombadil/tree/a56bfa7af69fcb51fc2f99cd7e04d9c9073324f0).

- Audited copy SHA-256 `fbaebfebe82609b96e0e043611a313736690b3a6a616f2d7e10b27c8083f508e`
- [How GNOTH Auditor checks outcomes](README.md#what-an-outcome-audit-checks) · [All audited repositories](README.md#audited-repositories)

## Check the recorded result

Read the [Python checker](checkers/cases/bombadil.py) to see which rule it tests. The [recorded observation](checkers/observations/bombadil.json) contains the measurements from this audit.

From the top folder of this repository, run the checker with Python 3.8 or later. It reads the saved measurements and runs offline.

```sh
python3 checkers/check.py bombadil checkers/observations/bombadil.json
```

The expected last line is `FAIL` (exit code 1). The control checks pass, and the checker identifies where the measured outcome broke the rule. Checking a different version of the project requires measurements from that version.
