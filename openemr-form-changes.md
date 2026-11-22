# In a form test, OpenEMR skipped the exit warning after one optional answer changed

OpenEMR is an electronic health records system. Its legacy GAD-7 questionnaire includes scored answers and a separate question about how much difficulty the person experiences. Someone who edits either kind of answer and then chooses to leave would expect the form to recognize that work is unsaved. [OpenEMR project](https://github.com/openemr/openemr).

Trueactions AI used GNOTH Auditor to check the form’s own change detection in a simulated browser. The test changed the optional answer and tried to leave. On the same simulated page, it then reset the tracking flags, called the scored-answer change handler with a test value and tried to leave again. It recorded whether the form recognized the edit, asked for confirmation and selected the exit.

| Test action | What the form did on exit |
| --- | --- |
| Changed only the optional difficulty answer | Displayed the new selection, kept the form marked as unedited and selected the exit without asking for confirmation. |
| Called the scored-answer change handler directly | Marked the form as edited and asked for confirmation. Declining to leave kept the form open. |

The control shows that the warning could work when the form marked itself as edited. Changing the optional answer left that flag clear. The consequence demonstrated here is the missing opportunity to cancel an exit.

## Audit record

On November 21, 2026, Auditor exercised the project’s shipped form logic with a simulated page and captured the navigation decision. The test used synthetic answers and stopped at that decision. An installed electronic record system, patient records, persistence after leaving and clinical scoring or care were outside its scope. The saved report records this as finding F2. [Audited upstream revision](https://github.com/openemr/openemr/tree/48c71737f40ae13f808336d41d63d6a8cda20c54).

- Audited copy SHA-256 `a3797b47d36581972b8eed0cbb4b88008fc8afd274f70c58c05338396f32c8d1`
- [How GNOTH Auditor checks outcomes](README.md#what-an-outcome-audit-checks) · [All audited repositories](README.md#audited-repositories)

## Check the recorded result

Read the [Python checker](checkers/cases/openemr_form_changes.py) to see which rule it tests. The [recorded observation](checkers/observations/openemr-form-changes.json) contains the measurements from this audit.

From the top folder of this repository, run the checker with Python 3.8 or later. It reads the saved measurements and runs offline.

```sh
python3 checkers/check.py openemr-form-changes checkers/observations/openemr-form-changes.json
```

The expected last line is `FAIL` (exit code 1). The control checks pass, and the checker identifies where the measured outcome broke the rule. Checking a different version of the project requires measurements from that version.
