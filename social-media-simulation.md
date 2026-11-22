# A social-media simulation logged two successes and submitted one action

MiroFish lets a user set up simulations in which artificial accounts interact. The simulation can start with a list of initial events, such as two posts assigned to one simulated account. Those starting events shape what the rest of the simulated accounts encounter. A researcher or analyst needs the actions submitted to the simulator and the count in the activity log to agree. [Upstream MiroFish project](https://github.com/666ghj/MiroFish).

We used **GNOTH Auditor**, Trueactions AI’s product for checking whether software delivers the results people rely on, to compare the initial events the application recorded with the actions it handed off. [How an outcome audit works](README.md#what-an-outcome-audit-checks).

## Following two posts through the software

Auditor supplied **two distinct posts for the same simulated account** and ran the existing code that prepares and submits those starting actions. A test recorder stood in for the simulator and captured the actions it received. The log printed two successful post messages. The recorder captured one submission containing the second post.

| Point in the workflow | Count |
| --- | ---: |
| Distinct starting posts specified in the test | 2 |
| Successful post entries in the application log | 2 |
| Actions captured at the handoff to the simulator | 1 |

## What Auditor verified

The program reserved one pending slot per account. The second post replaced the first before the handoff, even though both produced success messages. Comparing the log with the captured submission revealed the missing post.

An analyst counting logged activity could overstate what the simulator was asked to process. The audit measured the preparation and handoff code with a recorder. The simulation engine’s subsequent behavior and any live social platform activity were outside the check.

## Audit record

The saved check ran on November 10, 2026, using GNOTH Auditor 2.1.3 and captured the call arguments at the simulator boundary.

- Audited copy SHA-256 `f32beb9a0485a5a189ec373c3ed6305517f5a2fbeff099b63b26532c23fe0cce`

## Check the recorded result

Read the [Python checker](checkers/cases/social_media_simulation.py) to see which rule it tests. The [recorded observation](checkers/observations/social-media-simulation.json) contains the measurements from this audit.

From the top folder of this repository, run the checker with Python 3.8 or later. It reads the saved measurements and runs offline.

```sh
python3 checkers/check.py social-media-simulation checkers/observations/social-media-simulation.json
```

The expected last line is `FAIL` (exit code 1). The control checks pass, and the checker identifies where the measured outcome broke the rule. Checking a different version of the project requires measurements from that version.
