"""OpenEMR. A declined departure should protect a changed, unsaved answer."""

from core import Scenario, control, require, rule


def check(o):
    edit, c = o["optional_edit"], o["direct_handler_control"]
    require(edit["prompts"] >= 0 and c["prompts"] >= 0, "Prompt counts must be nonnegative")
    return [
        control("Optional answer really changed", edit["before"] != edit["after"],
                f"before {edit['before']}, after {edit['after']}"),
        control("Direct scored-answer handler enables the normal declined-exit behavior",
                c["dirty"] and c["prompts"] >= 1 and not c["exit_selected"],
                f"edited {c['dirty']}, prompts {c['prompts']}, exit {c['exit_selected']}"),
        rule("Optional edit is recognized", edit["dirty"], f"edited flag {edit['dirty']}"),
        rule("Form prompts and honors the declined exit", edit["prompts"] >= 1 and not edit["exit_selected"],
             f"expected a prompt and no exit, observed {edit['prompts']} prompts and exit {edit['exit_selected']}"),
    ]


EXIT = {"dirty": bool, "prompts": int, "exit_selected": bool}
SHAPE = {"optional_edit": {"before": str, "after": str, **EXIT}, "direct_handler_control": EXIT}
SCENARIOS = {"case-page": Scenario(SHAPE, check)}
