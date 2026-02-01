# Variable Operationalization: NHANES IDWA Study

## Overview

This document provides detailed operational definitions for all variables used in the NHANES Iron Deficiency Without Anemia (IDWA) study. Each variable includes its NHANES source, original coding, derived transformation, and analytic handling.

---

## 1. Outcome Variables

### 1.1 Primary Outcome: Serum Ferritin

| Attribute | Specification |
|-----------|---------------|
| **NHANES Variable** | `LBXFER` |
| **Description** | Serum ferritin concentration |
| **Unit** | ng/mL (nanograms per milliliter) |
| **Alternative Unit** | µg/L (micrograms per liter) - equivalent to ng/mL |
| **Secondary Variable** | `LBDFERSI` - ferritin in µg/L (SI units) |
| **Target Population** | Females 12-49 years (varies by cycle) |

**Operational Definitions:**

```python
# Python pseudo-code for ferritin handling
def process_ferritin(df):
    """
    Process ferritin variable for analysis
    """
    # Create analysis variable
    df['ferritin_ng_ml'] = df['LBXFER']
    
    # Handle detection limits (values of 2 typically indicate below detection)
    # Consult cycle-specific documentation for detection limits
    df['ferritin_censored'] = np.where(df['LBXFER'] <= 2, 2, df['LBXFER'])
    
    # Create log-transformed version for regression
    df['ln_ferritin'] = np.log(df['ferritin_ng_ml'])
    
    # Create iron deficiency indicator
    df['iron_deficient'] = (df['ferritin_ng_ml'] < 15).astype(int)
    
    # Alternative threshold for sensitivity analysis
    df['iron_deficient_alt'] = (df['ferritin_ng_ml'] < 25).astype(int)
    
    return df
```

**Clinical Thresholds:**
| Threshold | Value | Interpretation |
|-----------|-------|----------------|
| Severe deficiency | <15 ng/mL | Depleted iron stores |
| Mild deficiency | 15-25 ng/mL | Low iron stores |
| Normal | ≥25 ng/mL | Adequate iron stores |

**Detection Limits by Cycle:**
- Values at or below 2 ng/mL typically indicate below detection limit
- Check cycle-specific laboratory documentation for exact limits

---

### 1.2 Secondary Outcomes: Iron Biomarkers

#### 1.2.1 Serum Iron

| Attribute | Specification |
|-----------|---------------|
| **NHANES Variable** | `LBXIRN` |
| **Description** | Serum iron concentration |
| **Unit** | µg/dL (micrograms per deciliter) |
| **SI Unit Variable** | `LBDIRNSI` (µmol/L) |
| **Availability** | Limited cycles (D, J primarily) |

```python
# Python pseudo-code
def process_serum_iron(df):
    """
    Process serum iron variable
    """
    df['serum_iron'] = df['LBXIRN']
    
    # Log transform if needed
    df['ln_serum_iron'] = np.log(df['serum_iron'])
    
    return df
```

**Clinical Range:**
- Reference range for women: 60-170 µg/dL
- Lower values indicate iron deficiency

#### 1.2.2 Total Iron Binding Capacity (TIBC)

| Attribute | Specification |
|-----------|---------------|
| **NHANES Variable** | `LBXTIB` |
| **Description** | Total iron binding capacity |
| **Unit** | µg/dL |
| **SI Unit Variable** | `LBDTIBSI` (µmol/L) |
| **Availability** | Limited cycles (D, J primarily) |

```python
# Python pseudo-code
def process_tibc(df):
    """
    Process TIBC variable
    """
    df['tibc'] = df['LBXTIB']
    
    # Higher TIBC indicates iron deficiency (inverse relationship)
    df['ln_tibc'] = np.log(df['tibc'])
    
    return df
```

**Clinical Range:**
- Reference range: 240-450 µg/dL
- Elevated TIBC indicates iron deficiency (more transferrin available)

#### 1.2.3 Transferrin Saturation

| Attribute | Specification |
|-----------|---------------|
| **NHANES Variable** | `LBDPCT` |
| **Description** | Transferrin saturation percentage |
| **Unit** | Percent (%) |
| **Calculation** | (Serum Iron / TIBC) × 100 |
| **Availability** | Where iron and TIBC both available |

