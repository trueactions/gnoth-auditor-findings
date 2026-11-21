# The log showed two successes and the test recorded one submission

A test supplied two posts from the same simulated account. Both were logged as successful. The test recorder captured one submission.

## What should have happened

If two distinct actions are logged as successful, the activity count should reflect two distinct submissions. Logs should describe the actions that were actually passed on.

## What Auditor observed

The test supplied two different posts under one simulated account. The program kept its pending actions by account. The second action replaced the first pending action before submission, although each produced a success entry. A test recorder at the point of submission captured one action. The two success entries remained in the log.

## Why it matters

A report or analysis that relies on the success entries could overstate the amount of activity the simulator received.

## What was tested

The saved check exercised the code that prepares and submits the initial actions using a test recorder in place of the simulator. It covered the actions passed on and the logs printed alongside them. The audit was run on November 10, 2026 using GNOTH Auditor 2.1.3.

- Audited copy SHA-256 `f32beb9a0485a5a189ec373c3ed6305517f5a2fbeff099b63b26532c23fe0cce`
- [Upstream MiroFish project](https://github.com/666ghj/MiroFish)
