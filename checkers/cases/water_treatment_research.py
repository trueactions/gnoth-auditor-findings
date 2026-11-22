"""OpenAqua software checks for explicit exclusions, reference support and index membership."""

from core import Scenario, control, require, rule


def check(o):
    options = o["recommendations"]
    for group in options.values():
        require(all(row["status"] in {"PASS", "WARN", "FAIL", "DROP"} for row in group),
                "Each returned candidate needs its constraint status")
    prohibited = [row for row in options["prohibited"]
                  if row["requires_dosing"] and row["status"] in {"PASS", "WARN"}]
    c = o["coverage"]
    require(0 <= c["percent"] <= 100, "Coverage must be between 0 and 100 percent")
    credited = set(c["credited_option_ids"])
    # The two retained reference entries explicitly describe these options as ineffective here.
    unsupported = sorted(credited.intersection({"reference-A", "reference-B"}))
    idx = o["index"]
    require(min(idx["records_before"], idx["records_after"]) >= 0, "Index sizes must be nonnegative")
    require(not idx["present_after_rebuild"] or idx["records_after"] > 0,
            "An empty index cannot contain the submitted record")
    results = []
    for key in ("allowed", "unspecified"):
        viable = any(row["status"] == "PASS" for row in options[key])
        results.append(control(f"Example yields a viable option with dosing {key}", viable,
                               f"observed {sum(row['status'] == 'PASS' for row in options[key])} accepted options"))
    results.extend([
        rule("Restriction is respected by every viable recommendation", not prohibited,
             f"expected zero viable options using the prohibited step, observed {len(prohibited)}"),
        rule("Full coverage has credited options consistent with the two reference entries",
             c["percent"] < 100 or (bool(credited) and not unsupported),
             f"coverage {c['percent']}%, credited options contradicted by the references {unsupported}"),
        control("Application acknowledged this submission", idx["acknowledged_records"] == 1,
                f"expected one accepted record, observed {idx['acknowledged_records']}"),
        control("Submitted record is parseable for search", idx["submitted_id"] in idx["control_parsed_ids"],
                f"expected {idx['submitted_id']} in {idx['control_parsed_ids']}"),
        rule("Accepted record is present after the completed rebuild", idx["present_after_rebuild"],
             f"records {idx['records_before']} to {idx['records_after']}, submitted ID present {idx['present_after_rebuild']}"),
    ])
    return results


OPTION = {"status": str, "requires_dosing": bool}
SHAPE = {"recommendations": {key: [OPTION] for key in ("allowed", "prohibited", "unspecified")},
         "coverage": {"percent": int, "credited_option_ids": [str]},
         "index": {"submitted_id": str, "acknowledged_records": int, "control_parsed_ids": [str],
                   "records_before": int, "records_after": int, "present_after_rebuild": bool}}
SCENARIOS = {"case-page": Scenario(SHAPE, check)}
