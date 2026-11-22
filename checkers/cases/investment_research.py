"""TradingAgents. Preserve the author's explicit decision through the report header."""

from core import Scenario, control, rule


def check(o):
    def rating(field, expected, label, compare):
        actual = o[field]
        return compare(label, actual.strip().casefold() == expected.casefold(),
                       f"expected {expected}, read {actual}")

    return [
        rating("hold_with_buy_quote", "Hold", "Hold with quoted Buy", control),
        rating("no_rating", "Review", "Fallback without a rating or a quote", control),
        rating("review_with_buy_quote", "Review", "Parsed Review with quoted Buy", rule),
        rating("review_report_header", "Review", "Displayed decision for that same text", rule),
    ]


SHAPE = {"hold_with_buy_quote": str, "no_rating": str, "review_with_buy_quote": str,
         "review_report_header": str}
SCENARIOS = {"case-page": Scenario(SHAPE, check)}
