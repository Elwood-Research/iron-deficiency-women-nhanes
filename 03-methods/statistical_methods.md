# Statistical Methods: Iron Deficiency Without Anemia Study

## Overview

This document describes the comprehensive statistical methodology for analyzing the relationship between iron supplement use and iron biomarkers in women with IDWA using NHANES 2005-2022 data.

## Survey Weighting

### Weight Adjustment for Pooled Cycles

When combining data across multiple NHANES cycles, weights must be adjusted to maintain population representativeness.

**Formula**:
```
Adjusted Weight = WTMEC2YR / N_cycles
```

Where:
- `WTMEC2YR` = Original 2-year MEC exam weight
- `N_cycles` = 8 (cycles D, E, F, G, H, I, J, L)

**Python Implementation**:
```python
# Adjust weights for 8 combined cycles
n_cycles = 8
data['WTMEC2YR_adj'] = data['WTMEC2YR'] / n_cycles
```

### Weight Selection Rationale

| Weight Type | Variable | Use Case |
|-------------|----------|----------|
| MEC 2-year | `WTMEC2YR` | Primary weight for exam-based analyses |
| Interview 2-year | `WTINT2YR` | For interview-only variables |
| Fasting subsample | `WTSAF2YR` | For fasting glucose/lipid analyses |

**Decision**: Use `WTMEC2YR` as all key variables (ferritin, hemoglobin) are from MEC examination.

### Subpopulation Analysis Weights

For analyses restricted to subgroups (e.g., IDWA only), continue using full-sample adjusted weights with domain indicators:

```python
# Domain analysis - use full weights with domain flag
data['domain_idwa'] = (data['idwa_status'] == 1).astype(int)
# Analysis includes all cases but estimates apply to IDWA domain
```

## Variance Estimation

### Taylor Series Linearization

NHANES complex survey design requires special variance estimation accounting for stratification and clustering.

**Design Variables**:
- `SDMVSTRA`: Masked variance pseudo-stratum (1-112)
- `SDMVPSU`: Masked variance pseudo-PSU (1-2 per stratum)

**Variance Formula**:
```
Var(θ̂) = Σ_h [n_h/(n_h-1)] × Σ_i (z_hi - z̄_h)²
```

Where:
- h = stratum
- i = PSU within stratum
- z_hi = weighted estimate from PSU

**Python Implementation**:
```python
from statsmodels.stats.weightstats import DescrStatsW
import numpy as np

# For descriptive statistics
wstats = DescrStatsW(data['outcome'], 
                     weights=data['WTMEC2YR_adj'],
                     ddof=0)

# Standard error
se = wstats.std / np.sqrt(wstats.nobs)
```

### Degrees of Freedom

```
df = Σ_h (n_h - 1) = number of PSUs - number of strata
```

For 8 combined cycles: approximately 120-140 degrees of freedom.

### Finite Population Correction

Not applied for NHANES public-use data as the sampling fraction is small relative to the US population.

## Primary Analysis: Survey-Weighted Linear Regression

### Model Specification

**Primary Model**:
```
log(Ferritin) = β₀ + β₁(Supplement_Use) + β₂(Age) + β₃(BMI) + β₄(Race) + β₅(Cycle) + ε
```

Where:
- Outcome: Natural log of ferritin (ng/mL)
- Primary predictor: Iron supplement use (binary or categorical)
- Covariates: Age, BMI, race/ethnicity, NHANES cycle

**Python Implementation**:
```python
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Survey-weighted regression
model = smf.wls(
    formula='np.log(LBXFER) ~ iron_supplement + RIDAGEYR + BMXBMI + C(RIDRETH1) + C(SDDSRVYR)',
    data=data,
    weights=data['WTMEC2YR_adj']
)

results = model.fit()
print(results.summary())
```

### Geometric Mean Interpretation

Because ferritin is log-transformed, coefficients represent ratios of geometric means.

**Interpretation**:
```
If β₁ = 0.15 for supplement use:
Geometric mean ratio = exp(0.15) = 1.16
Interpretation: 16% higher geometric mean ferritin in supplement users
```

**Confidence Interval**:
```
95% CI for ratio: [exp(β₁ - 1.96×SE), exp(β₁ + 1.96×SE)]
```

## Log Transformation of Ferritin Rationale

### Statistical Justification

Ferritin exhibits a highly right-skewed distribution with the following characteristics:

