# Statistical Analysis Plan: Iron Deficiency Without Anemia Study

## 1. Study Design

### 1.1 Design Overview

This study employs a **cross-sectional design using pooled NHANES cycles** to examine the relationship between iron supplement use and iron status biomarkers in women with iron deficiency without anemia (IDWA).

**Study Type:** Population-based, nationally representative cross-sectional analysis  
**Data Source:** National Health and Nutrition Examination Survey (NHANES)  
**Years Included:** 2005-2006, 2007-2008, 2009-2010, 2015-2016, 2017-2018, 2021-2022  
**Analysis Approach:** Complex survey design with appropriate weighting and variance estimation

### 1.2 Study Population

**Target Population:** Non-pregnant women aged 18-45 years residing in the United States

**Inclusion Criteria:**
1. Age 18-45 years at examination (RIDAGEYR)
2. Female sex (RIAGENDR = 2)
3. Not pregnant (to be determined from appropriate NHANES variables)
4. Complete ferritin measurement (LBXFER not missing)
5. Complete hemoglobin measurement (LBXHGB not missing)
6. Valid survey weights available (WTMEC2YR > 0)

**Exclusion Criteria:**
1. Pregnant women (at time of examination)
2. Missing ferritin or hemoglobin data
3. Age outside 18-45 range
4. Iron deficiency anemia (IDA) - to be analyzed separately if sample size permits

### 1.3 Case Definition: Iron Deficiency Without Anemia (IDWA)

**Primary Definition (Standard):**
- **Iron Deficiency:** Serum ferritin < 15 ng/mL (LBXFER < 15)
- **Without Anemia:** Hemoglobin ≥ 12.0 g/dL (LBXHGB ≥ 12.0)

**Alternative Definition (Sensitivity Analysis):**
- **Iron Deficiency:** Serum ferritin < 25 ng/mL (LBXFER < 25)
- **Without Anemia:** Hemoglobin ≥ 12.0 g/dL (LBXHGB ≥ 12.0)

*Rationale:* The WHO threshold of 15 ng/mL may underestimate iron deficiency, particularly in women with heavy menstrual bleeding. The 25 ng/mL cutoff captures a broader spectrum of iron depletion [1,2].

### 1.4 Iron Status Categories

Participants will be classified into four mutually exclusive categories:

| Category | Ferritin | Hemoglobin | Clinical Meaning |
|----------|----------|------------|------------------|
| Normal Iron Status | ≥15 ng/mL | ≥12 g/dL | Iron replete, non-anemic |
| IDWA (Primary) | <15 ng/mL | ≥12 g/dL | Iron deficient, non-anemic |
| Iron Deficiency Anemia (IDA) | <15 ng/mL | <12 g/dL | Iron deficient, anemic |
| Anemia without ID | ≥15 ng/mL | <12 g/dL | Anemia from other causes |

---

## 2. Primary Exposures and Outcomes

### 2.1 Primary Exposure: Iron Supplement Use

**Variable Derivation:**
- Primary source: DSQTIRON (total iron from supplements, mg/day)
- Alternative: Individual supplement files (DSQ files) for detailed product information

**Categorization Scheme:**

| Category | Iron Dose | Description | Rationale |
|----------|-----------|-------------|-----------|
| None | 0 mg | No iron supplementation | Reference group |
| Low | >0 to <18 mg | Multivitamin-level iron | Typical multivitamin dose |
| Moderate | 18-65 mg | Standard therapeutic | Optimal per literature [3] |
| High | >65 mg | High therapeutic | Prescription strength |

**Binary Derivation (for sensitivity analyses):**
- User: DSQTIRON > 0 mg
- Non-user: DSQTIRON = 0 mg

### 2.2 Primary Outcomes

**Continuous Outcomes:**
1. **Serum Ferritin** (LBXFER): Primary endpoint, ng/mL
   - Will be natural log-transformed due to right-skewed distribution
   - Interpretation: % change in geometric mean per unit change in predictor

2. **Serum Iron** (LBXIRN): µg/dL (where available)
   - May require log transformation depending on distribution

3. **TIBC** (LBXTIB): µg/dL (where available)
   - Expected inverse relationship with iron status

4. **Transferrin Saturation** (LBDPCT): %
   - Calculated/derived variable: (Serum Iron / TIBC) × 100
   - Or use pre-calculated LBDPCT where available

