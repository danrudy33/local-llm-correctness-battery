# Smart, not just fast — an exploratory local-LLM battery

> [!IMPORTANT]
> **Corrected results — November 25, 2026 (semantic audit v2).** This revision supersedes the original automated scores and the interim withdrawal. We rechecked all 120 slots across eight configurations, including two new TFQ3 runs. **21 historical question scores changed, including rubric reinterpretations as well as mechanical fixes.** The earlier claims that TensorFold sacrifices correctness for speed or that oMLX is universally better remain withdrawn. This is a small exploratory comparison, not a validated general-intelligence benchmark.

## Why

The goal is a useful local everyday assistant: correct answers, appropriate uncertainty, practical latency and manageable memory. Speed matters, but token throughput alone does not measure usefulness. The aim of covering most personal work is an aspiration, not a finding of this experiment.

## Audited results

All eight configurations received the **same 15 original prompt byte sequences**, temperature 0 and recorded 16K output-token budgets, one pass each. “Qwen” is Qwen3.8-Flash-Next; “GLM” is GLM-5.3-Flash, **not full GLM-5.3**. Hardware: M5 Ultra 256 GB; Tandem uses two such Macs.

| Configuration | Audited task score | Final answers /15 | Median response | E2E output tok/s |
|---|---:|---:|---:|---:|
| Qwen3.8-Flash-Next · TFQ3 · TensorFold 1.3.5 | 93.3% | 14 | 4.2s | 142.4 |
| GLM-5.3-Flash · TFQ3 · TensorFold 1.3.5 | 93.3% | 14 | 15.3s | 82.4 |
| Qwen3.8-Flash-Next · MLX 6-bit · oMLX | 91.7% | 14 | 4.4s | 146.9 |
| Qwen3.8-Flash-Next · MLX 6-bit · TensorFold 1.3.4 | 88.9% | 14 | 5.2s | 164.3 |
| Qwen3.8-Flash-Next · MLX 4-bit · oMLX | 86.7% | 13 | 8.9s | 165.9 |
| GLM-5.3-Flash · MLX 6-bit Pipe · Tandem (two Macs) | 85.0% | 13 | 19.0s | 78.6 |
| GLM-5.3-Flash · MLX 4-bit · oMLX | 81.7% | 13 | 24.9s | 74.5 |
| GLM-5.3-Flash · MLX 4-bit + DFlash2 · TensorFold 1.3.4 | 66.7% | 11 | 11.7s | 108.3 |

**How to read this:** scores are component-weighted task utility under the revised rubric, not probabilities of being correct. “Final answers” means nonempty delivered responses, not necessarily correct answers. E2E throughput includes hidden reasoning and full response time; it is **not native decode or visible-answer speed**. DFlash has only 14 throughput observations because its HTTP400 response has no token counter; that failure remains in delivery/latency accounting. Timing summaries were rounded to 0.1 seconds.

## What we can responsibly conclude

**Qwen TFQ3 on TensorFold 1.3.5 is our provisional practical candidate**, not a proven intelligence champion. It ties GLM TFQ3 on primary task score, has a roughly 79 GiB checkpoint, and delivered responsive answers on this workload. Qwen6 oMLX remains a close reference. The observed 4.2 versus 4.4 second medians do not demonstrate a meaningful speed advantage.

The leading scores are close and **rubric-dependent**:
- Qwen TFQ3 explicitly noted that the liquidity question does not specify payout capacity.
- GLM TFQ3 gives correct arithmetic conditional on a 10%-NAV cap, without explicitly warning that the cap was omitted. Strict missing-cap scoring reduces it to **91.7%**.
- Accepting the conventional implied cap raises Qwen6 oMLX to **93.3%**, a tie with the TFQ3 configurations.

There is no demonstrated two-Mac advantage for this particular workload, but this is **not** matched hardware scaling or evidence that two Macs are generally useless. Runtime/version, quantization, templates, drafting and context settings differ; engine-causal claims are not justified.

## Important limitations

- **Every configuration exhausted the mortgage question's output budget without delivering a final answer.** No configuration is validated for unattended financial calculations. Empty answers score zero delivered utility but are not labelled demonstrated arithmetic errors.
- The supplied “30-day policy” question legitimately asks for conditional arithmetic. We no longer treat its calculated date as automatic dishonesty. Premise-checking and policy-item-excluded sensitivities are provided separately.
- The document exercises are short integration tasks, not a long-context stress test. The battery is largely saturated and has limited power to distinguish capable models.
- Code answers were assessed by static algorithm review in the audit, **not newly executed in a qualified sandbox**. Target-component credit does not certify every sentence: GLM TFQ3 includes an erroneous temporal aside and an unverified Nobel-committee explanation, neither rewarded as a target fact.
- The audit is retrospective semantic adjudication by the assistant with parent verification, not independent multi-grader consensus. Tests validate arithmetic, counts, binding and aggregation—not the unique correctness of every judgement.

## What changed and how to inspect it

Original local responses and scores remain preserved. [score-changes.json](score-changes.json) records **21 historical changes (17 up, four down)**; GLM TFQ3's 15 new adjudications have null old scores rather than invented zeros.

Confirmed problems included valid debugging examples rejected for differing from the preferred example, currency/sign/LaTeX formatting misses, correct conditional uncertainty answers missed by regex, a 1% numeric tolerance accepting a $100 error, and a spurious fraction match to unrelated zeros. We also found an omitted payout-cap assumption in our own gold and an ambiguous authority question. The revised score is **literal-task utility**, not the old hard honesty gate.

- [results.json](results.json): all eight aggregates, delivery/timing and sensitivity measures.
- [audited-items.csv](audited-items.csv): all 120 slot scores and reasons.
- [audited-items.json](audited-items.json): component decisions and public evidence.
- [AUDITED-RUBRIC.md](AUDITED-RUBRIC.md): criteria and judgement calls.
- [MEASURED-QUESTIONS.json](MEASURED-QUESTIONS.json): 13 exact original measured prompts plus hashes/status for two privacy-withheld purchase-derived prompts. The Einstein original includes “Answer the question directly.”
- [CASES-v2.json](CASES-v2.json): **unscored edited draft variants** from the first publication. Its embedded gold/rubric is historical and superseded by AUDITED-RUBRIC.md. Do not attribute these scores to edited questions.

The two original purchase-derived prompts/final texts are omitted from public evidence, not silently replaced with generic examples. This limits exact public reproduction of those two slots; their original hashes, criteria and reviewer decisions are retained. No private host paths or hidden reasoning are exported.

## Recompute the published aggregates

```sh
python3 recompute_public_results.py
```

This checks the published structured decisions and aggregation. It does **not** automatically grade prose or claim to regenerate semantic judgement. The original runner/grader remain experimental historical tools; **the old grader executes model-provided Python and should not be used on untrusted answers without isolation**. Running it does not reproduce this semantic audit.

## Attempts outside the comparable field

- **DeepSeek-V4.1-Flash:** an earlier low-quant configuration had problematic outputs. Other candidate checkpoint/runtime paths were not qualified here. This does not show DeepSeek generally cannot run or lacks ability. We welcome a compatible reproducible recipe; no invented Battery v2 score is assigned.
- **GLM Flash 6-bit single-Mac:** not measured using the owned tandem-oriented checkpoint.
- **Full GLM-5.3 on a 512 GB Mac and EXO:** still unmeasured here, not failed scored results.

Suggestions for better question batteries, clearer rubrics, tool-use evaluations and independent reproductions are welcome. The purpose is to learn which configuration is useful—not to turn a small battery into an engine leaderboard.