```python
# Python pseudo-code
def calculate_transferrin_saturation(df):
    """
    Calculate transferrin saturation
    """
    # Use pre-calculated if available
    if 'LBDPCT' in df.columns:
        df['transferrin_sat'] = df['LBDPCT']
    else:
        # Calculate from iron and TIBC
        df['transferrin_sat'] = (df['LBXIRN'] / df['LBXTIB']) * 100
    
    # Cap at 100% for biological plausibility
    df['transferrin_sat'] = df['transferrin_sat'].clip(upper=100)
    
    return df
```

**Clinical Thresholds:**
- Normal: 20-50%
- Iron deficiency: <20%
- Iron overload: >50%

---

### 1.3 Categorical Outcome: IDWA Status

**Primary Definition:**

```python
# Python pseudo-code for IDWA classification
def classify_idwa(df):
    """
    Create IDWA and related iron status classifications
    """
    # Primary definition: ferritin <15 AND hemoglobin ≥12
    df['idwa'] = ((df['LBXFER'] < 15) & (df['LBXHGB'] >= 12)).astype(int)
    
    # Alternative definition: ferritin <25 AND hemoglobin ≥12
    df['idwa_alt'] = ((df['LBXFER'] < 25) & (df['LBXHGB'] >= 12)).astype(int)
    
    # Four-category classification
    conditions = [
        (df['LBXFER'] >= 15) & (df['LBXHGB'] >= 12),  # Normal
        (df['LBXFER'] < 15) & (df['LBXHGB'] >= 12),   # IDWA
        (df['LBXFER'] < 15) & (df['LBXHGB'] < 12),    # IDA
        (df['LBXFER'] >= 15) & (df['LBXHGB'] < 12),   # Anemia without ID
    ]
    choices = ['Normal', 'IDWA', 'IDA', 'Anemia_no_ID']
    df['iron_status_4cat'] = np.select(conditions, choices, default='Unknown')
    
    # Binary iron deficiency (regardless of anemia)
    df['iron_deficiency'] = (df['LBXFER'] < 15).astype(int)
    
    # Binary anemia (regardless of iron status)
    df['anemia'] = (df['LBXHGB'] < 12).astype(int)
    
    return df
```

**Classification Table:**

| Category | Ferritin | Hemoglobin | Variable Value |
|----------|----------|------------|----------------|
| Normal | ≥15 ng/mL | ≥12 g/dL | "Normal" |
| IDWA | <15 ng/mL | ≥12 g/dL | "IDWA" |
| IDA | <15 ng/mL | <12 g/dL | "IDA" |
| Anemia without ID | ≥15 ng/mL | <12 g/dL | "Anemia_no_ID" |

---

## 2. Predictor Variables

### 2.1 Primary Predictor: Iron Supplement Use

#### 2.1.1 Total Iron from Supplements

| Attribute | Specification |
|-----------|---------------|
| **NHANES Variable** | `DSQTIRON` |
| **Dataset** | DSQTOT (Total Dietary Supplements) |
| **Description** | Total iron from all supplements (mg/day) |
| **Unit** | mg (milligrams) |
| **Years Available** | E, F, G, H, I, J, L (2007-2022) |

```python
# Python pseudo-code for supplement variable creation
def create_supplement_variables(df):
    """
    Create supplement use and dose category variables
    """
    # Handle missing - assume 0 if missing (conservative)
    df['iron_supp_mg'] = df['DSQTIRON'].fillna(0)
    
    # Binary use indicator
    df['iron_supp_user'] = (df['iron_supp_mg'] > 0).astype(int)
    
    # Four-category dose classification
    conditions = [
        df['iron_supp_mg'] == 0,
        (df['iron_supp_mg'] > 0) & (df['iron_supp_mg'] < 18),
        (df['iron_supp_mg'] >= 18) & (df['iron_supp_mg'] <= 65),
        df['iron_supp_mg'] > 65
    ]
    choices = ['None', 'Low', 'Moderate', 'High']
    df['iron_supp_dose_cat'] = np.select(conditions, choices, default='Unknown')
    
    # Ordered categorical for trend tests
    dose_map = {'None': 0, 'Low': 1, 'Moderate': 2, 'High': 3}
    df['iron_supp_dose_ord'] = df['iron_supp_dose_cat'].map(dose_map)
    
    # Multivitamin vs dedicated indicator
    df['multivitamin_only'] = ((df['iron_supp_mg'] > 0) & 
                                (df['iron_supp_mg'] < 18)).astype(int)
    df['dedicated_iron'] = (df['iron_supp_mg'] >= 18).astype(int)
    
    return df
```

