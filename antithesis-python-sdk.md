# The Antithesis Python SDK listed five checks and registered none at startup for one directory layout

The Antithesis Python SDK lets developers describe properties that their software should satisfy during testing. The SDK can read these declarations from a catalog. For a developer who sees five declarations listed, the practical question is whether the SDK also announces those five when the application starts. [Antithesis Python SDK project](https://github.com/antithesishq/antithesis-sdk-python).

Trueactions AI used GNOTH Auditor to follow the same five declarations through both operations. It recorded what the catalog reader listed and what the local startup code actually emitted. The contents of the catalog stayed the same.

| How the test specified the catalog | Declarations listed | Declarations emitted at startup |
| --- | ---: | ---: |
| The catalog file itself | 5 | 5 |
| The directory directly containing that file | 5 | 0 |

Startup exited successfully and gave no warning in the second run. A separate control using the SDK’s expected parent-and-application directory layout registered all five. The catalog reader and the startup code resolved the directory differently. Listing the right file was therefore insufficient evidence that startup had announced its checks.

## Could the catalog also miss checks that ran?

Auditor compared two small Python programs that ran the same five checks. One imported the SDK’s assertions module under its usual name. The other gave that module a valid alternate name. Both emitted the same five check identifiers when they ran. The catalog scanner listed five for the ordinary import and zero for the alternate name. A developer using that inventory to plan test coverage would see different lists for two programs that exercised the same checks.

## Audit record

On November 19, 2026, Auditor exercised the local Python SDK’s catalog reader, startup code and scanner. An installed customer application and a session on the hosted Antithesis service were outside the checks. The saved report records the startup and scanner findings as F6 and F1. [Audited upstream revision](https://github.com/antithesishq/antithesis-sdk-python/tree/1c8a39eceb459deb4769182f1034b8733f7c388e).

- Audited copy SHA-256 `65aeb02788808c5786854ab5752ff04d2dc8e9072d65366f2676fb5488ea0aca`
- [How GNOTH Auditor checks outcomes](README.md#what-an-outcome-audit-checks) · [All audited repositories](README.md#audited-repositories)

## Check the recorded result

Read the [Python checker](checkers/cases/antithesis_python_sdk.py) to see which rule it tests. The [recorded observation](checkers/observations/antithesis-python-sdk.json) contains the measurements from this audit.

From the top folder of this repository, run the checker with Python 3.8 or later. It reads the saved measurements and runs offline.

```sh
python3 checkers/check.py antithesis-python-sdk checkers/observations/antithesis-python-sdk.json
```

The expected last line is `FAIL` (exit code 1). The control checks pass, and the checker identifies where the measured outcome broke the rule. Checking a different version of the project requires measurements from that version.
