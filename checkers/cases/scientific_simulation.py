"""Compare the last sample time with the requested simulated duration, in milliseconds."""

from core import Scenario, control, require, rule


def check(o):
    quick, full = o["quick_request_ms"], o["full_request_ms"]
    require(0 < quick < full and all(n >= 0 for n in o.values()),
            "Durations must be nonnegative and the full request longer than the quick request")
    return [
        control("Short sample originally stored", o["quick_end_ms"] == quick,
                f"requested {quick} ms, sampled through {o['quick_end_ms']} ms"),
        control("Full request with cache bypassed", o["bypass_end_ms"] == full,
                f"requested {full} ms, sampled through {o['bypass_end_ms']} ms"),
        rule("Full request after storing the short sample", o["reuse_end_ms"] == full,
             f"requested {full} ms, sampled through {o['reuse_end_ms']} ms"),
    ]


SHAPE = {k: int for k in ("quick_request_ms", "full_request_ms", "quick_end_ms",
                          "bypass_end_ms", "reuse_end_ms")}
SCENARIOS = {"case-page": Scenario(SHAPE, check)}
