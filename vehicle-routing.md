# VROOM assigned two jobs when it had no distances to check against a vehicle’s limit

VROOM plans routes for fleets. A dispatcher can give it jobs, travel times between stops and a maximum distance for a vehicle. Knowing that one stop is ten minutes from another tells the planner how to schedule it. To check whether the route is within a distance limit, it also needs to know how far apart the stops are. [VROOM project](https://github.com/VROOM-Project/vroom).

Trueactions AI used GNOTH Auditor to ask what happens when a routing request supplies the times and sets a distance limit, but leaves out the distances. A dispatcher reading an assigned route would reasonably expect the planner to have checked that limit.

## The same two jobs and the same distance limit

Auditor used a two-job example from the project. It set the vehicle’s maximum distance to zero, so even one positive-distance leg would exceed the limit. The controlled runs kept the jobs, times and limit fixed.

| Distance information supplied | What the routing engine did |
| --- | --- |
| Travel times only | Assigned both jobs to the vehicle. |
| Travel times plus explicit positive distances between stops | Left both jobs unassigned. |

The routing engine treated missing distances as zero. The comparison explains why the jobs fit in the first run and fell outside the limit in the second. A planner could request the missing distances or report that it cannot check the limit. Here it returned a route that looked usable. The positive distances were test inputs, so the audit establishes no road mileage for this route.

## A separate check on the time limit

In another run, the planner accepted a route under a **1,803-second limit** and reported **1,802 seconds**. The times supplied for that route added up to 5,461 seconds before the requested threefold speed adjustment. Dividing by three gives **1,820⅓ seconds**, over the limit. The solver rounded its speed conversion before applying it to the journey. Both figures describe the model’s supplied travel times. [Audited upstream revision](https://github.com/VROOM-Project/vroom/tree/877c2dd572fb780ab95a6b546fddacc6f474d71e).

## Audit record

On November 19, 2026, Auditor exercised the compiled C++ routing core in an offline test. The shipped command-line program, external routing services and a dispatcher’s production workflow were outside the run. The saved report records the distance and time checks as findings F1 and F2.

- Audited copy SHA-256 `205facf326aa79f979ca9f729bde2828d57bba1dbcdd524843542a7885b201e7`
- [How GNOTH Auditor checks outcomes](README.md#what-an-outcome-audit-checks) · [All audited repositories](README.md#audited-repositories)

## Check the recorded result

Read the [Python checker](checkers/cases/vehicle_routing.py) to see which rule it tests. The [recorded observation](checkers/observations/vehicle-routing.json) contains the measurements from this audit.

From the top folder of this repository, run the checker with Python 3.8 or later. It reads the saved measurements and runs offline.

```sh
python3 checkers/check.py vehicle-routing checkers/observations/vehicle-routing.json
```

The expected last line is `FAIL` (exit code 1). The control checks pass, and the checker identifies where the measured outcome broke the rule. Checking a different version of the project requires measurements from that version.
