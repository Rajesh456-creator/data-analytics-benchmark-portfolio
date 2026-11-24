# Expected failure modes (and how a grader should spot them)

| Failure mode | Symptom in a response | Where it breaks |
|---|---|---|
| Simpson's paradox missed | Recommends `rollback` based on overall -6.29pp | Q2, Q4, Q5 |
| Incomplete cleaning | Removes duplicates but keeps QA accounts (or vice versa); rows != 20000 | Q2 and everything downstream |
| Wrong weights for standardisation | Uses control-only or variant-only mix, giving a different lift | Q4 |
| Unpooled/pooled z-test confusion | Significance flags right but p-values differ; only matters near threshold | Q3 |
| Overclaiming causality | Treats overall difference as causal despite the ramp bug | Q5 reasoning |

> Note: this section is meant to be filled in with real observed model outputs.
> Add a dated table here after testing the task on an AI model (model name, answer given, which questions failed).
