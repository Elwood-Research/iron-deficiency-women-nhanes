# Research Hypotheses: Iron Deficiency Without Anemia in Women

## Overview

This document presents the formal research hypotheses for the NHANES study examining iron deficiency without anemia (IDWA) and iron supplement usage effects in non-pregnant women aged 18-45 years. Hypotheses are organized hierarchically with primary hypotheses addressing the core research questions and secondary hypotheses exploring additional associations of clinical interest.

---

## Primary Hypotheses

### H1: Effect of Iron Supplementation on Ferritin Levels in IDWA

**Statement:** Women with iron deficiency without anemia (IDWA) who use iron supplements have significantly higher ferritin levels than non-users after adjusting for demographic and socioeconomic covariates.

**Rationale:** Based on literature suggesting that 60 mg daily iron supplementation is optimal for raising ferritin levels in iron-deficient women [1,2]. Current guidelines recommend supplementation for iron deficiency even without anemia.

**Operationalization:**
- **Exposure:** Iron supplement use (binary: yes/no) derived from DSQTIRON > 0 mg
- **Outcome:** Continuous ferritin levels (LBXFER, ng/mL)
- **Population:** Women with IDWA (ferritin <15 ng/mL AND hemoglobin ≥12 g/dL)
- **Expected Direction:** Positive association (β > 0)

**Hypothesis Type:** Two-tailed test of difference in means

---

### H2: Dose-Response Relationship Between Iron Supplementation and Ferritin

**Statement:** There is a positive dose-response relationship between iron supplement dose categories and ferritin levels in women with IDWA.

**Rationale:** Literature indicates that supplementation effects are dose-dependent, with higher doses producing greater increases in iron stores [3]. The optimal therapeutic dose of 60 mg/day is expected to show the strongest association.

**Operationalization:**
- **Exposure:** Categorical dose variable
  - None: 0 mg (reference)
  - Low: >0 to <18 mg (multivitamin-level)
  - Moderate: 18-65 mg (standard therapeutic dose)
  - High: >65 mg (high therapeutic dose)
- **Outcome:** Continuous ferritin levels (natural log-transformed)
- **Expected Pattern:** Stepwise increase: None < Low < Moderate ≤ High

**Hypothesis Type:** Test for linear trend across ordered categories

---

### H3: Demographic Variation in IDWA Prevalence

**Statement:** The prevalence of IDWA varies significantly across demographic subgroups including race/ethnicity, age group, and socioeconomic status (as measured by poverty ratio).

**Rationale:** Health disparities research consistently demonstrates differential burden of nutritional deficiencies across racial, economic, and age strata. Heavy menstrual bleeding patterns (major risk factor) vary by demographic factors [4].

**Operationalization:**
- **Outcome:** IDWA prevalence (binary: yes/no)
- **Predictors:**
  - Race/ethnicity (RIDRETH1: 5 categories)
  - Age group (18-25, 26-35, 36-45 years)
  - Poverty ratio (continuous INDFMPIR)
- **Expected Patterns:**
  - Higher prevalence in non-Hispanic Black women
  - Higher prevalence in lower income groups
  - Peak prevalence in reproductive peak years (26-35)

**Hypothesis Type:** Chi-square tests of independence (categorical) and logistic regression (continuous)

---

## Secondary Hypotheses

### H4: Association Between Supplementation and Complete Iron Biomarker Panel

**Statement:** Iron supplementation is associated with improvements across the complete iron biomarker panel (serum iron, TIBC, and transferrin saturation) in women with IDWA, beyond the effect on ferritin alone.

**Rationale:** Iron deficiency represents a spectrum of biomarker abnormalities. Supplementation should normalize iron metabolism across multiple parameters, not just storage ferritin [5].

**Operationalization:**
- **Exposure:** Iron supplement use (binary/categorical)
- **Outcomes:**
  - Serum iron (LBXIRN, µg/dL)
  - TIBC (LBXTIB, µg/dL) - expected to decrease
  - Transferrin saturation (LBDPCT, %) - expected to increase
- **Expected Directions:**
  - Serum iron: Positive association
  - TIBC: Negative association (inverse relationship)
  - Transferrin saturation: Positive association

**Hypothesis Type:** Multiple regression with correction for multiple comparisons (Bonferroni or FDR)

---

### H5: Multivitamin vs. Dedicated Iron Supplement Effect Comparison

