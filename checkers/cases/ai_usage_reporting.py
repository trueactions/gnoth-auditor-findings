"""AITRA Meter. Preserve independent counters across ingestion order and reader restart."""

from core import Scenario, control, require, rule


def check(o):
    parts = o["engine_counters"]
    require(len(parts) == 2 and all(n > 0 for n in parts) and parts[0] != parts[1],
            "Supply two unequal positive counts for the same model on distinct engines")
    require(all(o[k] >= 0 for k in SHAPE if k != "engine_counters"), "A token count is negative")
    total = sum(parts)
    out = [control("One counter with the combined input", o["single_record_total"] == total,
                   f"expected {total}, read {o['single_record_total']}")]
    for field, label in [("forward_total", "Two counters"), ("reverse_total", "Reversed counters"),
                         ("fresh_reverse_total", "Reversed counters in a fresh reader")]:
        out.append(rule(label, o[field] == total, f"expected {total}, read {o[field]}"))
    return out


SHAPE = {"engine_counters": [int], "single_record_total": int, "forward_total": int,
         "reverse_total": int, "fresh_reverse_total": int}
SCENARIOS = {"case-page": Scenario(SHAPE, check)}
