# Methods Documentation Summary

## Iron Deficiency Without Anemia in US Women Study
**Study Directory**: `studies/iron-deficiency-women-2026-01-31/03-methods/`

---

## Documentation Files

### 1. `study_design.md`
**Content**: Comprehensive NHANES survey design documentation

**Key Sections**:
- NHANES complex survey design overview
- Strata, PSUs, and weight methodology
- Laboratory measurement procedures (ferritin, iron, hemoglobin, CBC)
- Data collection timeline (2005-2022)
- Ethical considerations (NCHS IRB approval)
- Study advantages and limitations

**Use Case**: Background for manuscript methods section and understanding survey structure

---

### 2. `nhanes_data_structure.md`
**Content**: Dataset structure and merge documentation

**Key Sections**:
- Dataset summaries (FERTIN, FETIB, CBC, DEMO, DSQTOT, BMX, FASTQX)
- Variable descriptions and key values
- Cycle availability matrix
- Merge strategy using SEQN
- Missing data patterns by cycle
- Weight adjustment formula for pooled cycles

**Use Case**: Reference for data loading and variable identification

---

### 3. `population_criteria.md`
**Content**: Study population definition algorithms

**Key Sections**:
- Step-by-step inclusion criteria algorithm
- Pregnancy exclusion algorithm
- IDWA status definition (ferritin <15, Hb ≥12)
- Exclusion criteria matrix
- Flow diagram text description
- Expected sample size calculations by cycle
- Sensitivity analysis population definitions

**Use Case**: Reproducing study population selection; understanding inclusion/exclusion logic

---

### 4. `statistical_methods.md`
**Content**: Comprehensive statistical methodology

**Key Sections**:
- Survey weighting (WTMEC2YR adjustment)
- Variance estimation (Taylor series linearization)
- Primary analysis: survey-weighted linear regression
- Log transformation rationale for ferritin
- Geometric mean ratios vs. arithmetic means
- Multiple comparison corrections (Bonferroni, FDR)
- Sensitivity analyses plan (6 scenarios)
- Below-detection-limit handling
- Regression diagnostics

**Use Case**: Statistical analysis plan; software implementation guidance

---

### 5. `variable_derivations.py`
**Content**: Complete Python derivation script

**Key Functions**:
- `load_nhanes_dataset()`: Load individual cycle data
- `load_all_study_datasets()`: Load all required datasets
- `derive_idwa_status()`: Primary IDWA classification
- `derive_iron_status_categories()`: 4-category iron status
- `identify_iron_supplements()`: Supplement identification
- `calculate_iron_dose()`: Daily iron dose calculation
- `derive_supplement_categories()`: Dose categorization
- `derive_anemia_status()`: Anemia classification
- `recode_demographics()`: Demographic variable recoding
- `adjust_survey_weights()`: Weight adjustment for pooled cycles
- `derive_all_study_variables()`: Complete derivation pipeline

**Use Case**: Execute data processing pipeline; modify for sensitivity analyses

---

## Quick Reference

### NHANES Variable Names Used

| Concept | NHANES Variable | Location |
|---------|----------------|----------|
| Ferritin | `LBXFER` | FERTIN |
| Hemoglobin | `LBXHGB` | CBC |
| Serum Iron | `LBXSIR` | FETIB |
| TIBC | `LBXSIT` | FETIB |
| Transferrin Sat | `LBXSTR` | FETIB |
| MCV | `LBXMCV` | CBC |
| Gender | `RIAGENDR` | DEMO |
| Age | `RIDAGEYR` | DEMO |
| Pregnancy | `RIDEXPRG` | DEMO |
| Race/Ethnicity | `RIDRETH1` | DEMO |
| Survey Weight | `WTMEC2YR` | DEMO |
| Strata | `SDMVSTRA` | DEMO |
| PSU | `SDMVPSU` | DEMO |
| BMI | `BMXBMI` | BMX |
| Supplement Use | `DSDSUPP` | DSQTOT |

### Study Thresholds

| Parameter | Threshold | Source |
|-----------|-----------|--------|
| Iron deficiency | Ferritin <15 ng/mL | WHO/CDC |
| Anemia (non-pregnant) | Hb <12.0 g/dL | WHO |
| Anemia (pregnant) | Hb <11.0 g/dL | WHO |
| Age range | 18-45 years | Study definition |
| Low supplement dose | <18 mg/day | Study definition |
| Moderate dose | 18-65 mg/day | Study definition |
| High dose | >65 mg/day | Study definition |

### Cycle Mapping

| Letter | Years | Ferritin Available? | Key Notes |
|--------|-------|---------------------|-----------|
| D | 2005-2006 | Yes | DSQ1/DSQ2 for supplements |
| E | 2007-2008 | Yes | First DSQTOT cycle |
| F | 2009-2010 | Yes | Standard protocols |
| G | 2011-2012 | No | CBC only for this study |
| H | 2013-2014 | No | CBC only for this study |
| I | 2015-2016 | Yes | Standard protocols |
| J | 2017-2018 | Yes | Standard protocols |
| L | 2021-2022 | No | COVID-19 modifications |

---

## Usage Instructions

### To Run the Derivation Pipeline

```bash
# Navigate to methods directory
cd studies/iron-deficiency-women-2026-01-31/03-methods/

# Execute derivation script
python3 variable_derivations.py
```

### To Modify Study Parameters

Edit `variable_derivations.py`:
- Change `STUDY_CYCLES` list to include/exclude cycles
- Modify thresholds in derivation functions
- Add new exclusion criteria

### To Access Raw Data

All raw data accessed via:
- `Processed Data/Data/<PREFIX>_<CYCLE>.csv`
- `Processed Data/Doc/<PREFIX>_<CYCLE>_metadata.md`
- `Processed Data/Doc/<PREFIX>_<CYCLE>_dictionary.csv`

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2026-01-31 | 1.0 | Initial methods documentation |

## Contact

**Study Author**: Elwood Research (elwoodresearch@gmail.com)
**Repository**: NHANES Automated Research System
