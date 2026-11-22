"""Compare the same five declaration identities at listing, startup and scanning."""

from collections import Counter
from core import Scenario, control, require, rule


def check(o):
    expected = Counter(o["catalog_ids"])
    require(len(expected) == 5 and sum(expected.values()) == 5,
            "The catalog for this comparison must contain five distinct IDs")
    results = []
    for key, label in [("file", "Catalog file control"), ("parent", "Parent layout control"),
                       ("direct", "Direct directory")]:
        row = o[key]
        require(row["listed_count"] >= 0, "Catalog size must be nonnegative")
        compare = rule if key == "direct" else control
        passed = (row["exit_status"] == 0 and row["listed_count"] == 5
                  and Counter(row["emitted_ids"]) == expected)
        results.append(compare(label, passed,
                               f"expected the five catalog IDs, listed {row['listed_count']}, "
                               f"emitted {sorted(row['emitted_ids'])}, exit {row['exit_status']}"))
    ordinary, alternate = o["ordinary_import"], o["alternate_import"]
    results.extend([
        control("Ordinary import runs and lists the catalog checks",
                Counter(ordinary["runtime_ids"]) == expected == Counter(ordinary["scanned_ids"]),
                f"runtime {sorted(ordinary['runtime_ids'])}, scanned {sorted(ordinary['scanned_ids'])}"),
        control("Alternate import runs the same five checks", Counter(alternate["runtime_ids"]) == expected,
                f"expected {sorted(expected)}, runtime {sorted(alternate['runtime_ids'])}"),
        rule("Scanner inventories every check exercised with the alternate import",
             Counter(alternate["scanned_ids"]) == Counter(alternate["runtime_ids"]),
             f"runtime {sorted(alternate['runtime_ids'])}, scanned {sorted(alternate['scanned_ids'])}"),
    ])
    return results


STARTUP = {"listed_count": int, "emitted_ids": [str], "exit_status": int}
SCAN = {"runtime_ids": [str], "scanned_ids": [str]}
SHAPE = {"catalog_ids": [str], "file": STARTUP, "parent": STARTUP, "direct": STARTUP,
         "ordinary_import": SCAN, "alternate_import": SCAN}
SCENARIOS = {"case-page": Scenario(SHAPE, check)}