**Categorical Outcomes:**
1. **IDWA Status:** Binary (yes/no) per definition above
2. **Iron Deficiency Status:** Binary (ferritin <15 ng/mL, yes/no)
3. **Anemia Status:** Binary (hemoglobin <12 g/dL, yes/no)

---

## 3. Covariates and Confounders

### 3.1 Demographic Covariates

| Variable | Source | Categories/Type | Handling |
|----------|--------|-----------------|----------|
| Age | RIDAGEYR | Continuous (18-45) | Include as continuous; test for non-linearity |
| Age Group | RIDAGEYR | 18-25, 26-35, 36-45 | For stratified analyses |
| Race/Ethnicity | RIDRETH1 | 5 categories (see below) | Include all categories |
| Race/Ethnicity (Alt) | RIDRETH3 | 6 categories (includes Asian) | Use in 2011+ cycles |

**Race/Ethnicity Coding (RIDRETH1):**
- 1: Mexican American
- 2: Other Hispanic
- 3: Non-Hispanic White
- 4: Non-Hispanic Black
- 5: Other Race - Including Multi-Racial

### 3.2 Socioeconomic Covariates

| Variable | Source | Type | Handling |
|----------|--------|------|----------|
| Poverty Ratio | INDFMPIR | Continuous | Truncate at 5.0 (top-coded); handle missing |
| Income Category | INDFMPIR | <1.0, 1.0-1.99, 2.0-3.99, ≥4.0 | For descriptive tables |

### 3.3 Anthropometric Covariates

| Variable | Source | Type | Handling |
|----------|--------|------|----------|
| BMI | BMXBMI | Continuous kg/m² | Include as continuous |
| BMI Category | BMXBMI | <18.5, 18.5-24.9, 25-29.9, ≥30 | For stratified analyses |

### 3.4 Survey Design Variables (Required)

| Variable | Purpose | Handling |
|----------|---------|----------|
| WTMEC2YR | Sample weights | Normalize for pooled cycles (divide by number of cycles) |
| SDMVSTRA | Sampling strata | Include in survey design specification |
| SDMVPSU | Primary sampling units | Include in survey design specification |

### 3.5 Potential Confounders to Consider

**Inflammation Markers (if available):**
- CRP (high-sensitivity C-reactive protein): Elevated in inflammation, affects ferritin
- Adjustment strategy: Exclude participants with CRP > 5 mg/L (indicates acute inflammation)

**Menstrual Factors (if available):**
- Heavy menstrual bleeding history
- Menopause status (to exclude if relevant)

---

## 4. Statistical Methods

### 4.1 Descriptive Statistics

**Population Characteristics:**
- Means ± SE for continuous variables (complex survey SEs)
- Frequencies (weighted %) for categorical variables
- Overall and stratified by IDWA status and supplement use

**Iron Status Distribution:**
- Prevalence estimates (%) with 95% confidence intervals for:
  - IDWA (primary definition)
  - IDWA (alternative <25 ng/mL definition)
  - Iron deficiency anemia
  - Anemia without iron deficiency
- Estimates overall and by demographic subgroups

### 4.2 Primary Analysis: Effect of Supplementation on Ferritin

**Model 1: Unadjusted**
```
ln(Ferritin) = β₀ + β₁(Supplement Use) + ε
```

**Model 2: Demographically Adjusted**
```
ln(Ferritin) = β₀ + β₁(Supplement Use) + β₂(Age) + β₃(Race) + β₄(Cycle) + ε
```

**Model 3: Fully Adjusted**
```
ln(Ferritin) = β₀ + β₁(Supplement Use) + β₂(Age) + β₃(Race) + β₄(Poverty Ratio) + 
               β₅(BMI) + β₆(Cycle) + ε
```

**Model Specifications:**
- Outcome: Natural log of ferritin (to handle skewness)
- Exposure: Binary (user vs. non-user) or categorical (4 dose groups)
- Survey design: Taylor series linearization with strata and PSUs
- Interpretation: Exponentiate coefficients to get geometric mean ratios

**Effect Estimates:**
- β coefficient (log scale)
- Geometric mean ratio (exp(β))
- 95% Confidence interval
- p-value for two-sided test

### 4.3 Dose-Response Analysis

**Trend Test:**
- Test for linear trend across ordered categories (None, Low, Moderate, High)
- Assign scores: 0, 1, 2, 3 to categories
- Wald test for trend coefficient

