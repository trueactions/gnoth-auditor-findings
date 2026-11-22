# Check the eleven audit cases

Each case has a small Python checker, a recorded observation, and a control that shows whether the comparison worked. The checkers run offline with Python 3 and its standard library. You can read the rule, replay the recorded result, or evaluate measurements from your own build.

## Run a check

Run these commands from the folder containing `check.py`.

```sh
python3 check.py --verify-examples
python3 check.py saleor-discounts
python3 check.py saleor-discounts observations/saleor-one-cent-fixed.json
```

The first command verifies the checksums of the included observations and checks every control and rule against the recorded result. Its expected summary is **14/14**. The second prints the original Saleor comparison, including the two portions that total 102 cents on a 101-cent discount. The third evaluates the saved measurements from a local fix on a separate one-cent order.

| Result for a single observation | Meaning | Exit code |
| --- | --- | ---: |
| PASS | All controls and all outcome rules hold for the supplied measurements. | 0 |
| FAIL | The controls passed and at least one measured outcome broke its rule. | 1 |
| INCONCLUSIVE | A control failed, a required measurement was missing, or the input was invalid. | 2 |

## Cases

| Project | What the code checks | Open the files |
| --- | --- | --- |
| AITRA Meter | The two engine counters sum to the same total in either order and in a fresh reader. A single combined counter is the control. | [Code](cases/ai_usage_reporting.py) · [Observation](observations/ai-usage-reporting.json) |
| Antithesis Python SDK | Startup emits the catalog's five declarations. The scanner lists the same five identities exercised at runtime. File, parent-directory and ordinary-import measurements provide the controls. | [Code](cases/antithesis_python_sdk.py) · [Observation](observations/antithesis-python-sdk.json) |
| RD-Agent | A recorded task error produces a nonzero child status and a failure status at the caller. The same error reaching the process boundary is the control. | [Code](cases/background_jobs.py) · [Observation](observations/background-jobs.json) |
| Bombadil | First-time action names succeed at both tested interfaces. An ordinary name succeeds on the first attempt, and a genuine repeat is rejected as a duplicate. | [Code](cases/bombadil.py) · [Observation](observations/bombadil.json) |
| TradingAgents | An explicit Review decision survives parsing and appears in the report. Two controls cover an explicit Hold with the same quote and a text with no rating. | [Code](cases/investment_research.py) · [Observation](observations/investment-research.json) |
| OpenEMR | An optional answer changes, the form recognizes the edit, and declining to leave keeps it open. The control directly calls the scored-answer handler after resetting the flags on the same simulated form. | [Code](cases/openemr_form_changes.py) · [Observation](observations/openemr-form-changes.json) |
| Saleor | The sum of the two discount portions equals the entered discount in integer cents. Equal portions, zero shipping and direct subtraction provide the original controls. | [Code](cases/saleor_discounts.py) · [Observation](observations/saleor-discounts.json) |
| Ion-exchange neural-mass simulation | The last cached sample matches the duration requested. The original short sample and the full request with cache reuse bypassed establish the comparison. | [Code](cases/scientific_simulation.py) · [Observation](observations/scientific-simulation.json) |
| MiroFish | Both distinct planned posts reach the simulation recorder exactly once. The log's success count matches the handoff. A single-post run checks the recorder. | [Code](cases/social_media_simulation.py) · [Observation](observations/social-media-simulation.json) |
| VROOM | A zero distance limit needs usable distances before jobs can be assigned. In the separate time-limit case, the checker divides the supplied route time by three and checks the 1,803-second cap. | [Code](cases/vehicle_routing.py) · [Observation](observations/vehicle-routing.json) |
| OpenAqua | Recommendations honor the excluded step. Full coverage does not credit either of the two explicitly contradicted options. The accepted case can be found after its index rebuild. | [Code](cases/water_treatment_research.py) · [Observation](observations/water-treatment-research.json) |

## Check a different build

Take fresh measurements for the same setup and comparison controls described on the case page. Copy its observation file, keep the case and scenario identifiers, and replace the measurements with the values you observed. Run the checker against that file, for example:

```sh
python3 check.py saleor-discounts my-saleor-observation.json
```

Use measured counts and amounts, including zero. A missing measurement should be omitted so the checker returns INCONCLUSIVE. For the MiroFish, SDK and Bombadil cases, assign the same neutral ID to the same item across observations. Preserve duplicates. In Bombadil, label the three first-time public names `name-01` through `name-03` in observation order. Reuse their labels in the component run and number its nine additional names from 04 through 12. For OpenEMR, only the change in selection, the edit flag, the prompt count and the navigation decision are needed. Synthetic selection labels are sufficient.

For OpenAqua, `reference-A` identifies the recorded “Adsorptive Media” entry and `reference-B` identifies “Aeration and Air Stripping”. Both source entries describe the option as ineffective in the tested context. `credited_option_ids` contains the options the software counted as removal steps. An empty prohibited-options list represents a completed response with no viable option. Record index membership by looking up the submitted ID after the rebuild has finished. The record count alone cannot establish membership.

For VROOM, `supplied_route_seconds` is the sum of input leg times on the route actually returned, before applying the requested speed factor. A repaired planner can choose a shorter route, leave jobs unassigned, or explicitly request the missing distances. When it returns no route under the time limit, record zero jobs and null durations. The unconstrained run must still assign both jobs.

### The saved Saleor fix

The original case page measures the two portions of a $1.01 discount. A separate saved verification measures the total returned on a one-cent order through Saleor's tax response. The same conservation rule applies to both. The one-cent order also has an independently measured two-cent control.

| Recorded state | One-cent order returned | Two-cent control returned | Checker result |
| --- | ---: | ---: | --- |
| [Original source](observations/saleor-one-cent-original.json) | 2¢ | 2¢ | FAIL |
| [Locally fixed source](observations/saleor-one-cent-fixed.json) | 1¢ | 2¢ | PASS |
| [Fix reverted locally](observations/saleor-one-cent-reverted.json) | 2¢ | 2¢ | FAIL |

The ten other case pages have original observations and controls. Establishing a fix on another build requires measurements from that build. The package evaluates supplied observations offline. The [case record](records.json) binds each included observation to its reviewed write-up and audited snapshot by SHA-256. It includes an upstream revision where the case page identifies one.

To run the checker tests, use `python3 -m unittest discover -s tests -v`. The tests include synthetic conforming and malformed inputs to exercise PASS, FAIL and INCONCLUSIVE.
