"""Run with Python 3.8 or later. Uses only the standard library."""

import argparse
import hashlib
import sys
from importlib import import_module
from pathlib import Path

from core import decode_json, evaluate, read_json


ROOT = Path(__file__).resolve().parent
CASES = (
    "ai-usage-reporting", "antithesis-python-sdk", "background-jobs", "bombadil",
    "investment-research", "openemr-form-changes", "saleor-discounts", "scientific-simulation",
    "social-media-simulation", "vehicle-routing", "water-treatment-research",
)
EXAMPLES = [(case, case + ".json", "FAIL") for case in CASES] + [
    ("saleor-discounts", "saleor-one-cent-original.json", "FAIL"),
    ("saleor-discounts", "saleor-one-cent-fixed.json", "PASS"),
    ("saleor-discounts", "saleor-one-cent-reverted.json", "FAIL"),
]
EXIT = {"PASS": 0, "FAIL": 1, "INCONCLUSIVE": 2}


def run(case, path, recorded_digest=None):
    try:
        data = path.read_bytes()
        if recorded_digest is not None and hashlib.sha256(data).hexdigest() != recorded_digest:
            raise ValueError("Recorded observation digest changed")
        scenarios = import_module("cases." + case.replace("-", "_")).SCENARIOS
        return evaluate(case, scenarios, decode_json(data))
    except (ValueError, OSError, RecursionError) as exc:
        return "INCONCLUSIVE", [str(exc)]


def show(verdict, rows):
    for row in rows:
        if isinstance(row, str):
            print(f"  INPUT ERROR  {row}")
        else:
            state = "OK" if row.passed else "MISMATCH"
            print(f"  {row.kind.upper()} {state}  {row.label}: {row.detail}")
    print(verdict)


def verify_examples():
    try:
        index = read_json(ROOT / "records.json")
    except (OSError, ValueError) as exc:
        print(f"Cannot read the recorded observation index. {exc}", file=sys.stderr)
        return 1
    matched = 0
    for case, name, expected in EXAMPLES:
        path = ROOT / "observations" / name
        try:
            digest = index[case]["observations"][name]
            if not isinstance(digest, str) or len(digest) != 64:
                raise ValueError("invalid SHA-256 entry")
        except (KeyError, TypeError, ValueError) as exc:
            print(f"{name} — missing or invalid case record ({exc})")
            continue
        verdict, rows = run(case, path, recorded_digest=digest)
        # Each archived failing example violated every outcome rule it illustrates.
        # Check every control and rule so a partial reproduction cannot silently pass this test.
        exact = verdict == expected and all(r.passed == (r.kind == "control" or expected == "PASS")
                                            for r in rows)
        print(f"{name}: {verdict} (expected {expected})" + ("" if exact else " [mismatch]"))
        if exact:
            matched += 1
        else:
            show(verdict, rows)
    print(f"{matched}/{len(EXAMPLES)} recorded observations matched every expected rule and control.")
    return 0 if matched == len(EXAMPLES) else 1


def main():
    parser = argparse.ArgumentParser(description="Check independently measured outcomes for the eleven case pages.")
    choice = parser.add_mutually_exclusive_group()
    choice.add_argument("--list", action="store_true", help="list the case identifiers")
    choice.add_argument("--verify-examples", action="store_true", help="compare the archived observations with their expected results")
    parser.add_argument("case", choices=CASES, nargs="?")
    parser.add_argument("file", nargs="?", type=Path, help="fresh observation JSON (defaults to the recorded case example)")
    args = parser.parse_args()
    if (args.list or args.verify_examples) and args.case:
        parser.error("choose a case or a listing/verification option")
    if args.list:
        print("\n".join(CASES))
        return 0
    if args.verify_examples:
        return verify_examples()
    if not args.case:
        parser.error("choose a case, --list, or --verify-examples")
    path = args.file or ROOT / "observations" / (args.case + ".json")
    verdict, rows = run(args.case, path)
    show(verdict, rows)
    return EXIT[verdict]


if __name__ == "__main__":
    sys.exit(main())