**Statement:** Multivitamin use containing lower-dose iron (<18 mg) has a smaller effect on ferritin levels compared to dedicated iron supplements (≥18 mg) in women with IDWA.

**Rationale:** While multivitamins contain iron, the dose is typically insufficient for therapeutic correction of deficiency. Literature suggests that 60 mg is the optimal dose, far exceeding multivitamin content [2,6].

**Operationalization:**
- **Exposure Comparison:**
  - Multivitamin only: >0 to <18 mg iron (primarily from multi)
  - Dedicated iron: ≥18 mg iron (iron-specific supplement)
- **Outcome:** Ferritin change/levels
- **Expected Result:** Dedicated iron group shows significantly higher ferritin than multivitamin-only group

**Hypothesis Type:** Two-group comparison with adjustment for confounders

---

### H6: Duration-Response Relationship

**Statement:** Duration of iron supplement use correlates positively with ferritin levels in women with IDWA, with longer use associated with greater iron store repletion.

**Rationale:** Iron repletion is a cumulative process. Longer duration of supplementation should result in greater restoration of iron stores, up to physiologic limits [7].

**Operationalization:**
- **Exposure:** Duration categories (if available in NHANES)
  - <1 month
  - 1-6 months
  - 6-12 months
  - >12 months
- **Outcome:** Ferritin levels (continuous)
- **Alternative:** If duration not available, use cycle-based proxy or exclude
- **Expected Pattern:** Positive correlation with duration

**Hypothesis Type:** Ordinal regression or trend test across duration categories

---

## Exploratory Hypotheses

### EH1: Interaction Between Supplement Use and Demographics

**Statement:** The effect of iron supplementation on ferritin levels varies by race/ethnicity and/or socioeconomic status.

**Rationale:** Absorption and metabolism of iron may differ across demographic groups due to genetic factors, dietary patterns, or comorbidities.

**Testing:** Interaction terms in regression models (supplement use × race, supplement use × poverty ratio)

---

### EH2: BMI as Effect Modifier

**Statement:** BMI modifies the relationship between iron supplementation and ferritin response, with different patterns observed in underweight, normal weight, and overweight/obese women.

**Rationale:** Obesity is associated with inflammatory states that can elevate ferritin independent of iron status, potentially confounding supplementation assessments [8].

**Testing:** Stratified analyses by BMI category; interaction testing

---

## Hypothesis Testing Framework Summary

| Hypothesis | Primary/Secondary | Statistical Test | Alpha Level |
|------------|-------------------|------------------|-------------|
| H1 | Primary | Linear regression (complex survey) | 0.05 |
| H2 | Primary | Linear trend test / ANOVA | 0.05 |
| H3 | Primary | Chi-square / Logistic regression | 0.05 |
| H4 | Secondary | Multivariate regression (adjusted) | 0.017 (Bonferroni) |
| H5 | Secondary | Two-group comparison (t-test) | 0.05 |
| H6 | Secondary | Ordinal regression / Correlation | 0.05 |
| EH1 | Exploratory | Interaction testing | 0.05 |
| EH2 | Exploratory | Stratified analysis | 0.05 |

---

## References

1. Low MS, et al. (2016). Daily iron supplementation for improving anaemia, iron status and health in menstruating women. *Cochrane Database Syst Rev*.
2. Stoffel NU, et al. (2020). Iron absorption from oral iron supplements given on consecutive versus alternate days. *Lancet Haematol*.
3. Toblli JE, et al. (2015). Comparison of different iron compounds as supplements in rats with iron deficiency anemia. *Nutr Res Pract*.
4. Taymor ML, et al. (2010). Iron deficiency and heavy menstrual bleeding. *Obstet Gynecol*.
5. Bothwell TH, et al. (1979). Iron metabolism in man. *Blackwell Scientific Publications*.
6. Cancelo-Hidalgo MJ, et al. (2013). Tolerability of different oral iron supplements. *Clin Ther*.
7. Finch CA, Huebers H. (1982). Perspectives in iron metabolism. *N Engl J Med*.
8. Yanoff LB, et al. (2007). Inflammation and iron deficiency in the hypoferremia of obesity. *Int J Obes*.

---

*Document prepared for NHANES Iron Deficiency Without Anemia Study*  
*Study Directory: studies/iron-deficiency-women-2026-01-31*  
*Version: 1.0*  
*Date: 2026-01-31*
