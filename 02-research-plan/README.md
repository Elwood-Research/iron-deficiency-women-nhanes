# Research Plan Summary: Iron Deficiency Without Anemia in Women

## Overview

This document provides a high-level summary of the comprehensive research plan for the NHANES study examining iron deficiency without anemia (IDWA) and iron supplement usage effects in non-pregnant women aged 18-45 years.

---

## Research Plan Components

| Document | Purpose | Key Contents |
|----------|---------|--------------|
| `hypotheses.md` | Formal hypotheses | 3 primary + 3 secondary hypotheses with operational definitions |
| `analysis_plan.md` | Statistical methods | Study design, regression models, survey weighting, power analysis |
| `variable_operationalization.md` | Variable definitions | Complete specification of all NHANES variables and derivations |
| `expected_results.md` | Literature-based projections | Expected prevalence, effect sizes, and clinical significance |

---

## Study Overview

### Research Question
What are the effects of iron supplement usage on ferritin levels, other iron biomarkers, and related outcomes in non-pregnant women aged 18-45 with iron deficiency without anemia?

### Study Design
- **Type:** Cross-sectional analysis of pooled NHANES cycles
- **Years:** 2005-2006, 2007-2008, 2009-2010, 2015-2016, 2017-2018, 2021-2022
- **Population:** Non-pregnant women aged 18-45 years
- **Sample Size:** Expected 800-1,000 women with IDWA

### IDWA Definition
- **Iron Deficiency:** Ferritin <15 ng/mL (LBXFER)
- **Without Anemia:** Hemoglobin ≥12 g/dL (LBXHGB)
- **Alternative (sensitivity):** Ferritin <25 ng/mL

---

## Primary Hypotheses

### H1: Supplementation Effect on Ferritin
Women with IDWA who use iron supplements have significantly higher ferritin levels than non-users (expected geometric mean ratio: 1.3-1.6).

### H2: Dose-Response Relationship
Positive dose-response relationship between supplement dose and ferritin:
- None (0 mg): Reference
- Low (>0-18 mg): +10-30% ferritin
- Moderate (18-65 mg): +40-80% ferritin  
- High (>65 mg): +50-100% ferritin

### H3: Demographic Variation
IDWA prevalence varies by race (higher in Black women), age (peak 26-35), and income (higher in lower income).

---

## Key Variables

### Primary Outcome
- **Serum Ferritin** (LBXFER): Continuous, log-transformed for analysis

### Secondary Outcomes
- Serum Iron (LBXIRN)
- TIBC (LBXTIB)
- Transferrin Saturation (LBDPCT)

### Primary Exposure
- **Iron Supplement Use:** DSQTIRON (mg/day)
- Categories: None (0), Low (>0-18), Moderate (18-65), High (>65)

### Key Covariates
- Age (RIDAGEYR)
- Race/Ethnicity (RIDRETH1)
- Poverty Ratio (INDFMPIR)
- BMI (BMXBMI)
- NHANES Cycle (temporal control)

---

## Statistical Approach

### Survey Design
- **Weights:** WTMEC2YR (adjusted for pooling)
- **Strata:** SDMVSTRA
- **PSU:** SDMVPSU
- **Method:** Taylor series linearization

### Primary Analysis
Linear regression of ln(ferritin) on supplement use:
- Model 1: Unadjusted
- Model 2: Demographically adjusted (age, race, cycle)
- Model 3: Fully adjusted (+ poverty, BMI)

### Secondary Analyses
- Dose-response trend tests
- Logistic regression for IDWA prevalence factors
- Subgroup analyses by demographics
- Sensitivity analyses (alternative thresholds, inflammation adjustment)

---

## Expected Findings

### Prevalence
- **Overall IDWA:** 10-12% of women 18-45
- **By race:** 15-20% in Black women, 8-10% in White women
- **By income:** 18-25% below poverty, 6-10% higher income

### Treatment Effects
- Supplementation increases ferritin by 30-60%
- Optimal dose: ~60 mg/day
- Multivitamins insufficient for deficiency correction
- 35-50% normalization rate with supplementation

---

## Deliverables Checklist

- [x] Hypotheses defined with operational specifications
- [x] Statistical analysis plan with models and procedures
- [x] Variable operationalization with code examples
- [x] Expected results based on literature synthesis
- [ ] Methods development (next phase)
- [ ] Data analysis execution
- [ ] Manuscript preparation

---

## Next Steps

1. **Methods Development (Phase 3):**
   - Finalize data merging procedures
   - Create variable derivation scripts
   - Develop analysis code templates

2. **Data Analysis (Phase 4):**
   - Execute data merging and cleaning
   - Run primary and secondary analyses
   - Generate tables and figures

3. **Manuscript Preparation (Phase 5):**
   - Write results and discussion
   - Create publication-ready figures
   - Format for target journal

---

## Document Versions

| Document | Version | Date |
|----------|---------|------|
| hypotheses.md | 1.0 | 2026-01-31 |
| analysis_plan.md | 1.0 | 2026-01-31 |
| variable_operationalization.md | 1.0 | 2026-01-31 |
| expected_results.md | 1.0 | 2026-01-31 |

---

*Research Plan Summary*  
*Study: Iron Deficiency Without Anemia in Women*  
*Location: studies/iron-deficiency-women-2026-01-31/02-research-plan/*  
*Date: 2026-01-31*