| Statistic | Raw Ferritin | Log(Ferritin) |
|-----------|--------------|---------------|
| Skewness | 3.5-5.0 | 0.1-0.5 |
| Kurtosis | 15-25 | 2.5-3.5 |
| Shapiro-Wilk p | <0.001 | 0.05-0.20 |

### Biological Justification

1. **Multiplicative Nature**: Iron metabolism processes are multiplicative rather than additive
2. **Reference Intervals**: Clinical reference ranges are often expressed in geometric terms
3. **Heteroscedasticity**: Log transformation stabilizes variance across predicted values

### Transformation Details

**Natural Log vs. Log10**:
- Use natural log (ln) for regression coefficients
- Conversion: ln(x) = 2.303 × log10(x)
- Both produce identical p-values and model fit

**Handling Zero/Negative Values**:
```python
# For values below detection limit
data['LBXFER_adj'] = np.where(
    data['LBXFER'] <= 0, 
    LLOD / sqrt(2),  # Assign LLOD/√2 (standard approach)
    data['LBXFER']
)

# Then log transform
data['log_ferritin'] = np.log(data['LBXFER_adj'])
```

## Geometric Mean Ratios vs. Arithmetic Means

### Comparison of Approaches

| Metric | Arithmetic Mean | Geometric Mean |
|--------|-----------------|----------------|
| Formula | Σxᵢ/n | exp(Σln(xᵢ)/n) |
| Sensitive to outliers | Yes | No |
| Suitable for ferritin | No | Yes |
| CI calculation | Symmetric | Asymmetric (back-transformed) |

### Reporting Standards

**Primary Presentation**: Geometric means with 95% confidence intervals

**Calculation**:
```python
# Geometric mean
gmean = np.exp(np.average(np.log(ferritin), weights=weights))

# 95% CI for geometric mean
se_log = np.sqrt(np.average((np.log(ferritin) - np.log(gmean))**2, weights=weights)) / np.sqrt(n)
ci_lower = np.exp(np.log(gmean) - 1.96 * se_log)
ci_upper = np.exp(np.log(gmean) + 1.96 * se_log)
```

## Multiple Comparison Corrections

### Primary Outcomes

| Outcome | Variable | Comparison |
|---------|----------|------------|
| Ferritin | `LBXFER` | Primary |
| Hemoglobin | `LBXHGB` | Secondary |
| Transferrin saturation | `LBXSTR` | Secondary |

### Correction Methods

**Family-Wise Error Rate (Bonferroni)**:
```
Adjusted α = 0.05 / m
Where m = number of comparisons
```

For 3 biomarkers: α_adjusted = 0.05/3 = 0.017

**False Discovery Rate (Benjamini-Hochberg)**:
```python
from statsmodels.stats.multitest import multipletests

p_values = [p1, p2, p3]
reject, pvals_corrected, _, _ = multipletests(p_values, alpha=0.05, method='fdr_bh')
```

### Decision Rule

Use Bonferroni correction for primary hypothesis testing; report both corrected and uncorrected p-values.

## Sensitivity Analyses Plan

### Analysis 1: Alternative IDWA Definitions

| Scenario | Ferritin Threshold | Hemoglobin Threshold |
|----------|-------------------|---------------------|
| Primary | <15 ng/mL | ≥12 g/dL |
| Conservative | <12 ng/mL | ≥12 g/dL |
| Expanded | <20 ng/mL | ≥12 g/dL |

### Analysis 2: Inflammation Adjustment

```python
# Exclude elevated CRP (inflammation elevates ferritin)
no_inflammation = data[data['CRP'] <= 10.0]  # mg/L
```

### Analysis 3: Supplement Dose Categories

| Dose Category | Elemental Iron | Analysis Type |
|---------------|----------------|---------------|
| None | 0 mg | Reference |
| Low | <18 mg/day | Categorical |
| Moderate | 18-65 mg/day | Categorical |
| High | >65 mg/day | Categorical |

### Analysis 4: Time Trends

```python
# Test for cycle × supplement interaction
model = smf.wls(
    'log_ferritin ~ supplement * C(cycle) + covariates',
    data=data,
    weights=data['WTMEC2YR_adj']
)
```

### Analysis 5: Propensity Score Adjustment

For potential confounding by indication:

```python
from sklearn.linear_model import LogisticRegression

# Propensity score: probability of supplement use
ps_model = LogisticRegression()
ps_model.fit(X_covariates, y_supplement)
propensity_scores = ps_model.predict_proba(X_covariates)[:, 1]

# Inverse probability weighting
ipw_weights = data['WTMEC2YR_adj'] / propensity_scores
```

