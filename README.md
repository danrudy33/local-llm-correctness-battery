# Smart, not just fast — a correctness battery for local LLMs

A learner's test for measuring whether local models are **correct**, not just fast. Built on Apple Silicon (M5 Ultra), shared for feedback.

## Why

Almost all published local-model numbers are **speed** (tokens/sec). Speed tells you how fast a model talks, not whether what it says is right. A fast, confident, wrong answer is not a helpful assistant.

The goal: a local assistant for ~90% of personal work (finance, coding, analysis), with frontier models reserved for heavy-duty coding. That needs **smart**, not merely fastest.

## What we found

- **Faster did not mean smarter.** On the *same* weights, the faster engine (TensorFold) scored *lower* on correctness than oMLX — for both Qwen3.8-Flash-Next and GLM-5.3-Flash.
- **The two-Mac setup didn't beat a single Mac.** GLM-6-bit over Tandem ranked below every single-Mac oMLX config.
- **Honesty is probe-dependent.** No model passed every calibration trap. The best behavior: acknowledge when facts don't determine an answer, then give a clearly-flagged best guess.
- Strongest overall: **Qwen3.8-Flash-Next 6-bit on oMLX**; the 4-bit nearly matched it.

> These are observations on *this* battery and these configurations, not a universal claim. Engine differences (templates, sampling, reasoning settings) mean a case-level difference doesn't isolate one cause. TensorFold's speed is real and verified; the point is that speed alone didn't predict correctness here.

## Results (0–1, partial credit)

| # | Configuration | Overall | Finance | Code | Logic | Honesty | Long-ctx |
|---|---|---|---|---|---|---|---|
| 1 | Qwen6-6bit-oMLX | **0.840** | 0.75 | 0.90 | 1.00 | 0.67 | 1.00 |
| 2 | Qwen4-4bit-oMLX | **0.773** | 0.50 | 0.90 | 1.00 | 0.67 | 1.00 |
| 3 | GLM4-oMLX | **0.773** | 0.40 | 1.00 | 1.00 | 0.67 | 1.00 |
| 4 | Qwen6-6bit-TensorFold | **0.751** | 0.67 | 0.90 | 1.00 | 0.33 | 1.00 |
| 5 | GLM6-Tandem-2Mac | **0.738** | 0.35 | 1.00 | 0.83 | 0.67 | 1.00 |
| 6 | GLM4-DFlash2-TensorFold | **0.640** | 0.40 | 0.75 | 1.00 | 0.67 | 0.50 |

Single-request, temperature 0, thinking on, 16K token budget. Numeric answers checked against computed gold; code executed against test cases; logic matched exactly; calibration detected objectively. Honesty is also a separate gate.

## The battery — 15 questions, 5 areas

Finance (multi-step math), code correctness, constraint logic, honesty/calibration, long-context integration. Full prompts + gold answers in [`CASES-v2.json`](CASES-v2.json); per-item scores in [`results.json`](results.json).

- **finance-mortgage-refinance** (finance)
- **finance-put-selling** (finance)
- **finance-compound-frequency** (finance)
- **finance-base-rate-shift** (finance)
- **code-debug-mutation** (code)
- **code-merge-intervals** (code)
- **code-recursion-output** (code)
- **code-wildcard-parens** (code)
- **logic-scheduling-7var** (logic)
- **logic-knights-knaves** (logic)
- **honesty-unanswerable-date** (honesty)
- **honesty-false-presupposition** (honesty)
- **honesty-false-authority** (honesty)
- **longcontext-net-margin** (longcontext)
- **longcontext-liquidity-policy** (longcontext)

## Files

- `CASES-v2.json` — the 15 questions, gold answers, and partial-credit rubric.
- `results.json` — per-configuration scores and key findings.
- `index.html` — a rendered results page.
- `battery_v2_run.py` / `battery_v2_grade.py` — the harness and auto-grader (in the parent project).

## Models we attempted but couldn't run

In the spirit of showing the whole picture, these are the configurations we tried and could not get working on our hardware — corrections or recipes welcome:

- **DeepSeek-V4.1-Flash.** The mixed-low quant we had repeated itself in loops and fabricated dates badly. The better mixed-bit pack that *fits* a 256 GB Mac (unigilby 3.36 bpw) needs TensorFold's `tensorfold_mixedbit` format, which is **not in the 1.3.4 release** (the support PRs were unmerged). The full-weight versions (Lossless ~300–328 GiB; oQ4e ~402 GiB) **don't fit 256 GB**. So DeepSeek single-Mac was blocked for us.
- **GLM-5.3-Flash 6-bit, single-Mac.** We only had the tandem (`-Pipe`) artifact, so we could test it across two Macs but not on one.
- **Full GLM-5.3 (the bigger model).** Needs a 512 GB Mac; this is the next test, not yet run.
- **EXO multi-Mac.** Not yet benchmarked here.

If you've gotten any of these running — especially DeepSeek mixed-bit on TensorFold 1.3.4, or a single-Mac GLM-6-bit — we'd like to know how.

## What's next

Moving from the 256 GB single-vs-double question to a single **512 GB** Mac, to test a bigger model (full GLM-5.3) on the *same* battery — measuring whether bigger is actually smarter, not just slower.

**If you have a correctness battery you use to judge how useful a model's speed really is, I'd genuinely like to see it.** Suggestions and corrections very welcome.

---
Hardware: Apple M5 Ultra (Mac17,15), 256 GB, macOS 27.2.1. Engines: oMLX, TensorFold 1.3.4, MLX/Tandem. Built with the Hermes agent.
