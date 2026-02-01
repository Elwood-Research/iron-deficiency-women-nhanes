# Study Variables: Methods Specification

## Study Population Definition

### Inclusion Criteria
1. **Age:** 18-45 years at examination (`RIDAGEYR`)
2. **Sex:** Female (`RIAGENDR = 2`)
3. **Not pregnant** (exclusion to be applied when pregnancy variable identified)
4. **Valid ferritin measurement** (`LBXFER` not missing)
5. **Valid hemoglobin measurement** (`LBXHGB` not missing)
6. **Valid survey weight** (`WTMEC2YR > 0`)

### Exclusion Criteria
1. Pregnant women
2. Missing ferritin or hemoglobin data
3. Age outside 18-45 range
4. Iron deficiency anemia (may be analyzed separately)

---

## Outcome Variables

### 1. Serum Ferritin (Primary Outcome)

| Attribute | Specification |
|-----------|---------------|
| **Variable** | `LBXFER` |
| **Source** | FERTIN dataset |
| **Unit** | ng/mL |
| **Transformation** | Natural log for regression (`ln_ferritin`) |
| **Clinical cutoffs** | <15 ng/mL (deficiency), <25 ng/mL (mild deficiency) |

**Derivation:**
```python
df['ln_ferritin'] = np.log(df['LBXFER'])
```

---

### 2. Iron Status Classification

| Category | Definition | Variables |
|----------|------------|-----------|
| **IDWA (Primary)** | Ferritin <15 AND Hemoglobin ≥12 | `LBXFER < 15` & `LBXHGB >= 12` |
| **IDWA (Alternative)** | Ferritin <25 AND Hemoglobin ≥12 | `LBXFER < 25` & `LBXHGB >= 12` |
| **Iron Deficiency Anemia** | Ferritin <15 AND Hemoglobin <12 | `LBXFER < 15` & `LBXHGB < 12` |
| **Normal Iron** | Ferritin ≥15 AND Hemoglobin ≥12 | `LBXFER >= 15` & `LBXHGB >= 12` |

---

### 3. Secondary Biomarkers

| Variable | NHANES Code | Unit | Expected Direction with Supplementation |
|----------|-------------|------|----------------------------------------|
| Serum Iron | `LBXIRN` | µg/dL | Increase |
| TIBC | `LBXTIB` | µg/dL | Decrease |
| Transferrin Saturation | `LBDPCT` | % | Increase |

---

## Predictor Variables

### 1. Iron Supplement Use (Primary Exposure)

| Variable | Source | Unit |
|----------|--------|------|
| Total iron from supplements | `DSQTIRON` (DSQTOT) | mg/day |

**Categories:**

| Category | Dose Range | Description |
|----------|------------|-------------|
| None | 0 mg | Reference group |
| Low | >0 to <18 mg | Multivitamin-level |
| Moderate | 18-65 mg | Standard therapeutic |
| High | >65 mg | High therapeutic |

**Derivation:**
```python
conditions = [
    df['DSQTIRON'] == 0,
    (df['DSQTIRON'] > 0) & (df['DSQTIRON'] < 18),
    (df['DSQTIRON'] >= 18) & (df['DSQTIRON'] <= 65),
    df['DSQTIRON'] > 65
]
choices = ['None', 'Low', 'Moderate', 'High']
df['iron_dose_cat'] = np.select(conditions, choices)
```

---

## Covariates

### 1. Demographics

| Variable | NHANES Code | Type | Categories |
|----------|-------------|------|------------|
| Age | `RIDAGEYR` | Continuous | 18-45 years |
| Age Group | Derived | Categorical | 18-25, 26-35, 36-45 |
| Race/Ethnicity | `RIDRETH1` | Categorical | Mexican American, Other Hispanic, Non-Hispanic White, Non-Hispanic Black, Other |

**Race/Ethnicity Coding:**
- 1 = Mexican American
- 2 = Other Hispanic  
- 3 = Non-Hispanic White
- 4 = Non-Hispanic Black
- 5 = Other Race - Including Multi-Racial

---

### 2. Socioeconomic

| Variable | NHANES Code | Type | Handling |
|----------|-------------|------|----------|
| Poverty Income Ratio | `INDFMPIR` | Continuous | Top-coded at 5.0; missing imputed with median |
| Poverty Category | Derived | Categorical | <1.0, 1.0-1.99, 2.0-3.99, ≥4.0 |

---

### 3. Anthropometric

| Variable | NHANES Code | Type | Categories |
|----------|-------------|------|------------|
| BMI | `BMXBMI` | Continuous | kg/m² |
| BMI Category | Derived | Categorical | Underweight(<18.5), Normal(18.5-24.9), Overweight(25-29.9), Obese(≥30) |

---

## Survey Design Variables

| Variable | NHANES Code | Purpose | Adjustment |
|----------|-------------|---------|------------|
| MEC Weight | `WTMEC2YR` | Sample weight | Divide by 6 for pooled cycles |
| Strata | `SDMVSTRA` | Variance estimation | Include in survey design |
| PSU | `SDMVPSU` | Variance estimation | Include in survey design |

**Weight Adjustment for Pooled Cycles:**
```python
df['wtmec2yr_adj'] = df['WTMEC2YR'] / 6  # 6 cycles
```

---

## Data Merging Strategy

### Merge Order
1. Start with DEMO (demographics + weights)
2. Merge with CBC (hemoglobin, hematocrit)
3. Merge with FERTIN (ferritin)
4. Merge with FETIB (iron, TIBC, TSAT) - where available
5. Merge with DSQTOT (supplement data)
6. Merge with BMX (BMI)
7. Apply inclusion/exclusion criteria

**Merge Key:** `SEQN` (participant identifier)

---

## Variable Summary by Analysis

### Primary Analysis (H1: Supplementation → Ferritin)
- **Outcome:** `ln_ferritin` (continuous)
- **Exposure:** `iron_supp_user` (binary) or `iron_dose_cat` (4-category)
- **Covariates:** age, race, poverty_ratio, bmi, cycle
- **Design:** wtmec2yr_adj, sdmvstra, sdmvpsu

### Secondary Analyses
- **H3 (Demographics):** Outcome = `idwa` (binary), Predictors = demographics
- **H4 (Biomarkers):** Outcomes = serum_iron, tibc, transferrin_sat
- **H5 (Dose comparison):** Compare Low vs. Moderate dose categories

---

## Sample Size Estimates

| Population | Expected n | Purpose |
|------------|------------|---------|
| Women 18-45 (all cycles) | ~8,000-10,000 | Base population |
| After exclusions | ~6,000-8,000 | Analysis sample |
| With IDWA | ~700-960 | Primary analysis population |
| IDWA + Supplement use | ~200-300 | Exposure contrast |

---

*Variable specification for methods section*  
*Study: Iron Deficiency Without Anemia in Women*  
*Date: 2026-01-31*
