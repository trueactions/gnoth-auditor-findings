"""MiroFish. Reconcile planned post identities, logged success count and actual handoff."""

from collections import Counter
from core import Scenario, control, require, rule


def check(o):
    one, two = o["single_post"], o["same_account_pair"]
    require(len(one["planned"]) == 1 and len(two["planned"]) == 2
            and len(set(two["planned"])) == 2 and one["planned"][0] == two["planned"][0],
            "Use one post, then the same post plus a distinct second post on the same account")
    require(one["logged_successes"] >= 0 and two["logged_successes"] >= 0,
            "Success counts must be nonnegative")
    return [
        control("Single-post handoff and log", one["logged_successes"] == 1
                and one["submitted"] == one["planned"],
                f"planned {one['planned']}, logged {one['logged_successes']}, received {one['submitted']}"),
        rule("Both planned posts reach the recorder exactly once",
             Counter(two["submitted"]) == Counter(two["planned"]),
             f"expected {two['planned']}, received {two['submitted']}"),
        rule("Successful log entries reconcile with submitted actions",
             two["logged_successes"] == len(two["submitted"]),
             f"logged {two['logged_successes']}, received {len(two['submitted'])}"),
    ]


ROW = {"planned": [str], "logged_successes": int, "submitted": [str]}
SCENARIOS = {"case-page": Scenario({"single_post": ROW, "same_account_pair": ROW}, check)}
