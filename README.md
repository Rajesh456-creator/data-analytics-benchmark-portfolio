# Data Analytics Benchmark Portfolio

Original, self-authored benchmark tasks for evaluating data-analytics reasoning.
Each task ships with a dataset, a verifiable answer key, a grading rubric, a Python reference solution,
and a failure analysis. CI re-runs every reference solution and checks it against `answer.json`.

All data is synthetic and generated with fixed seeds (`tools/`). No third-party or client material is included.

| Task | Skills tested | Difficulty | Answer type | Expires? |
|---|---|---|---|---|
| [001 Checkout A/B test](tasks/task_001_checkout_ab_test/) | Data cleaning, Simpson's paradox, standardisation, z-tests | Hard | numeric / boolean / categorical | static |

## Task anatomy
```
tasks/<task>/
  problem.md            scenario, questions, output schema
  data/                 dataset(s)
  reference_solution.py solution that produces the answers
  answer.json           ground truth
  rubric.md             grading criteria and deductions
  failure_analysis.md   expected and observed model failure modes
```

## Design principles
1. **Objective answers:** every question has one checkable result.
2. **Traps that mirror real work:** dirty rows, confounded groups, misleading aggregates.
3. **Reproducible:** `python tools/validate_task.py` must pass.
4. **Time-sensitivity tagged:** static / quarterly / fast-changing.

## Run
```bash
pip install -r requirements.txt
python tools/validate_task.py
```
