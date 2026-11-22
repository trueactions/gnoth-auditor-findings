"""Tests of the checkers. Modifications below are synthetic and describe no upstream fix."""

import copy
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import check
from core import evaluate, read_json


ROOT = Path(check.__file__).parent


def example(case):
    return read_json(ROOT / "observations" / (case + ".json"))


def outcome(case, doc):
    module = check.import_module("cases." + case.replace("-", "_"))
    return evaluate(case, module.SCENARIOS, doc)[0]


def passing_examples():
    docs = {slug: example(slug) for slug in check.CASES}
    o = {slug: d["observation"] for slug, d in docs.items()}
    usage = o["ai-usage-reporting"]
    for key in ("forward_total", "reverse_total", "fresh_reverse_total"):
        usage[key] = sum(usage["engine_counters"])
    sdk = o["antithesis-python-sdk"]
    sdk["direct"]["emitted_ids"] = list(reversed(sdk["catalog_ids"]))
    sdk["alternate_import"]["scanned_ids"] = list(sdk["alternate_import"]["runtime_ids"])
    o["background-jobs"]["handler"].update(exit_status=3, reader_status=3)
    for layer in o["bombadil"].values():
        for name in layer["first_time"]:
            layer["first_time"][name] = "accepted"
    o["investment-research"].update(review_with_buy_quote="REVIEW", review_report_header="Review")
    o["openemr-form-changes"]["optional_edit"].update(dirty=True, prompts=1, exit_selected=False)
    o["saleor-discounts"]["one_dollar_one_cent"].update(merchandise=50, shipping=51)
    sim = o["scientific-simulation"]
    sim["reuse_end_ms"] = sim["full_request_ms"]
    posts = o["social-media-simulation"]["same_account_pair"]
    posts["submitted"] = list(reversed(posts["planned"]))
    route = o["vehicle-routing"]
    route["no_distances"].update(outcome="distances_required", assigned_jobs=0)
    route["time_limited"].update(outcome="no_feasible_route", assigned_jobs=0,
                                 supplied_route_seconds=None, reported_route_seconds=None)
    aqua = o["water-treatment-research"]
    aqua["recommendations"]["prohibited"] = []
    aqua["coverage"]["percent"] = 60
    aqua["index"].update(records_after=930, present_after_rebuild=True)
    return docs


