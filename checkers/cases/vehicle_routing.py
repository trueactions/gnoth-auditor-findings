"""VROOM. Check distance feasibility and route time using the supplied travel times."""

from fractions import Fraction
from core import Scenario, control, require, rule


def check(o):
    positive, missing, route = o["positive_distances"], o["no_distances"], o["time_limited"]
    for row in (positive, missing, route):
        require(0 <= row["assigned_jobs"] <= 2, "A result must account for at most two assigned jobs")
    require(missing["outcome"] in {"plan", "distances_required"},
            "Record a completed plan or an explicit request for the missing distances")
    require(route["outcome"] in {"plan", "no_feasible_route"},
            "Record a completed plan or an explicit infeasible-route response")
    require((missing["outcome"] == "plan" or missing["assigned_jobs"] == 0)
            and (route["outcome"] == "plan" or route["assigned_jobs"] == 0),
            "A declined request cannot assign jobs")
    require(positive["unassigned_jobs"] + positive["assigned_jobs"] == 2,
            "The explicit-distance control must account for both jobs")
    raw, reported = route["supplied_route_seconds"], route["reported_route_seconds"]
    for n in (raw, reported):
        require(n is None or n >= 0, "Route times must be nonnegative")
    if route["assigned_jobs"]:
        require(raw is not None and raw > 0 and reported is not None,
                "An assigned route needs positive input leg times and a recorded duration")
        exact = Fraction(raw, 3)
        time_ok = exact <= 1803 and reported <= 1803 and abs(reported - exact) < 1
        detail = f"limit 1803 s, input legs {raw} s / 3 = {exact} s, planner reported {reported} s"
    else:
        require(raw in (None, 0) and reported in (None, 0), "An empty route cannot carry travel time")
        time_ok, detail = True, "no jobs assigned under the time limit"
    return [
        control("Zero distance limit with supplied positive distances", positive["unassigned_jobs"] == 2,
                f"expected both unassigned, observed {positive['unassigned_jobs']}"),
        control("Unconstrained two-job route", o["unconstrained_jobs"] == 2,
                f"expected two assigned, observed {o['unconstrained_jobs']}"),
        rule("Zero distance limit without usable distances", missing["assigned_jobs"] == 0,
             f"expected zero assignments until distances are available, observed {missing['assigned_jobs']}"),
        rule("Assigned travel respects the time limit at the requested speed", time_ok, detail),
    ]


NULLABLE_INT = (int, type(None))
SHAPE = {"positive_distances": {"assigned_jobs": int, "unassigned_jobs": int},
         "no_distances": {"outcome": str, "assigned_jobs": int}, "unconstrained_jobs": int,
         "time_limited": {"outcome": str, "assigned_jobs": int, "supplied_route_seconds": NULLABLE_INT,
                          "reported_route_seconds": NULLABLE_INT}}
SCENARIOS = {"case-page": Scenario(SHAPE, check)}