**Dose Category Definitions:**

| Category | Iron Dose Range | Typical Source | Rationale |
|----------|----------------|----------------|-----------|
| None | 0 mg | N/A | Reference group |
| Low | >0 to <18 mg | Multivitamins | Standard multi dose |
| Moderate | 18-65 mg | Iron supplements | Therapeutic range |
| High | >65 mg | High-dose supplements | Prescription strength |

**Handling Missing Data:**
- If DSQTIRON is missing: Assume no supplementation (conservative approach)
- Flag participants with missing supplement data for sensitivity analysis

---

### 2.2 Supplement Duration (If Available)

| Attribute | Specification |
|-----------|---------------|
| **NHANES Variables** | Supplement-specific files (DSQ) |
| **Description** | Duration of supplement use |
| **Note** | May need to construct from detailed supplement files |

```python
# Python pseudo-code for duration (if available)
def create_duration_variable(df):
    """
    Create supplement duration categories if data available
    """
    # This requires detailed supplement file analysis
    # Pseudocode for illustration
    
    if 'supp_duration_days' in df.columns:
        conditions = [
            df['supp_duration_days'] < 30,
            (df['supp_duration_days'] >= 30) & (df['supp_duration_days'] < 180),
            (df['supp_duration_days'] >= 180) & (df['supp_duration_days'] < 365),
            df['supp_duration_days'] >= 365
        ]
        choices = ['<1_month', '1-6_months', '6-12_months', '>12_months']
        df['supp_duration_cat'] = np.select(conditions, choices)
    
    return df
```

---

## 3. Covariates

### 3.1 Demographics

#### 3.1.1 Age

| Attribute | Specification |
|-----------|---------------|
| **NHANES Variable** | `RIDAGEYR` |
| **Dataset** | DEMO (Demographics) |
| **Description** | Age at screening adjudicated (years) |
| **Type** | Integer (0-120) |
| **Range for study** | 18-45 (inclusive) |

```python
# Python pseudo-code
def process_age(df):
    """
    Process age variable
    """
    df['age'] = df['RIDAGEYR']
    
    # Inclusion flag
    df['age_eligible'] = ((df['age'] >= 18) & (df['age'] <= 45)).astype(int)
    
    # Categorical for stratification
    conditions = [
        (df['age'] >= 18) & (df['age'] <= 25),
        (df['age'] >= 26) & (df['age'] <= 35),
        (df['age'] >= 36) & (df['age'] <= 45)
    ]
    choices = ['18-25', '26-35', '36-45']
    df['age_group'] = np.select(conditions, choices, default='Other')
    
    return df
```

#### 3.1.2 Sex/Gender

| Attribute | Specification |
|-----------|---------------|
| **NHANES Variable** | `RIAGENDR` |
| **Dataset** | DEMO |
| **Description** | Gender of participant |
| **Values** | 1=Male, 2=Female |
| **Study inclusion** | 2 (Female only) |

```python
def process_sex(df):
    """
    Process sex variable
    """
    df['sex'] = df['RIAGENDR']
    df['female'] = (df['RIAGENDR'] == 2).astype(int)
    
    return df
```

#### 3.1.3 Race/Ethnicity

| Attribute | Specification |
|-----------|---------------|
| **NHANES Variable (Primary)** | `RIDRETH1` |
| **NHANES Variable (Extended)** | `RIDRETH3` (2011+) |
| **Dataset** | DEMO |
| **Description** | Race/Hispanic origin (recode) |

