# EVALUATION.md — Aradhana AstroAgent

## Overview

This document reflects honestly on what the evaluation revealed, what worked, what didn't, and what I would fix with more time.

---

## Evaluation Approach

I built the evaluation harness before completing all features — the golden set was written on Day 1 as a contract for expected behavior, not retrofitted at the end.

### What I measured

| Metric | Method |
|--------|--------|
| Success rate | Did the agent return a response without crashing? |
| Safety pass rate | Did safety cases get handled without harmful output? |
| Warmth | LLM-as-judge (1-5 rubric) |
| Relevance | LLM-as-judge (1-5 rubric) |
| Grounded | LLM-as-judge (1-5 rubric) |
| Latency | Wall clock time per case |

---

## Results (Latest Run)

| Metric | Score |
|--------|-------|
| Total cases | 20 |
| Success rate | 95% |
| Safety pass rate | 100% |
| Avg latency | 3.31s |
| Avg overall | 4.23/5 |
| Avg warmth | 4.30/5 |
| Avg relevance | 4.20/5 |

---

## What the Eval Revealed

### Strengths

**Safety handling is robust.**
Every single safety case passed — financial advice requests, medical queries, prompt injection attempts, and death predictions were all handled gracefully and redirected with warmth. This was the most important dimension and the agent scored 100%.

**Tone is consistently warm.**
4.30/5 average warmth across 20 diverse cases including edge cases and adversarial prompts. The system prompt effectively maintains Aradhana's spiritual, compassionate personality even under pressure.

**Tool calling works correctly.**
Cases requiring geocoding + birth chart computation completed successfully. The agent correctly chains tools: geocode_place → compute_birth_chart → interpret results.

### Weaknesses

**1 failed case (5% failure rate)**
One case failed due to an edge case in birth chart computation with an unusual timezone combination. The agent returned a 500 error instead of a graceful fallback message. This needs a better try/catch in the birth chart tool.

**Latency on chart requests**
Cases requiring tool calls averaged 7-8 seconds due to the agent loop: geocode → compute chart → reason → respond. This is acceptable for a spiritual companion but could be improved with caching.

**LLM judge validation**
I spot-checked 10 judge verdicts against my own assessment and found 8/10 agreement (80%). The judge occasionally rates "grounded" too high when the agent responds without calling tools. A stricter rubric would improve this.

---

## What I Would Fix With More Time

**1. Caching birth chart computations**
The Swiss Ephemeris calculation is deterministic — same inputs always produce same outputs. Caching with Redis would cut latency from 7s to under 1s for returning users.

**2. Missing birth time handling**
When users don't know their birth time, the agent currently defaults to 12:00 PM (solar chart). I'd add explicit handling that explains this limitation and offers a whole-sign house system as an alternative.

**3. Expand golden set to 50 cases**
20 cases is sufficient for this submission but a production system needs broader coverage — more edge cases, more languages, more adversarial prompts.

**4. Streaming eval metrics**
The current eval runner uses the non-streaming endpoint. I'd add streaming-specific tests to verify token-by-token delivery works correctly under load.

**5. Cost tracking**
I didn't implement per-run token cost tracking. Adding this would let us optimize prompts for cost without sacrificing quality.

**6. Fix the 1 failing case**
The timezone edge case failure needs a defensive fallback that returns a partial chart with a clear explanation rather than crashing.

---

## On Using LLM-as-Judge

I used `llama-3.1-8b-instant` as the judge model with a concrete 1-5 rubric scoring one dimension at a time. I validated 10 verdicts manually and found 80% agreement.

The judge is most reliable for warmth and safety — these are clear, definable qualities. It is least reliable for "grounded" because it cannot verify whether the agent actually called the ephemeris tool vs. hallucinated positions.

For a production eval, I would add a deterministic check: parse the agent's response for planetary position claims and verify them against pyswisseph directly.

---

## Reproducing the Eval

```bash
cd backend
python evals/eval_runner.py
```

Output: scorecard printed to terminal + CSV saved to `evals/eval_results_TIMESTAMP.csv` + appended to `evals/results_log.md`