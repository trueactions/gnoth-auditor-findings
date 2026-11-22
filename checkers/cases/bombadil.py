"""Distinguish a first action registration from a genuine repeat, at two API levels."""

from core import Scenario, control, require, rule


def check(o):
    public, component = o["public_interface"], o["component"]
    outcomes = [public["ordinary_first"], public["ordinary_repeat"], component["ordinary_first"],
                *public["first_time"].values(), *component["first_time"].values()]
    require(all(value in {"accepted", "duplicate", "other_error"} for value in outcomes),
            "Registration outcomes must be accepted, duplicate, or other_error")
    results = [
        control("Public interface accepts an ordinary first registration",
                public["ordinary_first"] == "accepted", public["ordinary_first"]),
        control("Public interface identifies a genuine repeat",
                public["ordinary_repeat"] == "duplicate", public["ordinary_repeat"]),
        control("Lower-level component accepts an ordinary first registration",
                component["ordinary_first"] == "accepted", component["ordinary_first"]),
    ]
    for label, rows in [("Public interface", public["first_time"]), ("Lower-level component", component["first_time"])]:
        rejected = [f"{key} ({rows[key]})" for key in sorted(rows) if rows[key] != "accepted"]
        results.append(rule(f"{label} admits each previously unused name", not rejected,
                            f"expected {len(rows)} accepted, observed {len(rows) - len(rejected)}"
                            + (f", rejected {', '.join(rejected)}" if rejected else "")))
    return results


# Stable neutral IDs preserve overlap between the two tests. The ordinary-name controls are separate.
PUBLIC_IDS = ("name-01", "name-02", "name-03")
COMPONENT_IDS = tuple(f"name-{n:02d}" for n in range(1, 13))
SHAPE = {
    "public_interface": {"ordinary_first": str, "ordinary_repeat": str,
                         "first_time": {i: str for i in PUBLIC_IDS}},
    "component": {"ordinary_first": str, "first_time": {i: str for i in COMPONENT_IDS}},
}
SCENARIOS = {"case-page": Scenario(SHAPE, check)}