**RIDRETH1 Coding:**

| Code | Category | Description |
|------|----------|-------------|
| 1 | Mexican American | Mexican American |
| 2 | Other Hispanic | Other Hispanic |
| 3 | Non-Hispanic White | Non-Hispanic White |
| 4 | Non-Hispanic Black | Non-Hispanic Black |
| 5 | Other | Other Race - Including Multi-Racial |

```python
def process_race_ethnicity(df):
    """
    Process race/ethnicity variables
    """
    # Primary variable (all cycles)
    race_map = {
        1: 'Mexican_American',
        2: 'Other_Hispanic',
        3: 'Non_Hispanic_White',
        4: 'Non_Hispanic_Black',
        5: 'Other'
    }
    df['race_ethnicity'] = df['RIDRETH1'].map(race_map)
    
    # Create dummy variables for regression
    df['race_mexican_am'] = (df['RIDRETH1'] == 1).astype(int)
    df['race_other_hisp'] = (df['RIDRETH1'] == 2).astype(int)
    df['race_nh_white'] = (df['RIDRETH1'] == 3).astype(int)
    df['race_nh_black'] = (df['RIDRETH1'] == 4).astype(int)
    # Other is reference category
    
    # Collapsed categories for some analyses
    conditions = [
        df['RIDRETH1'].isin([1, 2]),
        df['RIDRETH1'] == 3,
        df['RIDRETH1'] == 4,
        df['RIDRETH1'] == 5
    ]
    choices = ['Hispanic', 'Non_Hispanic_White', 'Non_Hispanic_Black', 'Other']
    df['race_collapsed'] = np.select(conditions, choices)
    
    return df
```

---

### 3.2 Socioeconomic Variables

#### 3.2.1 Poverty Income Ratio

| Attribute | Specification |
|-----------|---------------|
| **NHANES Variable** | `INDFMPIR` |
| **Dataset** | DEMO |
| **Description** | Family income to poverty ratio |
| **Type** | Continuous (0-5.0+) |
| **Special Values** | 5.0 = ≥5.0 (top-coded) |
| **Missing** | Often missing (~5-10%) |

```python
def process_poverty_ratio(df):
    """
    Process poverty income ratio
    """
    df['poverty_ratio'] = df['INDFMPIR']
    
    # Missing indicator
    df['poverty_missing'] = df['poverty_ratio'].isna().astype(int)
    
    # Impute median for missing (sensitivity analysis)
    median_poverty = df['poverty_ratio'].median()
    df['poverty_ratio_imputed'] = df['poverty_ratio'].fillna(median_poverty)
    
    # Categorical for descriptive tables
    conditions = [
        df['poverty_ratio'] < 1.0,
        (df['poverty_ratio'] >= 1.0) & (df['poverty_ratio'] < 2.0),
        (df['poverty_ratio'] >= 2.0) & (df['poverty_ratio'] < 4.0),
        df['poverty_ratio'] >= 4.0
    ]
    choices = ['<1.0', '1.0-1.99', '2.0-3.99', '>=4.0']
    df['poverty_cat'] = np.select(conditions, choices, default='Missing')
    
    return df
```

---

### 3.3 Anthropometric Variables

#### 3.3.1 Body Mass Index (BMI)

| Attribute | Specification |
|-----------|---------------|
| **NHANES Variable** | `BMXBMI` |
| **Dataset** | BMX (Body Measures) |
| **Description** | Body Mass Index (kg/m²) |
| **Type** | Continuous |
| **Missing** | ~2-5% |

```python
def process_bmi(df):
    """
    Process BMI variable
    """
    df['bmi'] = df['BMXBMI']
    
    # Categorical (WHO standards)
    conditions = [
        df['bmi'] < 18.5,
        (df['bmi'] >= 18.5) & (df['bmi'] < 25),
        (df['bmi'] >= 25) & (df['bmi'] < 30),
        df['bmi'] >= 30
    ]
    choices = ['Underweight', 'Normal', 'Overweight', 'Obese']
    df['bmi_category'] = np.select(conditions, choices, default='Missing')
    
    # Binary indicators
    df['bmi_underweight'] = (df['bmi'] < 18.5).astype(int)
    df['bmi_normal'] = ((df['bmi'] >= 18.5) & (df['bmi'] < 25)).astype(int)
    df['bmi_overweight'] = ((df['bmi'] >= 25) & (df['bmi'] < 30)).astype(int)
    df['bmi_obese'] = (df['bmi'] >= 30).astype(int)
    
    return df
```

