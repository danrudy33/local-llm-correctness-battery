# Smart, not just fast — a correctness battery for local LLMs

> [!WARNING]
> **RESULTS WITHDRAWN PENDING GRADING AUDIT — November 25, 2026.**
> We found errors in our automatic grader that can penalize correct answers and may also award undeserved credit. The previously published scores, rankings, honesty-gate labels and comparative conclusions are not validated and should not be cited or used for model, engine or hardware purchasing decisions. We have removed them from the current results files while we recheck the saved responses. No replacement ranking is available yet.

## What needs correcting

Confirmed examples include:
- A correct, explicitly conditional answer was marked wrong even though it acknowledged that the supplied facts did not determine the answer.
- A valid debugging counterexample was rejected because it differed from the grader's preferred example.
- Correct maximum-loss answers expressed as negative profit/loss were penalized against positive loss-magnitude gold values.

The review also covers numeric tolerances, false-positive scoring, ambiguous questions, and separating delivery failures (truncation or HTTP errors) from incorrect reasoning. It applies across all previously tested configurations, not just the newest one. Original local answers and historical scores are being preserved; corrected results will be versioned and accompanied by a change log after verification.

**We withdraw the earlier conclusions that oMLX is more correct than TensorFold, that a particular model is the overall winner, or that a two-Mac setup does not earn its complexity.** This experiment did not isolate engine causality or matched hardware scaling, and the unreliable scoring cannot support those conclusions.

## Why this project exists

The aim is a useful everyday local assistant: correct answers, appropriate uncertainty, practical response times and manageable hardware requirements. Token throughput is valuable, but does not by itself establish task correctness. This is a small exploratory battery, not a validated intelligence benchmark.

## Questions remain available for feedback

[`CASES-v2.json`](CASES-v2.json) contains 15 draft questions, proposed gold answers and rubrics covering finance, coding, logic, calibration and document integration. **The rubric is under review.** The document tasks are short multi-fact exercises, not a validated large-context stress test.

The public question file contains edited/generalized prompts and is not an exact immutable copy of every prompt used in the historical runs. In particular, the Einstein wording and return-policy examples were edited after those runs. Do not attach the withdrawn scores to these edited prompts as though they were the tested version. The audit uses the exact saved original prompts and responses.

## Files and current status

- `results.json` — machine-readable withdrawal notice; no active rankings.
- `index.html` — the same public correction notice.
- `CASES-v2.json` — draft questions/gold/rubrics for discussion, not certified scoring ground truth.
- `battery_v2_run.py` / `battery_v2_grade.py` — original experimental tooling, not yet repaired or validated. The grader executes model-provided Python; do not run it on untrusted responses without isolation.

## Coverage and unavailable configurations

The original publication covered Qwen3.8-Flash-Next at 4/6-bit on oMLX, Qwen 6-bit on TensorFold 1.3.4, GLM-5.3-Flash 4-bit on oMLX and TensorFold+DFlash2, and GLM 6-bit over two-Mac Tandem. The ongoing audit additionally includes Qwen TFQ3 on TensorFold 1.3.5. These are coverage descriptions, not a ranking.

- **DeepSeek-V4.1-Flash:** a previously tested low-quant configuration had problematic outputs. Other candidate checkpoint/runtime combinations were not qualified here. This is not evidence that DeepSeek generally cannot run or is intrinsically unsuitable; a reproducible compatible recipe is welcome.
- **GLM-5.3-Flash 6-bit single-Mac:** not measured with the owned tandem-oriented artifact.
- **Full GLM-5.3 on a 512 GB Mac and EXO:** planned/unmeasured here, not failed benchmark results.

Suggestions for better questions, clearer rubrics and established correctness benchmarks are welcome. Thank you for helping us catch problems before drawing stronger conclusions.