**Pairwise Comparisons:**
- Each category vs. reference (None)
- Moderate vs. Low (multivitamin vs. therapeutic)
- High vs. Moderate (diminishing returns test)
- Bonferroni correction for multiple comparisons: α = 0.05/6 = 0.008

### 4.4 Demographic Variation in IDWA Prevalence

**Prevalence Estimates:**
- Calculate weighted prevalence with 95% CIs overall and by subgroups
- Test for differences across groups using Rao-Scott chi-square

**Logistic Regression (for factors associated with IDWA):**
```
logit(P(IDWA)) = β₀ + β₁(Age) + β₂(Race) + β₃(Poverty) + β₄(BMI) + β₅(Cycle) + ε
```

### 4.5 Secondary Biomarker Analyses

**Multiple Outcome Testing:**
- Serum iron (continuous)
- TIBC (continuous)
- Transferrin saturation (continuous)

**Adjustment for Multiple Comparisons:**
- Bonferroni: α = 0.05/3 = 0.017 per outcome family
- Or FDR (Benjamini-Hochberg) control

### 4.6 Sensitivity Analyses

**SA1: Alternative Ferritin Threshold**
- Repeat primary analyses using ferritin <25 ng/mL as ID definition
- Compare effect estimates between <15 and <25 definitions

**SA2: Inflammation Adjustment**
- Exclude participants with CRP > 5 mg/L (if CRP available)
- Repeat primary analyses in inflammation-free sample

**SA3: Pregnancy Sensitivity**
- If pregnancy data incomplete, conduct sensitivity analysis excluding:
  - Women with very high ferritin (possible acute phase response)
  - Women with specific age-related patterns

**SA4: Extreme Dose Analysis**
- Exclude participants with iron dose >100 mg/day (possible data errors)
- Examine effect of very high doses separately

**SA5: Cycle-Specific Analysis**
- Test for effect modification by NHANES cycle (time trends)
- If significant heterogeneity, present cycle-stratified results

---

## 5. Survey Weighting and Variance Estimation

### 5.1 Weight Construction

**For Pooled Cycles (2005-2022):**
```
Adjusted Weight = WTMEC2YR / (Number of Cycles)
```

Where Number of Cycles = 6 (D, E, F, I, J, L)

**Rationale:** Dividing by the number of cycles ensures the total weighted sample represents the average population size across the study period rather than summing to 6× the population.

### 5.2 Survey Design Specification

**Python (svy_design):**
```python
# Pseudo-code for survey design
survey_design = SurveyDesign(
    data=df,
    weights='WTMEC2YR_adj',
    strata='SDMVSTRA',
    psu='SDMVPSU',
    nest=True
)
```

**Key Considerations:**
- Use MEC examination weights (WTMEC2YR) not interview weights
- Strata and PSUs must be included for valid variance estimation
- Finite population correction not needed for NHANES

### 5.3 Variance Estimation

**Method:** Taylor series linearization (recommended for NHANES)
- Degrees of freedom: Number of PSUs - Number of strata
- For subpopulation analyses (e.g., only IDWA participants), use proper subpopulation domain approach

---

## 6. Sample Size and Power Considerations

### 6.1 Expected Sample Sizes

| Population | Expected n | Source |
|------------|------------|--------|
| Women 18-45 (all cycles) | ~8,000-10,000 | NHANES sampling patterns |
| After exclusions (pregnancy, missing) | ~6,000-8,000 | ~20% attrition |
| IDWA prevalence (~12%) | ~700-960 | Literature estimates |
| IDWA with supplement use (~30%) | ~210-290 | Estimated uptake |

### 6.2 Minimum Detectable Effects

Assuming n=800 with IDWA and 30% supplement use (n=240 users, n=560 non-users):

| Outcome | SD | Power | Alpha | Minimum Detectable Difference |
|---------|-----|-------|-------|-------------------------------|
| Ferritin | 25 ng/mL | 80% | 0.05 | ~6 ng/mL mean difference |
| Ferritin (log scale) | 0.8 | 80% | 0.05 | ~25% geometric mean ratio |

*Calculations assume two-sided test with complex survey design inflation factor of 1.5*

---

## 7. Software and Implementation

### 7.1 Primary Software