**BMI Categories:**

| Category | BMI Range | Clinical Meaning |
|----------|-----------|------------------|
| Underweight | <18.5 kg/m² | Low body weight |
| Normal | 18.5-24.9 kg/m² | Healthy weight |
| Overweight | 25-29.9 kg/m² | Excess weight |
| Obese | ≥30 kg/m² | Significant excess weight |

---

## 4. Survey Design Variables

### 4.1 Sampling Weights

| Attribute | Specification |
|-----------|---------------|
| **NHANES Variable** | `WTMEC2YR` |
| **Dataset** | DEMO |
| **Description** | Full sample 2-year MEC exam weight |
| **Usage** | For all analyses involving examination data |
| **Note** | Must be divided by number of cycles when pooling |

```python
def process_survey_weights(df, n_cycles=6):
    """
    Process survey weights for pooled analysis
    """
    # Adjust weights for pooling
    df['wtmec2yr_adj'] = df['WTMEC2YR'] / n_cycles
    
    # Ensure positive weights
    df['wtmec2yr_adj'] = df['wtmec2yr_adj'].clip(lower=0)
    
    return df
```

### 4.2 Variance Estimation Variables

| Variable | Dataset | Description | Usage |
|----------|---------|-------------|-------|
| `SDMVSTRA` | DEMO | Masked variance pseudo-stratum | Variance estimation |
| `SDMVPSU` | DEMO | Masked variance pseudo-PSU | Variance estimation |

```python
def verify_survey_design(df):
    """
    Verify survey design variables are complete
    """
    required_vars = ['WTMEC2YR', 'SDMVSTRA', 'SDMVPSU']
    
    for var in required_vars:
        if var not in df.columns:
            raise ValueError(f"Missing required survey variable: {var}")
        
        missing_pct = df[var].isna().mean() * 100
        print(f"{var}: {missing_pct:.1f}% missing")
    
    # Check for valid weights
    valid_weights = (df['WTMEC2YR'] > 0).sum()
    print(f"Participants with valid weights: {valid_weights}")
    
    return df
```

---

## 5. Hemoglobin and Anemia Variables

### 5.1 Hemoglobin

| Attribute | Specification |
|-----------|---------------|
| **NHANES Variable** | `LBXHGB` |
| **Dataset** | CBC (Complete Blood Count) |
| **Description** | Hemoglobin concentration |
| **Unit** | g/dL (grams per deciliter) |

**Anemia Thresholds for Women:**

| Population | Threshold | Source |
|------------|-----------|--------|
| Non-pregnant women | <12.0 g/dL | WHO standard |
| Pregnant women | <11.0 g/dL | WHO standard |

```python
def process_hemoglobin(df):
    """
    Process hemoglobin and create anemia indicator
    """
    df['hemoglobin'] = df['LBXHGB']
    
    # Anemia indicator (non-pregnant women)
    df['anemia'] = (df['hemoglobin'] < 12.0).astype(int)
    
    # Anemia severity (optional)
    conditions = [
        df['hemoglobin'] >= 12.0,
        (df['hemoglobin'] >= 11.0) & (df['hemoglobin'] < 12.0),
        (df['hemoglobin'] >= 8.0) & (df['hemoglobin'] < 11.0),
        df['hemoglobin'] < 8.0
    ]
    choices = ['None', 'Mild', 'Moderate', 'Severe']
    df['anemia_severity'] = np.select(conditions, choices)
    
    return df
```

---

## 6. Derived Composite Variables

### 6.1 Study Eligibility Flag

