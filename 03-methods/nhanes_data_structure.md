# NHANES Data Structure Documentation

## Dataset Overview

This study utilizes six core NHANES datasets across 8 survey cycles (2005-2022). All datasets are linked via the unique identifier `SEQN` (Sample Sequence Number).

## Datasets Used

### 1. Ferritin (FERTIN)

**Description**: Serum ferritin measurements - primary outcome measure for iron stores

| Variable | Description | Key Values |
|----------|-------------|------------|
| `LBXFER` | Ferritin (ng/mL) | Continuous, 2=below detection |
| `LBDFER` | Ferritin result flag | 0=detectable, 1=below LLOD, 2=above ULOD |

**Cycles Available**: D (2005-2006), E (2007-2008), F (2009-2010), I (2015-2016), J (2017-2018)

**Special Notes**:
- Ferritin not measured in cycles G, H, L (use FETIB for iron/TIBC in these cycles)
- Below detection limit values coded as 2 in `LBDFER`
- Highly right-skewed distribution requiring log transformation

### 2. Iron and TIBC (FETIB)

**Description**: Serum iron, TIBC, and transferrin saturation measurements

| Variable | Description | Key Values |
|----------|-------------|------------|
| `LBXSIR` | Serum iron (μg/dL) | Continuous |
| `LBXSIT` | TIBC (μg/dL) | Continuous |
| `LBXSTR` | Transferrin saturation (%) | Continuous |
| `LBDSIR` | Iron result flag | 0=detectable, 1=below LLOD |

**Cycles Available**: D (2005-2006), J (2017-2018)

**Special Notes**:
- Iron/TIBC collected in limited cycles; most IDWA identification uses ferritin from FERTIN
- Transferrin saturation = (Iron/TIBC) × 100

### 3. Complete Blood Count (CBC)

**Description**: Hematology panel including hemoglobin and red cell indices

| Variable | Description | Key Values |
|----------|-------------|------------|
| `LBXHGB` | Hemoglobin (g/dL) | Continuous |
| `LBXHCT` | Hematocrit (%) | Continuous |
| `LBXMCV` | Mean corpuscular volume (fL) | Continuous |
| `LBXMCH` | Mean corpuscular hemoglobin (pg) | Continuous |
| `LBXRDW` | Red cell distribution width (%) | Continuous |
| `LBXRBCSI` | Red blood cell count (×10⁶/μL) | Continuous |

**Cycles Available**: D, E, F, G, H, I, J, L (all 8 study cycles)

**Special Notes**:
- Universal across all cycles - most reliable dataset for hemoglobin
- Hemoglobin <12 g/dL defines anemia in non-pregnant women
- MCV <80 fL suggests microcytic anemia (iron deficiency pattern)

### 4. Demographics (DEMO)

**Description**: Demographic characteristics and survey design variables

| Variable | Description | Key Values |
|----------|-------------|------------|
| `SEQN` | Sample sequence number | Unique identifier |
| `RIAGENDR` | Gender | 1=Male, 2=Female |
| `RIDAGEYR` | Age in years | 0-80+ (top-coded) |
| `RIDEXPRG` | Pregnancy status | 1=Yes, 2=No, 3=Unknown |
| `RIDRETH1` | Race/Hispanic origin | 1=Mexican American, 2=Other Hispanic, 3=Non-Hispanic White, 4=Non-Hispanic Black, 5=Other |
| `DMDEDUC2` | Education level | 1-5 categories |
| `DMDMARTL` | Marital status | 1-6 categories |
| `INDFMPIR` | Poverty income ratio | Continuous, 0-5+ |
| `SDMVSTRA` | Masked variance pseudo-stratum | 1-112 |
| `SDMVPSU` | Masked variance pseudo-PSU | 1-2 |
| `WTMEC2YR` | 2-year MEC exam weight | Sample weight |
| `SDDSRVYR` | Data release cycle number | 6-13 (corresponds to D-L) |

**Cycles Available**: B, C, D, E, F, G, H, I, J (DEMO available for all study cycles)

**Special Notes**:
- Survey design variables (`SDMVSTRA`, `SDMVPSU`, `WTMEC2YR`) required for all analyses
- `RIDEXPRG` critical for excluding pregnant women
- `SDDSRVYR` identifies cycle for weight adjustment

### 5. Dietary Supplement Total (DSQTOT)

**Description**: Dietary supplement use from household interview (30-day recall)

| Variable | Description | Key Values |
|----------|-------------|------------|
| `SEQN` | Sample sequence number | Unique identifier |
| `DSDSUPP` | Supplement ID code | NHANES-DSD product code |
| `DSDMTCH` | Matching code | Indicates specific product match |
| `DSDQTY` | Quantity consumed | Amount per day |
| `DSDUNIT` | Unit of measure | Unit for quantity |
| `DSDSRVY` | Days supplement taken | Frequency of use |

**Cycles Available**: E, F, G, H, I, J, L (2007-2022)

**Special Notes**:
- Iron supplements identified by `DSDSUPP` codes and product database
- Daily iron dose calculated from `DSDQTY` × iron content from DSBI database
- Supplements not measured in cycle D (2005-2006) - use DSQ1/DSQ2 instead

### 6. Body Measurements (BMX)

**Description**: Physical examination measurements

