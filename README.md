# AI outcome reliability

**AI outcome reliability** is the extent to which software delivers the business result its users intended, under the conditions and constraints they set. Whether AI writes the code or helps make a decision, the team using the software still owns the outcome. To judge whether people can rely on it, that team needs to make the requirement explicit and compare it with what the application actually did.

**Trueactions AI** brings founder Radhakrishnan Poomari’s more than twenty years of engineering, research and business experience to that question. He developed a deep-learning solution that GE deployed across its turbine fleet through Predix and led technology due diligence for GE’s acquisition of SmartSignal. He began building Auditor after seeing coding agents extend his software while some of the business rules it was built to preserve quietly stopped holding. [Founder’s background](https://trueactions.ai/advisory).

**GNOTH Auditor** is Trueactions AI’s product for independently checking those outcomes. It uses expert knowledge of how systems fail to guide an investigation of an application’s code, data and business context. Each case report in this repository shows what someone needed to rely on, what the software produced, how Auditor traced the discrepancy and what evidence an engineer could use to check a correction.

## What code review can tell you

A good reviewer asks whether a change does what its author intended, how it fits the rest of the system and which cases its tests cover. A reviewer can follow a user setting through the code, spot that another component ignores it and request a test. Review can uncover business-logic errors. An approval by itself cannot establish that every business rule held in the running application. The requirement tells the reviewer what should happen. Evidence from a run shows what happened under the conditions tested. [Google’s code review guide](https://google.github.io/eng-practices/review/reviewer/looking-for.html).

### Where review and testing stand in November 2026

Qodo’s review agents use business requirements and context from related repositories. Greptile’s TREX can run changed code in a sandbox and attach logs or traces to its review. A team can use those capabilities to investigate a business rule during review. [Qodo](https://www.qodo.ai/ai-code-review-platform/) · [Greptile TREX](https://www.greptile.com/blog/trex).

Teams can also use Antithesis to explore executions that might violate a specified rule, or LangSmith to evaluate an AI application’s outputs against chosen criteria. The choice of criterion matters. “Did the workflow finish?” and “Did the result honor the user’s restriction?” give different answers for the very same run. [Antithesis](https://antithesis.com/docs/product/writing_tests/assertions/) · [LangSmith](https://docs.langchain.com/langsmith/evaluation-types).

## What an outcome audit checks

GNOTH Auditor can take a whole application as it stands and work backward from a result someone acts on, even when there is no pending code change. What distinguishes its **neuro-symbolic** approach is how it connects three steps in one investigation.

1. **Find the rule the result depends on.** AI proposes candidate business rules from the application’s code and documentation. A user instruction, a documented requirement or a domain expert can settle what a correct result means.
2. **Put that rule to a test.** Explicit rules and expert knowledge of recurring failures guide the choice of what to challenge. Where the software can be exercised, a deterministic check compares its output with the expectation using the same pass/fail rule each time.
3. **Explain where the result went wrong.** Auditor follows the discrepancy back through the code and records which parts of the workflow ran, so someone else can examine the evidence or turn the finding into a regression test.

In our audit of the original OpenAqua water-treatment planner, the requirement came directly from the request. If chemical dosing was prohibited, the planner should offer a compatible option or say it found none. Auditor ran the same arsenic example with dosing allowed, prohibited and unspecified. All three responses were identical. OpenAqua preserved the setting when it read the request, but its offline planner and its own **PASS** check both ignored it. That gives an engineer a specific place to fix and a test to keep. The finding concerns the software’s recommendation. Establishing whether a treatment works in a plant requires separate evidence.

## Audited repositories

<!-- repository-coverage:start -->

Audit reports are recorded for all **15 repositories**. Across the audited snapshots, GNOTH Auditor indexed **2,859,389 source lines** and **113,420 functions** in **17,662 source files**. It counted **55,642 Python variable names** across the 10 repositories with indexed Python files.

[Open the table in the README file view](README.md#audited-repositories)

| Repository audit | What the project does | GitHub stars / forks | Project files | Source files | Source lines | Functions | No. of variables | Languages |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [VROOM](vehicle-routing.md) (C++) | Plans vehicle routes and assigns jobs to a fleet within scheduling and travel constraints. | [1,924 / 452](https://github.com/VROOM-Project/vroom "GitHub on 2026-11-21") | 208 | 183 | 27,247 | 832 | Not measured | C++, Shell |
| [AITRA Meter](ai-usage-reporting.md) (Go) | Measures the GPU energy that AI workloads on Kubernetes use per output token. | [138 / 73](https://github.com/aitra-ai/aitra-meter "GitHub on 2026-11-21") | 190 | 74 | 11,034 | 505 | Not measured | Go, TypeScript, JavaScript, Shell |
| [TradingAgents](investment-research.md) (Python) | Uses a team of AI agents to analyze market information and produce an investment research report. | [123,397 / 23,636](https://github.com/TauricResearch/TradingAgents "GitHub on 2026-11-21") | 213 | 94 | 13,587 | 473 | 2,064 | Python |
| [RD-Agent](background-jobs.md) (Python) | Automates research and development tasks such as proposing experiments, implementing ideas and evaluating results. | [15,445 / 2,061](https://github.com/microsoft/RD-Agent "GitHub on 2026-11-21") | 920 | 556 | 66,735 | 2,744 | 10,835 | Python, Shell, TypeScript, JavaScript |
| [OpenAqua](water-treatment-research.md) (Python) | Helps water-treatment researchers choose a sequence of treatment steps for a particular water source and its contaminants. | [3 / 0](https://github.com/zhaorui-bi/OpenAqua "GitHub on 2026-11-21") | 1,032 | 42 | 5,411 | 148 | 916 | Python |
| [MiroFish](social-media-simulation.md) (Python) | Simulates how virtual accounts post, respond and interact in a social network. | [86,190 / 13,048](https://github.com/666ghj/MiroFish "GitHub on 2026-11-21") | 128 | 51 | 26,578 | 690 | 2,635 | Python, JavaScript |
| [ion-exchange-neural-mass](scientific-simulation.md) (Python) | Simulates the activity of groups of neurons and reproduces figures from a published neuroscience study. | [3 / 1](https://github.com/grabuffo/ion-exchange-neural-mass "GitHub on 2026-11-21") | 62 | 17 | 1,503 | 43 | 465 | Python, Shell |
| [Antithesis Python SDK](antithesis-python-sdk.md) (Python) | Lets developers declare properties of a Python application and report which checks ran during testing. | [19 / 1](https://github.com/antithesishq/antithesis-sdk-python "GitHub on 2026-11-21") | 49 | 18 | 3,307 | 167 | 397 | Python |
| [Antithesis Bombadil](bombadil.md) (Rust) | Exercises browser interfaces using actions and checks defined by test authors. | [2,997 / 110](https://github.com/antithesishq/bombadil "GitHub on 2026-11-21") | 454 | 182 | 50,595 | 1,878 | 163 | Rust, TypeScript, Python, Lua, JavaScript, C |
| [Saleor](saleor-discounts.md) (Python) | Runs online commerce workflows including checkout, orders, discounts and tax integrations. | [23,593 / 6,217](https://github.com/saleor/saleor "GitHub on 2026-11-21") | 4,731 | 2,632 | 264,896 | 7,820 | 32,560 | Python, Shell |
| [OpenEMR](openemr-form-changes.md) (PHP) | Manages electronic health records and provides forms for recording questionnaire responses. | [5,615 / 3,137](https://github.com/openemr/openemr "GitHub on 2026-11-21") | 10,532 | 4,000 | 1,142,605 | 35,625 | Not measured | PHP, JavaScript, Shell, Perl |
| [frePPLe](https://github.com/frePPLe/frepple/tree/fdecacb2d5c169121e749c0120536ea556c8dcc4) (Python / C++) | Plans supply and production around demand, inventory and capacity. | [785 / 343](https://github.com/frePPLe/frepple "GitHub on 2026-11-25") | 2,209 | 584 | 282,572 | 6,084 | 5,524 | Python, C++, JavaScript, Shell |
| [Kimai](https://github.com/kimai/kimai/tree/382c618f89ffd8add341ab882e1221fa02ce6fcb) (PHP) | Tracks time and expenses and generates invoices for customer projects. | [5,181 / 896](https://github.com/kimai/kimai "GitHub on 2026-11-25") | 2,959 | 1,229 | 109,332 | 6,246 | Not measured | PHP, JavaScript, Shell |
| [Decidim](https://github.com/decidim/decidim/tree/58d3cd2919d37a0a09f216b253f4662453eb1c26) (Ruby) | Supports public participation through proposals, assemblies, elections and budgets. | [1,859 / 498](https://github.com/decidim/decidim "GitHub on 2026-11-25") | 11,772 | 4,000 | 268,987 | 13,238 | Not measured | Ruby, JavaScript |
| [OpenCondo](https://github.com/open-condo-software/condo/tree/a9358a545377764b445c6e0c68fb517567c27c8d) (JavaScript / TypeScript) | Supports property management, resident requests, billing and service workflows. | [436 / 164](https://github.com/open-condo-software/condo "GitHub on 2026-11-25") | 6,252 | 4,000 | 585,000 | 36,927 | 83 | Python, JavaScript, TypeScript, Shell |

Repository names open the published case reports where available and the audited source revisions for the other saved reports. Star and fork counts link to the upstream projects and are dated in each row.

Project files include code, documentation and data in the audit inventory. Source lines include comments and blank lines. Functions are those the parsers recognized. Languages are those represented in the indexed source files. Each repository contributes one snapshot to these totals. Each published case describes the behavior exercised in its snapshot.

Auditor counts names assigned, deleted or used as function parameters in Python files. A distinct name counts once per file, so a name in two files counts twice. “Not measured” means the index contained no Python files.

OpenEMR, Decidim and OpenCondo reached the 4,000-file source index limit. Their indexed counts cover part of each saved snapshot.

The latest OpenCondo audit confirmed a test-fixture false failure. Startup and service smoke checks passed in the prepared environment. End-to-end property management, payment and integration workflows remain unverified.

<!-- repository-coverage:end -->

To use these cases in your own work, pick one result people act on and write down what would make it wrong. For a usage total, reverse the same two records and check that both totals still equal their sum. For a completed action, compare the success log with what the receiving system recorded. Each case links to the upstream project and identifies the software copy and the part of the workflow checked.
