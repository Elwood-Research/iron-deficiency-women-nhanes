# Study Population Definition: Iron Deficiency Without Anemia

## Overview

This document defines precise inclusion and exclusion criteria for identifying the study population: non-pregnant US women aged 18-45 years with iron deficiency without anemia (IDWA).

## Inclusion Criteria Algorithm

### Step 1: Demographic Filters

```
IF (RIAGENDR == 2) AND           # Female
   (RIDAGEYR >= 18) AND          # Adult
   (RIDAGEYR <= 45)              # Reproductive age
   THEN → Proceed to Step 2
ELSE → Exclude
```

### Step 2: Pregnancy Status Filter

```
IF (RIDEXPRG == 2) OR            # Explicitly not pregnant
   (RIDEXPRG == 3 AND            # Unknown pregnancy status
    pregnancy_selfreport == 0)   # AND not self-reported pregnant
   THEN → Proceed to Step 3
ELSE → Exclude
```

**Pregnancy Identification Variables**:
- Primary: `RIDEXPRG` (examination pregnancy test)
  - 1 = Yes (positive)
  - 2 = No (negative)
  - 3 = Unknown/not done
- Secondary: Self-reported pregnancy from questionnaire data

### Step 3: Laboratory Data Availability

```
IF (LBXHGB is NOT NULL) AND      # Has hemoglobin measurement
   (LBXFER is NOT NULL) AND      # Has ferritin measurement
   (WTMEC2YR > 0)                # Has valid survey weight
   THEN → Proceed to Step 4
ELSE → Exclude
```

### Step 4: IDWA Status Definition

```
IF (LBXHGB >= 12.0) AND          # NOT anemic (WHO threshold)
   (LBXFER < 15.0)               # Iron deficient (ferritin <15 ng/mL)
   THEN → IDWA = 1 (Case)
ELSE IF (LBXHGB >= 12.0) AND     # Not anemic
        (LBXFER >= 15.0)         # Not iron deficient
        THEN → Control = 1
ELSE → Anemic (excluded from primary analysis)
```

**Iron Deficiency Thresholds**:

| Biomarker | Deficiency Threshold | Source |
|-----------|---------------------|--------|
| Ferritin | <15 ng/mL | WHO/CDC standard for women |
| Transferrin saturation | <20% | Secondary criterion |
| Hemoglobin (non-pregnant) | <12.0 g/dL | WHO anemia definition |
| Hemoglobin (pregnant) | <11.0 g/dL | WHO anemia definition |

## Exclusion Criteria

### Primary Exclusions

| Criterion | Variable(s) | Exclusion Rule |
|-----------|-------------|----------------|
| Male | `RIAGENDR` | Exclude if == 1 |
| Age <18 or >45 | `RIDAGEYR` | Exclude if <18 or >45 |
| Pregnant | `RIDEXPRG` | Exclude if == 1 |
| Anemia | `LBXHGB` | Exclude if <12.0 g/dL |
| Missing ferritin | `LBXFER` | Exclude if NULL or missing |
| Missing hemoglobin | `LBXHGB` | Exclude if NULL or missing |
| Missing weight | `WTMEC2YR` | Exclude if 0 or NULL |

### Secondary Exclusions (Sensitivity Analyses)

| Criterion | Rationale | Implementation |
|-----------|-----------|----------------|
| Heavy menstrual bleeding | Potential confounder | Where questionnaire data available |
| Chronic inflammation | Elevated ferritin falsely normal | CRP >10 mg/L |
| Recent blood donation | Affects iron status | Self-reported donation within 3 months |
| Known hemoglobinopathy | Affects hemoglobin interpretation | Self-reported sickle cell, thalassemia |
| Cancer treatment | Affects iron metabolism | Self-reported active treatment |

## Flow Diagram Text Description

```
NHANES 2005-2022 (8 cycles)
├── Total participants: ~80,000
│
├── Step 1: Female gender
│   ├── Eligible: ~40,000
│   └── Excluded (male): ~40,000
│
├── Step 2: Age 18-45
│   ├── Eligible: ~16,000
│   └── Excluded (age): ~24,000
│
├── Step 3: Not pregnant
│   ├── Eligible: ~14,500
│   └── Excluded (pregnant): ~1,500
│
├── Step 4: Complete laboratory data
│   ├── Eligible: ~12,000
│   └── Excluded (missing data): ~2,500
│
├── Step 5: Not anemic (Hb ≥12)
│   ├── Eligible: ~11,000
│   └── Excluded (anemic): ~1,000
│
└── FINAL IDWA SAMPLE
    ├── IDWA cases (ferritin <15): ~1,500-2,000
    └── Iron sufficient controls: ~9,000-9,500
```

## Expected Sample Size Calculations

### By NHANES Cycle