| Variable | Description | Key Values |
|----------|-------------|------------|
| `BMXWT` | Weight (kg) | Continuous |
| `BMXHT` | Standing height (cm) | Continuous |
| `BMXBMI` | Body mass index (kg/m²) | Continuous |
| `BMXWAIST` | Waist circumference (cm) | Continuous |

**Cycles Available**: B, C, D, E, F, G, H, I, J, L (all 8 study cycles)

**Special Notes**:
- BMI calculated from measured weight/height
- BMI categories: <18.5 underweight, 18.5-24.9 normal, 25-29.9 overweight, ≥30 obese

### 7. Fasting Questionnaire (FASTQX)

**Description**: Fasting status and blood draw timing

| Variable | Description | Key Values |
|----------|-------------|------------|
| `PHAFSTHR` | Fasting time (hours) | 0-24+ hours |
| `PHAFSTMN` | Fasting time (minutes) | 0-59 minutes |
| `PHDSESN` | Examination session | 1=Morning, 2=Afternoon, 3=Evening |

**Cycles Available**: D, E, F, G, H, I, J, L (all 8 study cycles)

**Special Notes**:
- Iron and ferritin measurements require fasting status for interpretation
- Morning draws preferred to minimize diurnal variation

## Merge Strategy

### Primary Key
All datasets are merged using `SEQN` (Sample Sequence Number), the unique participant identifier.

### Merge Logic

```python
# Pseudocode for data merge
base_data = DEMO_data  # Start with demographics (all participants)

# Left join laboratory data
merged = base_data.merge(FERTIN_data, on='SEQN', how='left')
merged = merged.merge(CBC_data, on='SEQN', how='left')

# Join supplement data (may be missing for non-users)
merged = merged.merge(DSQTOT_aggregated, on='SEQN', how='left')

# Join body measurements
merged = merged.merge(BMX_data, on='SEQN', how='left')

# Join fasting information
merged = merged.merge(FASTQX_data, on='SEQN', how='left')
```

### Handling Missing Data Across Cycles

| Dataset | Cycle D | Cycle E | Cycle F | Cycle G | Cycle H | Cycle I | Cycle J | Cycle L |
|---------|---------|---------|---------|---------|---------|---------|---------|---------|
| FERTIN | ✓ | ✓ | ✓ | ✗ | ✗ | ✓ | ✓ | ✗ |
| FETIB | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ |
| CBC | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| DEMO | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| DSQTOT | ✗* | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| BMX | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| FASTQX | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

*Cycle D uses DSQ1/DSQ2 for supplement data

### Cycle-Specific Ferritin Availability

Since ferritin was not measured in cycles G, H, and L, IDWA identification for these cycles relies on:
1. Historical ferritin from FERTIN in other cycles for reference
2. Alternative iron markers where available
3. Analyses may be stratified by ferritin availability

## Weight Adjustments for Combined Cycles

### Weight Calculation Formula

For analyses combining N cycles (N=8 for this study):

```python
# Adjust weights for pooled cycles
adjusted_weight = WTMEC2YR / 8
```

### Rationale
- Dividing by the number of cycles creates a representative average across the time period
- Maintains proper population representativeness
- Standard NHANES recommended approach for multi-cycle analyses

### Survey Design Specification

```python
# Python/statsmodels syntax
from statsmodels.stats.weightstats import DescrStatsW
from statsmodels.regression.linear_model import WLS

# Survey design variables
strata = 'SDMVSTRA'
psu = 'SDMVPSU'
weight = 'WTMEC2YR_adj'  # Adjusted weight
```

## Missing Data Patterns

### Expected Missing Data Sources

1. **Laboratory Non-response**: Not all MEC participants provide blood samples
2. **Insufficient Sample**: Volume inadequate for all requested assays
3. **Assay Not Performed**: Certain tests not run in specific subsamples
4. **Item Non-response**: Missing questionnaire responses

### Missing Data Handling

| Variable Type | Missing Strategy |
|---------------|------------------|
| Ferritin | Complete case analysis; sensitivity analysis with imputation |
| Hemoglobin | Complete case analysis |
| Supplement use | Assume non-user if missing (conservative) |
| Demographics | Complete case analysis |
| BMI | Complete case analysis |

## Dataset File Naming Convention

Data files follow the pattern: `PREFIX_YEARCODE.csv`

| Year | Code | Example |
|------|------|---------|
| 2005-2006 | D | `FERTIN_D.csv` |
| 2007-2008 | E | `FERTIN_E.csv` |
| 2009-2010 | F | `FERTIN_F.csv` |
| 2011-2012 | G | `CBC_G.csv` |
| 2013-2014 | H | `CBC_H.csv` |
| 2015-2016 | I | `FERTIN_I.csv` |
| 2017-2018 | J | `FERTIN_J.csv` |
| 2021-2022 | L | `CBC_L.csv` |

## Quality Control Notes

1. **Laboratory QC**: NHANES includes blind duplicates and proficiency testing
2. **Data Edits**: NCHS applies consistency edits before public release
3. **Supplement Database**: DSBI provides detailed product information for DSQTOT codes
4. **Pregnancy Exclusion**: Use both `RIDEXPRG` and self-reported pregnancy where available

## Data Access

All datasets accessed from:
- Data: `Processed Data/Data/`
- Documentation: `Processed Data/Doc/`
- Dictionaries: `<PREFIX>_<YEAR>_dictionary.csv`
- Metadata: `<PREFIX>_<YEAR>_metadata.md`
