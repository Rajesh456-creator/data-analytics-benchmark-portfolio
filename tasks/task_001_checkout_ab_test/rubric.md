# Rubric: Task 001 (total 100 points)

Numeric answers are correct within +/-0.0005 for rates and +/-0.02 for lifts (rounding tolerance). Match against `answer.json`.

| # | Criterion | Points |
|---|---|---|
| 1 | Q1 raw rates correct (no cleaning applied) | 10 |
| 2 | Removed internal QA accounts **and** exact duplicate users; `q2_clean_rows` correct | 20 |
| 3 | Q2 cleaned rates and naive lift correct (negative lift) | 10 |
| 4 | Q3 per-device lifts correct and both positive | 20 |
| 5 | Q3 significance flags correct (two-proportion z-test, pooled variance) | 10 |
| 6 | Q4 standardised lift correct using pooled device mix | 15 |
| 7 | Q4 significance flag correct (stratified variance) | 5 |
| 8 | Q5 recommendation correct: `ship_variant` | 10 |

## Automatic deductions / flags
- Recommending `rollback` from the naive aggregate: **cap total at 40** (falls for Simpson's paradox).
- Deduplicating by dropping rows with identical *values* in non-ID columns instead of by `user_id`: lose criterion 2 points.
- Order of cleaning matters for nothing here, but doing **no** cleaning at all caps Q2-Q5 at 50% credit.

## Why the answer is `ship_variant`
Control traffic is mostly desktop (high baseline conversion) and variant traffic is mostly mobile (low baseline). The aggregate comparison measures device mix, not the redesign. Within each device the variant wins and the effect is significant, so the standardised comparison is the valid one.