**Python Stack:**
- `pandas`: Data manipulation and merging
- `numpy`: Numerical operations
- `statsmodels`: Survey-weighted regression (with survey module)
- `scipy`: Statistical tests
- `matplotlib`/`seaborn`: Visualization

### 7.2 Alternative Software

**R (if needed for specific procedures):**
- `survey` package: Complex survey analysis (gold standard)
- `srvyr`: Tidyverse interface to survey package

### 7.3 Key Packages and Versions

```
pandas >= 1.3.0
numpy >= 1.21.0
statsmodels >= 0.13.0
scipy >= 1.7.0
matplotlib >= 3.4.0
seaborn >= 0.11.0
```

---

## 8. Quality Control and Validation

### 8.1 Data Quality Checks

1. **Range checks:** Verify all biomarkers within physiologic ranges
2. **Missing data patterns:** Examine by cycle, demographic group
3. **Weight verification:** Confirm all weights positive and sum appropriately
4. **Duplicate SEQN:** Ensure no duplicate participant IDs after merging

### 8.2 Analysis Validation

1. **Replicate in R:** Key models run in both Python and R for verification
2. **Bootstrap validation:** Non-parametric bootstrap for confidence intervals
3. **Sensitivity to outliers:** Models with and without extreme values

---

## 9. Handling of Missing Data

### 9.1 Missing Data Patterns

**Approach:** Complete case analysis for primary analyses
- Listwise deletion for missing covariates
- Report sample sizes for each analysis
- Conduct missing data sensitivity analyses

### 9.2 Variables with Expected Missingness

| Variable | Expected % Missing | Strategy |
|----------|-------------------|----------|
| Poverty Ratio | ~5-10% | Include "missing" category or impute |
| BMI | ~2-5% | Complete case or median imputation |
| Iron biomarkers | ~10-20% | Complete case (these define the sample) |
| Supplement data | ~15-25% | Assume no use if missing (conservative) |

---

## 10. Subgroup and Stratified Analyses

### 10.1 Pre-specified Subgroups

1. **By Age Group:**
   - Young adults (18-25)
   - Prime reproductive (26-35)
   - Later reproductive (36-45)

2. **By Race/Ethnicity:**
   - Non-Hispanic White
   - Non-Hispanic Black
   - Hispanic (Mexican + Other)
   - Other/Multi-racial

3. **By Socioeconomic Status:**
   - Below poverty (<1.0)
   - Near poverty (1.0-1.99)
   - Middle income (2.0-3.99)
   - Higher income (≥4.0)

4. **By BMI Category:**
   - Underweight (<18.5)
   - Normal (18.5-24.9)
   - Overweight (25-29.9)
   - Obese (≥30)

### 10.2 Subgroup Analysis Approach

- Test for interaction (effect modification) first
- If p-interaction < 0.05, report stratum-specific results
- If p-interaction ≥ 0.05, report overall with caution about generalizability

---

## 11. Tables and Figures Plan

### 11.1 Summary Tables

| Table | Content |
|-------|---------|
| Table 1 | Population characteristics by IDWA status and supplement use |
| Table 2 | IDWA prevalence by demographic subgroups |
| Table 3 | Unadjusted and adjusted associations: supplement use → ferritin |
| Table 4 | Dose-response analysis across supplement categories |
| Table 5 | Secondary biomarker outcomes (iron, TIBC, TSAT) |
| Table 6 | Sensitivity analyses summary |

### 11.2 Figures Plan

| Figure | Content | Type |
|--------|---------|------|
| Figure 1 | Study flow diagram | Flowchart |
| Figure 2 | IDWA prevalence by demographics | Bar chart with CIs |
| Figure 3 | Ferritin distribution by supplement use | Box plot/violin |
| Figure 4 | Dose-response relationship | Line plot with CIs |
| Figure 5 | Forest plot of subgroup analyses | Forest plot |

---

## References

1. WHO/CDC. (2007). Assessing the iron status of populations. *WHO Technical Report*.
2. Mei Z, et al. (2011). Serum ferritin thresholds for iron deficiency. *Am J Clin Nutr*.
3. Stoffel NU, et al. (2020). Iron absorption from oral iron supplements. *Lancet Haematol*.
4. NHANES Analytic Guidelines. (2021). *CDC/NCHS Documentation*.

---

*Analysis Plan Version 1.0*  
*Date: 2026-01-31*  
*Study: Iron Deficiency Without Anemia in Women*