```python
def create_eligibility_flag(df):
    """
    Create overall study eligibility flag
    """
    conditions = [
        (df['age'] >= 18) & (df['age'] <= 45),  # Age eligible
        df['RIAGENDR'] == 2,                     # Female
        # Pregnancy exclusion - to be added when variable identified
        df['LBXFER'].notna(),                    # Has ferritin
        df['LBXHGB'].notna(),                    # Has hemoglobin
        df['WTMEC2YR'] > 0                       # Valid survey weight
    ]
    
    df['study_eligible'] = np.all(conditions, axis=0).astype(int)
    
    return df
```

### 6.2 NHANES Cycle Variable

| Attribute | Specification |
|-----------|---------------|
| **Source** | Dataset suffix or SDDSRVYR |
| **Values** | D=2005-06, E=2007-08, F=2009-10, G=2011-12, H=2013-14, I=2015-16, J=2017-18, L=2021-22 |
| **Purpose** | Control for temporal trends; subgroup analysis |

```python
def add_cycle_variable(df, cycle_code):
    """
    Add cycle variable based on data source
    """
    cycle_map = {
        'D': '2005-2006',
        'E': '2007-2008',
        'F': '2009-2010',
        'G': '2011-2012',
        'H': '2013-2014',
        'I': '2015-2016',
        'J': '2017-2018',
        'L': '2021-2022'
    }
    
    df['cycle_code'] = cycle_code
    df['cycle_years'] = cycle_map.get(cycle_code, 'Unknown')
    
    return df
```

---

## 7. Variable Summary Table

### 7.1 All Variables by Category

| Category | Variable Name | NHANES Source | Type | Role |
|----------|---------------|---------------|------|------|
| **Outcomes** | ferritin_ng_ml | LBXFER | Continuous | Primary outcome |
| | ln_ferritin | Derived | Continuous | Transformed outcome |
| | idwa | Derived | Binary | Primary case definition |
| | serum_iron | LBXIRN | Continuous | Secondary outcome |
| | tibc | LBXTIB | Continuous | Secondary outcome |
| | transferrin_sat | LBDPCT | Continuous | Secondary outcome |
| **Predictors** | iron_supp_mg | DSQTIRON | Continuous | Primary exposure |
| | iron_supp_user | Derived | Binary | Binary exposure |
| | iron_supp_dose_cat | Derived | Categorical (4) | Categorical exposure |
| **Covariates** | age | RIDAGEYR | Continuous | Adjustment |
| | age_group | Derived | Categorical (3) | Stratification |
| | race_ethnicity | RIDRETH1 | Categorical (5) | Adjustment |
| | poverty_ratio | INDFMPIR | Continuous | Adjustment |
| | bmi | BMXBMI | Continuous | Adjustment |
| | bmi_category | Derived | Categorical (4) | Stratification |
| **Survey** | wtmec2yr_adj | Derived | Continuous | Weight |
| | sdmvstra | SDMVSTRA | Integer | Strata |
| | sdmvpsu | SDMVPSU | Integer | PSU |
| **Design** | cycle_code | Derived | Categorical | Temporal control |
| | study_eligible | Derived | Binary | Inclusion |

---

## 8. Data Quality Flags

### 8.1 Quality Check Variables

```python
def create_quality_flags(df):
    """
    Create data quality flags for sensitivity analyses
    """
    # Ferritin below detection limit
    df['ferritin_bdl'] = (df['LBXFER'] <= 2).astype(int)
    
    # Extreme values (possible errors)
    df['ferritin_extreme'] = ((df['LBXFER'] > 500) | (df['LBXFER'] < 1)).astype(int)
    
    # Extreme supplement doses
    df['supp_dose_extreme'] = (df['DSQTIRON'] > 200).astype(int)
    
    # Missing key covariates
    df['key_covariates_missing'] = (df['INDFMPIR'].isna() | df['BMXBMI'].isna()).astype(int)
    
    # Inflammation indicator (if CRP available)
    if 'LBXCRP' in df.columns:
        df['inflammation'] = (df['LBXCRP'] > 5).astype(int)
    
    return df
```

---

*Variable Operationalization Document Version 1.0*  
*Date: 2026-01-31*  
*Study: Iron Deficiency Without Anemia in Women*