### Analysis 6: Complete Case vs. Multiple Imputation

Compare results with:
1. Complete case analysis (primary)
2. Multiple imputation for missing ferritin (sensitivity)

```python
from sklearn.impute import IterativeImputer

# Multiple imputation (5 imputations)
imputer = IterativeImputer(max_iter=10, n_nearest_features=5)
imputed_data = imputer.fit_transform(data[['LBXFER', 'LBXHGB', 'BMXBMI']])
```

## Handling Below-Detection-Limit Ferritin Values

### Detection Limits by Cycle

| Cycle | LLOD (ng/mL) | % Below LLOD |
|-------|--------------|--------------|
| D | 0.5 | <1% |
| E | 0.5 | <1% |
| F | 0.5 | <1% |
| I | 0.5 | <1% |
| J | 0.5 | <1% |

### Approaches for Values < LLOD

**Method 1: Substitution (Primary)**
```python
# Assign LLOD/√2 (standard EPA approach)
LLOD_substitute = LLOD / np.sqrt(2)
data['LBXFER_imp'] = np.where(
    data['LBDFER'] == 1,  # Below detection flag
    LLOD_substitute,
    data['LBXFER']
)
```

**Method 2: Maximum Likelihood Estimation**
```python
# Tobit regression for censored data
# (Requires specialized software)
```

**Method 3: Sensitivity Analysis**
```python
# Test range of imputed values: LLOD/2 to LLOD
for impute_val in [LLOD/2, LLOD/np.sqrt(2), LLOD]:
    data['LBXFER_imp'] = np.where(data['LBDFER'] == 1, impute_val, data['LBXFER'])
    # Run analysis
```

### Impact Assessment

Given <1% of ferritin values are below LLOD, substitution method has minimal impact on results.

## Regression Diagnostics

### Residual Analysis

```python
# Check residuals
residuals = results.resid
fitted = results.fittedvalues

# Plots
plt.scatter(fitted, residuals)  # Residuals vs fitted
plt.hist(residuals, bins=30)     # Distribution of residuals
sm.qqplot(residuals)             # Q-Q plot
```

### Influence Statistics

```python
# Cook's distance
influence = results.get_influence()
cooks_d = influence.cooks_distance[0]

# Identify influential points
influential = np.where(cooks_d > 4/len(data))[0]
```

### Weight Diagnostics

```python
# Extreme weights
weight_mean = data['WTMEC2YR_adj'].mean()
weight_sd = data['WTMEC2YR_adj'].std()
extreme_weights = data[
    (data['WTMEC2YR_adj'] > weight_mean + 3*weight_sd) |
    (data['WTMEC2YR_adj'] < weight_mean - 3*weight_sd)
]
```

## Software and Packages

### Primary Analysis Tools

```python
# Required packages
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
```

### Specialized Survey Analysis

```python
# For complex survey analysis
# Note: statsmodels survey functionality is limited
# Consider using R survey package via rpy2 for full functionality
```

## Sample Size and Power

### Minimum Detectable Effect

With ~1,000 IDWA cases and ~9,000 controls:

| Parameter | Value |
|-----------|-------|
| IDWA cases | ~1,000 |
| Iron sufficient | ~9,000 |
| Expected supplement use in IDWA | 40% |
| α (two-tailed) | 0.05 |
| Power | 80% |
| **Minimum detectable difference in ferritin** | **~15% geometric mean ratio** |

### Precision Estimates

| Outcome | Expected SE | 95% CI Width |
|---------|-------------|--------------|
| Ferritin (log scale) | 0.05 | ±0.10 |
| Hemoglobin | 0.08 g/dL | ±0.16 |
| TSAT | 1.5% | ±3.0% |

## References

1. Korn EL, Graubard BI. Analysis of Health Surveys. Wiley; 1999.
2. Rust KF, Rao JNK. Variance estimation for complex surveys. Survey Methodology 1996;22(1):33-43.
3. Lumley T. Complex Surveys: A Guide to Analysis Using R. Wiley; 2010.
4. Hornung RW, Reed LD. Estimation of average concentration in the presence of nondetectable values. Appl Occup Environ Hyg 1990;5(1):46-51.
5. Mei Z, et al. Serum ferritin is associated with markers of inflammation. J Nutr 2005;135(5):1201-8.
