"""Conservation of one USD fixed discount, expressed in integer cents."""

from core import Scenario, control, require, rule


def conserved(label, cents, allocated, compare):
    return compare(label, allocated == cents, f"discount {cents} cents, allocated {allocated} cents")


def check_page(o):
    even, odd, zero = o["one_dollar"], o["one_dollar_one_cent"], o["zero_shipping"]
    require(all(n >= 0 for pair in (even, odd, zero) for n in pair.values())
            and o["direct_net_cents"] >= 0, "Amounts must be nonnegative integer cents")
    return [
        control("One dollar split evenly on equal bases", even["merchandise"] == even["shipping"] == 50,
                f"expected 50 + 50 cents, observed {even['merchandise']} + {even['shipping']}"),
        control("Zero shipping leaves the full discount on merchandise",
                zero["merchandise"] == 101 and zero["shipping"] == 0,
                f"expected 101 + 0 cents, observed {zero['merchandise']} + {zero['shipping']}"),
        control("Direct subtraction on the same total", o["direct_net_cents"] == 2000 - 101,
                f"expected 1899 cents, observed {o['direct_net_cents']}"),
        conserved("Split portions sum to the entered discount", 101, odd["merchandise"] + odd["shipping"], rule),
    ]


def check_one_cent(o):
    # This retained fix check measured the sum, while the case-page run retained both portions.
    require(all(value >= 0 for value in o.values()), "Amounts must be nonnegative integer cents")
    return [
        conserved("Two-cent control", 2, o["two_cent_control_total"], control),
        conserved("One-cent split conserves the discount", 1, o["one_cent_split_total"], rule),
    ]


PORTIONS = {"merchandise": int, "shipping": int}
SCENARIOS = {
    "case-page": Scenario({"one_dollar": PORTIONS, "one_dollar_one_cent": PORTIONS,
                           "zero_shipping": PORTIONS, "direct_net_cents": int}, check_page),
    "one-cent-recheck": Scenario({"two_cent_control_total": int, "one_cent_split_total": int}, check_one_cent),
}
