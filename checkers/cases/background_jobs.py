"""RD-Agent. A known failed child task must signal failure to its caller."""

from core import Scenario, control, rule


def check(o):
    c, t = o["comparison"], o["handler"]
    return [
        control("Same startup error in both observations", c["error"] == t["error"],
                f"comparison {c['error']}, handler {t['error']}"),
        control("Propagated task error produces a failure status", c["exit_status"] != 0,
                f"expected nonzero, process returned {c['exit_status']}"),
        rule("Failed task signals failure at the process boundary", t["exit_status"] != 0,
             f"expected nonzero, process returned {t['exit_status']}"),
        rule("Status reader sees the task failure", t["reader_status"] != 0,
             f"expected nonzero, reader returned {t['reader_status']}"),
    ]


SHAPE = {"comparison": {"error": str, "exit_status": int},
         "handler": {"error": str, "exit_status": int, "reader_status": int}}
SCENARIOS = {"case-page": Scenario(SHAPE, check)}
