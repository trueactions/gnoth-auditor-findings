"""Small, offline runner for comparisons of measured software outcomes."""

import json
from collections import namedtuple


Result = namedtuple("Result", "kind label passed detail")
Scenario = namedtuple("Scenario", "shape evaluate")


def control(label, passed, detail):
    return Result("control", label, passed, detail)


def rule(label, passed, detail):
    return Result("rule", label, passed, detail)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def _unique_keys(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"Duplicate JSON key {key!r}")
        result[key] = value
    return result


def _invalid_number(value):
    raise ValueError(f"Invalid JSON number {value}")


def decode_json(data):
    return json.loads(data.decode("utf-8"), object_pairs_hook=_unique_keys, parse_constant=_invalid_number)


def read_json(path):
    return decode_json(path.read_bytes())


def validate(value, shape, path):
    """Check exact object keys, ordered array element types, and uncoerced JSON types."""
    if isinstance(shape, dict):
        require(type(value) is dict, f"{path} must be an object")
        missing = sorted(shape.keys() - value.keys())
        extra = sorted(value.keys() - shape.keys())
        require(not missing and not extra, f"{path}: missing {missing}, unexpected {extra}")
        for key, item in shape.items():
            validate(value[key], item, f"{path}.{key}")
    elif isinstance(shape, list):
        require(type(value) is list, f"{path} must be an array")
        for i, item in enumerate(value):
            validate(item, shape[0], f"{path}[{i}]")
    else:
        allowed = shape if isinstance(shape, tuple) else (shape,)
        names = " or ".join(t.__name__ for t in allowed)
        require(type(value) in allowed, f"{path} must be {names}")
        if type(value) is str:
            require(bool(value.strip()), f"{path} must contain text")


def evaluate(slug, scenarios, document):
    require(type(document) is dict and set(document) == {"case", "scenario", "observation"},
            "Expected a JSON object with case, scenario, and observation")
    require(document["case"] == slug, f"Expected case {slug!r}")
    name = document["scenario"]
    require(type(name) is str and name in scenarios, f"Unknown scenario {name!r} for {slug}")
    scenario = scenarios[name]
    validate(document["observation"], scenario.shape, "observation")
    results = scenario.evaluate(document["observation"])
    if any(not r.passed for r in results if r.kind == "control"):
        return "INCONCLUSIVE", results
    return ("PASS" if all(r.passed for r in results) else "FAIL"), results