| Cycle | Years | Total Women 18-45 | Expected IDWA* | Iron Sufficient |
|-------|-------|-------------------|----------------|-----------------|
| D | 2005-2006 | ~2,000 | ~200 (10%) | ~1,800 |
| E | 2007-2008 | ~2,000 | ~200 (10%) | ~1,800 |
| F | 2009-2010 | ~2,000 | ~200 (10%) | ~1,800 |
| G | 2011-2012 | ~2,000 | N/A** | ~2,000 |
| H | 2013-2014 | ~2,000 | N/A** | ~2,000 |
| I | 2015-2016 | ~2,000 | ~200 (10%) | ~1,800 |
| J | 2017-2018 | ~2,000 | ~200 (10%) | ~1,800 |
| L | 2021-2022 | ~2,000 | N/A** | ~2,000 |
| **TOTAL** | | **~16,000** | **~1,000** | **~15,000** |

*IDWA prevalence estimated at ~10-12% in reproductive-age women based on NHANES literature
**Ferritin not measured in cycles G, H, L

### Pooled Analysis Sample

| Category | Expected N (Unweighted) | Expected N (Weighted) |
|----------|------------------------|----------------------|
| IDWA cases with ferritin | ~1,000 | ~4.5 million* |
| Iron sufficient controls | ~9,000 | ~40.5 million* |
| **Total analytic sample** | **~10,000** | **~45 million* |

*Weighted to US population 2005-2022

## Missing Data Patterns and Expected Exclusions

### Laboratory Missing Data

| Variable | Expected Missing % | Primary Reason |
|----------|-------------------|----------------|
| Ferritin | 15-20% | Not measured in all cycles; subsampling |
| Hemoglobin | 2-3% | Refusal or technical issues |
| Iron/TIBC | 40-50% | Limited cycles; fasting requirements |
| Supplement data | 5-10% | Non-response or cycle differences |

### Exclusion Breakdown

| Exclusion Category | Expected N | % of Initial |
|-------------------|------------|--------------|
| Initial pool (all women 18-45) | ~16,000 | 100% |
| Missing ferritin | ~3,000 | 19% |
| Missing hemoglobin | ~300 | 2% |
| Missing weight | ~100 | 1% |
| Anemic | ~1,200 | 8% |
| **Final analytic sample** | **~11,400** | **71%** |

## Supplement User Classification

### Iron Supplement Identification

```python
# Algorithm for identifying iron supplement users
IF supplement_code in iron_supplement_list:
    IF days_per_month >= 20:           # Regular use
        THEN iron_user = 1
        iron_dose_daily = calculate_dose()
    ELSE:
        THEN iron_user = 0 (irregular)
ELSE:
    iron_user = 0
```

### Supplement Dose Categories

| Category | Daily Elemental Iron | Expected N in IDWA |
|----------|---------------------|-------------------|
| Non-user | 0 mg | ~600 (60%) |
| Low dose | <18 mg | ~200 (20%) |
| Moderate dose | 18-65 mg | ~150 (15%) |
| High dose | >65 mg | ~50 (5%) |

## Sensitivity Analysis Populations

### Alternative Iron Deficiency Definitions

| Analysis | Ferritin Threshold | Additional Criteria |
|----------|-------------------|---------------------|
| Primary | <15 ng/mL | None |
| Conservative | <12 ng/mL | None |
| Expanded | <20 ng/mL | None |
| With inflammation adjustment | <15 ng/mL | CRP ≤10 mg/L |
| With transferrin saturation | <15 ng/mL | OR TSAT <20% |

### Age Subgroup Analyses

| Subgroup | Age Range | Expected N (IDWA) |
|----------|-----------|-------------------|
| Young adults | 18-25 | ~400 |
| Early reproductive | 26-35 | ~400 |
| Late reproductive | 36-45 | ~400 |

### Cycle-Specific Analyses

| Analysis | Cycles | Ferritin Available | Expected N |
|----------|--------|-------------------|------------|
| Full pooled | D,E,F,I,J | Yes | ~1,000 |
| Ferritin-specific | D,E,F,I,J | Yes | ~1,000 |
| All cycles (CBC only) | All 8 | No | ~2,000* |

*Uses alternative iron deficiency markers where ferritin unavailable

## Data Quality Checks

### Pre-analysis Validation

1. **Duplicate SEQN check**: Verify unique identifiers
2. **Weight distribution**: Check for extreme weights (trim if >3 SD)
3. **Laboratory outliers**: Flag values outside physiological range
4. **Age consistency**: Cross-check reported vs. calculated age
5. **Pregnancy consistency**: Cross-check urine test vs. self-report

### Expected Value Ranges

| Variable | Minimum | Maximum | Action if Outside |
|----------|---------|---------|-------------------|
| Hemoglobin | 7.0 | 18.0 | Exclude (likely error) |
| Ferritin | 0.5 | 2,000 | Log transform; winsorize |
| Age | 18 | 45 | Exclude |
| BMI | 10 | 60 | Exclude (likely error) |

## References

1. World Health Organization. Nutritional Anaemias: Tools for Prevention and Control. WHO; 2017.
2. Mei Z, et al. Serum ferritin thresholds for iron deficiency anemia. Am J Clin Nutr 2022;116(2):399-407.
3. Cogswell ME, et al. Iron supplementation use among women in the United States. Am J Clin Nutr 2009;89(1):45-52.
4. Looker AC, et al. Prevalence of iron deficiency in the United States. JAMA 1997;277(12):973-6.
