# Task 001: The Checkout Redesign That "Lost" Everywhere and Won Everywhere

**Skills tested:** data cleaning, A/B test analysis, Simpson's paradox, standardisation, hypothesis testing
**Difficulty:** Hard  |  **Answer type:** numeric + boolean + categorical  |  **Time-sensitivity:** static (answer does not expire)

## Scenario

An e-commerce company tested a redesigned checkout page (`variant`) against the existing one (`control`).
The product manager opened the dashboard and said: *"The new design converts far worse. Roll it back."*
You are asked to review the analysis before the decision is made.

Data: `data/checkout_experiment.csv` (one row per logged user session)

| column | meaning |
|---|---|
| `user_id` | unique user identifier |
| `arm` | `control` or `variant` |
| `device` | `desktop` or `mobile` |
| `converted` | 1 if the user completed a purchase, else 0 |
| `is_internal` | 1 if the account belongs to internal QA staff |

Known facts from the engineering team:
- A logging retry bug may have written some rows more than once.
- Internal QA accounts were not excluded from the experiment.
- Because of a traffic-ramp bug, device mix differs between arms. Assume that **within each device**, users were randomly assigned to arms.

## Questions

1. What are the raw conversion rates of `control` and `variant` using the file as-is?
2. After cleaning the data, how many rows remain, what are the conversion rates per arm, and what is the overall (naive) lift in percentage points (variant minus control)?
3. What is the absolute lift (percentage points) within each device, and is it significant at the 5% level (two-sided two-proportion z-test)?
4. What is the device-mix-standardised lift (use the pooled cleaned device mix of both arms as weights), and is it significant at 5%?
5. Final recommendation: `ship_variant`, `rollback`, or `inconclusive`?

## Output format

Submit a JSON object with exactly these keys (rates as fractions rounded to 4 decimals, lifts in percentage points rounded to 2 decimals):

```json
{
  "q1_raw_conversion_control": 0.0,
  "q1_raw_conversion_variant": 0.0,
  "q2_clean_rows": 0,
  "q2_clean_conversion_control": 0.0,
  "q2_clean_conversion_variant": 0.0,
  "q2_clean_naive_lift_pp": 0.0,
  "q3_desktop_lift_pp": 0.0,
  "q3_mobile_lift_pp": 0.0,
  "q3_desktop_significant_5pct": false,
  "q3_mobile_significant_5pct": false,
  "q4_standardised_lift_pp": 0.0,
  "q4_standardised_significant_5pct": false,
  "q5_recommendation": ""
}
```