class CheckerTests(unittest.TestCase):
    def test_expected_recorded_examples_and_controls(self):
        with redirect_stdout(io.StringIO()):
            self.assertEqual(check.verify_examples(), 0)

    def test_every_rule_accepts_a_synthetic_conforming_observation(self):
        for slug, doc in passing_examples().items():
            with self.subTest(slug=slug):
                self.assertEqual(outcome(slug, doc), "PASS")

    def test_each_case_requires_its_controls(self):
        docs = passing_examples()
        o = {slug: d["observation"] for slug, d in docs.items()}
        o["ai-usage-reporting"]["single_record_total"] = 0
        o["antithesis-python-sdk"]["file"]["emitted_ids"] = []
        o["background-jobs"]["comparison"]["exit_status"] = 0
        o["bombadil"]["public_interface"]["ordinary_repeat"] = "accepted"
        o["investment-research"]["no_rating"] = "Buy"
        o["openemr-form-changes"]["direct_handler_control"]["prompts"] = 0
        o["saleor-discounts"]["zero_shipping"]["shipping"] = 1
        o["scientific-simulation"]["bypass_end_ms"] = 8000
        o["social-media-simulation"]["single_post"]["submitted"] = []
        o["vehicle-routing"]["unconstrained_jobs"] = 0
        o["water-treatment-research"]["index"]["control_parsed_ids"] = []
        for slug, doc in docs.items():
            with self.subTest(slug=slug):
                self.assertEqual(outcome(slug, doc), "INCONCLUSIVE")

    def test_incomplete_controls_take_precedence_over_a_rule_mismatch(self):
        doc = example("saleor-discounts")
        doc["observation"]["one_dollar"]["shipping"] = 51
        self.assertEqual(outcome("saleor-discounts", doc), "INCONCLUSIVE")

    def test_fresh_outcome_cannot_omit_an_entire_case_measurement(self):
        for slug in check.CASES:
            doc = example(slug)
            del doc["observation"][next(iter(doc["observation"]))]
            with self.subTest(slug=slug), self.assertRaises(ValueError):
                outcome(slug, doc)

    def test_same_count_with_wrong_identities_is_still_a_failure(self):
        docs = passing_examples()
        posts = docs["social-media-simulation"]["observation"]["same_account_pair"]
        posts["submitted"] = [posts["planned"][1]] * 2
        self.assertEqual(outcome("social-media-simulation", docs["social-media-simulation"]), "FAIL")
        sdk = docs["antithesis-python-sdk"]["observation"]
        sdk["direct"]["emitted_ids"][1] = sdk["direct"]["emitted_ids"][0]
        self.assertEqual(outcome("antithesis-python-sdk", docs["antithesis-python-sdk"]), "FAIL")

    def test_reference_and_membership_are_independent_of_other_openaqua_results(self):
        slug = "water-treatment-research"
        doc = passing_examples()[slug]
        o = doc["observation"]
        o["recommendations"]["prohibited"] = [{"status": "PASS", "requires_dosing": False}]
        o["index"]["records_after"] = o["index"]["records_before"]
        self.assertEqual(outcome(slug, doc), "PASS")
        o["coverage"]["percent"] = 100
        self.assertEqual(outcome(slug, doc), "FAIL")
        o["coverage"]["credited_option_ids"] = ["independently-supported-option"]
        self.assertEqual(outcome(slug, doc), "PASS")
        o["index"].update(records_after=931, present_after_rebuild=False)
        self.assertEqual(outcome(slug, doc), "FAIL")

    def test_a_different_feasible_route_and_an_exact_fractional_limit(self):
        slug = "vehicle-routing"
        doc = passing_examples()[slug]
        route = doc["observation"]["time_limited"]
        route.update(outcome="plan", assigned_jobs=1, reported_route_seconds=1802, supplied_route_seconds=5408)
        self.assertEqual(outcome(slug, doc), "PASS")
        route.update(reported_route_seconds=1803, supplied_route_seconds=5410)
        self.assertEqual(outcome(slug, doc), "FAIL")
        route["supplied_route_seconds"] = None
        with self.assertRaises(ValueError):
            outcome(slug, doc)

    def test_either_portion_can_receive_the_extra_cent(self):
        slug = "saleor-discounts"
        doc = passing_examples()[slug]
        doc["observation"]["one_dollar_one_cent"].update(merchandise=51, shipping=50)
        self.assertEqual(outcome(slug, doc), "PASS")

    def test_cli_reports_distinct_status_codes_for_real_and_invalid_inputs(self):
        slug = "saleor-discounts"
        doc = example(slug)
        malformed = []
        for key, bad in [("case", "bombadil"), ("scenario", "unsupported")]:
            v = dict(doc, **{key: bad})
            malformed.append(json.dumps(v))
        for bad in [False, "51", 51.0, -1]:
            v = copy.deepcopy(doc)
            v["observation"]["one_dollar_one_cent"]["shipping"] = bad
            malformed.append(json.dumps(v))
        malformed.extend(['{"case": 1, "case": 2}', "{", "NaN"])
        def run(path):
            return subprocess.run([sys.executable, "-B", str(ROOT / "check.py"), slug, str(path)],
                                  capture_output=True, text=True)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "new.json"
            self.assertEqual(run(path).returncode, 2)
            for raw in malformed:
                path.write_text(raw)
                with self.subTest(raw=raw):
                    result = run(path)
                    self.assertEqual(result.returncode, 2)
                    self.assertIn("INCONCLUSIVE", result.stdout)
        for fname, status in [("saleor-discounts.json", 1), ("saleor-one-cent-fixed.json", 0),
                              ("saleor-one-cent-reverted.json", 1)]:
            self.assertEqual(run(ROOT / "observations" / fname).returncode, status)

    def test_changed_bundled_measurement_fails_record_verification(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copy(ROOT / "records.json", root)
            shutil.copytree(ROOT / "observations", root / "observations")
            target = root / "observations/ai-usage-reporting.json"
            target.write_bytes(target.read_bytes() + b"\n")
            with patch.object(check, "ROOT", root), redirect_stdout(io.StringIO()):
                self.assertEqual(check.verify_examples(), 1)


if __name__ == "__main__":
    unittest.main()
