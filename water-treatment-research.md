# OpenAqua recommended chemical dosing after the request ruled it out

OpenAqua helps water-treatment researchers explore which sequences of treatment steps might work for a given water source. A researcher can specify the contaminants, the treatment goals and constraints on what the design can use. Those constraints determine which options are worth investigating. For example, a request that prohibits chemical dosing should yield a compatible option or make clear that none was found. [OpenAqua project](https://github.com/zhaorui-bi/OpenAqua).

We used **GNOTH Auditor**, Trueactions AI’s product for checking whether software delivers the results people rely on, to audit the original OpenAqua. The supplied offline demo ran successfully and produced a report. The audit then checked whether the recommendations respected the stated constraints and the evidence available to the software. [How an outcome audit works](README.md#what-an-outcome-audit-checks).

## One request, three settings

Auditor ran the same example for arsenic three times. The only change was whether the request allowed chemical dosing, prohibited it or left the setting unspecified. OpenAqua returned the same response each time. The proposed sequence included steps labeled **Chemical Treatment** and **Chlorine**. Its constraint check returned **PASS** in all three cases.

| Dosing setting | What OpenAqua returned |
| --- | --- |
| Allowed | Sequence including Chemical Treatment and Chlorine, marked **PASS**. |
| Prohibited | The same sequence, marked **PASS**. |
| Unspecified | The same sequence, marked **PASS**. |

Auditor traced the setting through the code. OpenAqua kept it when it read the request. The offline planner and its constraint checker proceeded without applying it. The **PASS** label could lead a reviewer to believe the stated restriction had been checked.

## Two other checks from the same audit

- **Full coverage for ineffective options.** For 1,4-dioxane, the program awarded full coverage to a sequence that included steps its own references described as ineffective or unsuitable for full-scale use. Auditor traced this to the software treating a match in its filenames as evidence that the method would remove the contaminant.
- **A saved case never reached search.** OpenAqua acknowledged one new case. Auditor checked the searchable index after its rebuild finished. It still contained the same 929 records, and the new case was missing. The rebuild read a different source from the place where the application saved the case.

## Audit record

The saved audit ran on November 18, 2026, using GNOTH Auditor 2.1.3. It covered the original OpenAqua source and the reference data available in the audited snapshot. The offline demo ran as shipped. The controlled dosing comparison exercised the existing recommendation code through a temporary loader on a disposable copy. Hosted-model behavior, plant performance and drinking-water compliance were outside these checks.

- Audited copy SHA-256 `5a6a3901eb0a611b2ebc0eaba06dda761c7d445195f34b0fe6f4e1567e09579a`

## Check the recorded result

Read the [Python checker](checkers/cases/water_treatment_research.py) to see which rule it tests. The [recorded observation](checkers/observations/water-treatment-research.json) contains the measurements from this audit.

From the top folder of this repository, run the checker with Python 3.8 or later. It reads the saved measurements and runs offline.

```sh
python3 checkers/check.py water-treatment-research checkers/observations/water-treatment-research.json
```

The expected last line is `FAIL` (exit code 1). The control checks pass, and the checker identifies where the measured outcome broke the rule. Checking a different version of the project requires measurements from that version.
