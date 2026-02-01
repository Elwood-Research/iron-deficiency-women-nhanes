# Study Design: Iron Deficiency Without Anemia in US Women

## Overview

This cross-sectional study utilizes the National Health and Nutrition Examination Survey (NHANES) to investigate the relationship between iron supplement usage and iron biomarkers in women with iron deficiency without anemia (IDWA). The study spans NHANES cycles 2005-2022, encompassing 8 survey cycles (D, E, F, G, H, I, J, L).

## NHANES Survey Overview

### Program Description
The National Health and Nutrition Examination Survey (NHANES) is a program of studies designed to assess the health and nutritional status of adults and children in the United States. NHANES is conducted by the National Center for Health Statistics (NCHS), part of the Centers for Disease Control and Prevention (CDC).

### Complex Survey Design

NHANES employs a complex, multistage probability sampling design that includes:

1. **Geographic Stratification**: The United States is divided into geographic primary sampling units (PSUs)
2. **Clustered Sampling**: Households are selected within PSUs using systematic sampling
3. **Oversampling**: Specific subgroups (e.g., pregnant women, racial/ethnic minorities) are oversampled to improve statistical reliability
4. **Multi-stage Selection**: Counties → Segments → Households → Individuals

### Sampling Methodology

#### Strata and PSUs
- **Strata (SDMVSTRA)**: Geographic and demographic stratification variables (1-112 across cycles)
- **PSUs (SDMVPSU)**: Primary Sampling Units representing clusters of households (1-2 per stratum)
- **Masking**: For confidentiality, PSUs are masked and cannot be linked to geographic locations

#### Sample Weights
NHANES provides multiple weight variables for different analysis purposes:

| Weight Variable | Purpose | Recommended Use |
|----------------|---------|-----------------|
| `WTMEC2YR` | 2-year MEC exam weights | Analyses using MEC exam data |
| `WTINT2YR` | 2-year interview weights | Analyses using interview-only data |
| `WTSAF2YR` | 2-year fasting subsample | Analyses requiring fasting samples |

**Key Principle**: For combined cycles, divide `WTMEC2YR` by the number of cycles (8 for this study).

### Laboratory Measurement Procedures

#### Ferritin (LBXFER)
- **Method**: Immunometric assay (automated chemistry analyzer)
- **Specimen**: Serum
- **Detection Limit**: Varies by cycle (typically 0.5-1.0 ng/mL)
- **Below Detection**: Coded as 2 in result flag variables
- **Clinical Significance**: Primary indicator of iron stores; <15 ng/mL indicates depleted stores

#### Serum Iron (LBXSIR)
- **Method**: Colorimetric assay (ferrozine method)
- **Specimen**: Serum
- **Units**: μg/dL
- **Diurnal Variation**: Measured in morning samples to minimize variability
- **Clinical Significance**: Circulating iron; affected by recent intake and inflammation

#### Total Iron Binding Capacity (TIBC) (LBXSIT)
- **Method**: Colorimetric calculation
- **Specimen**: Serum
- **Units**: μg/dL
- **Clinical Significance**: Measure of transferrin capacity to bind iron

#### Transferrin Saturation
- **Calculation**: (Serum Iron / TIBC) × 100
- **Clinical Significance**: Percentage of transferrin saturated with iron; <20% suggests iron deficiency

#### Hemoglobin (LBXHGB)
- **Method**: Automated hematology analyzer
- **Specimen**: Whole blood (EDTA)
- **Units**: g/dL
- **Anemia Thresholds**:
  - Non-pregnant women: <12.0 g/dL (WHO criteria)
  - Pregnant women: <11.0 g/dL

#### Complete Blood Count (CBC)
- **Parameters**: Hemoglobin, hematocrit, MCV, MCH, RBC count, RDW
- **Method**: Automated cell counting with impedance and optical methods
- **Clinical Utility**: Characterizes anemia type (microcytic, normocytic, macrocytic)

### Data Collection Timeline

| Cycle | Years | Sample Size (Total) | Key Relevant Changes |
|-------|-------|---------------------|---------------------|
| D | 2005-2006 | ~10,000 | Standard ferritin assay |
| E | 2007-2008 | ~10,000 | Standard ferritin assay |
| F | 2009-2010 | ~10,000 | Standard ferritin assay |
| G | 2011-2012 | ~10,000 | Standard ferritin assay |
| H | 2013-2014 | ~10,000 | Standard ferritin assay |
| I | 2015-2016 | ~10,000 | Standard ferritin assay |
| J | 2017-2018 | ~10,000 | Standard ferritin assay |
| L | 2021-2022 | ~10,000 | COVID-19 protocol modifications |

**Note**: Cycle K (2019-2020) was not included due to incomplete data collection during the COVID-19 pandemic.

### Data Collection Components

1. **Household Interview**: Demographics, health history, supplement use (DSQTOT)
2. **Mobile Examination Center (MEC)**: Physical measurements, laboratory tests, specialized exams
3. **Fasting Subsample**: Morning blood draws for glucose, lipid, and iron studies

## Ethical Considerations

### IRB Approval
- **Approving Body**: NCHS Research Ethics Review Board (ERB)
- **Protocol**: All NHANES protocols receive annual review and approval
- **Informed Consent**: Written informed consent obtained from all participants ≥18 years; parental consent and child assent for minors

### Data Protection
- **Confidentiality**: All publicly released data undergo statistical disclosure control
- **Suppression**: Small geographic areas and rare characteristics are suppressed
- **Masked IDs**: SEQN (Sample Sequence Number) cannot be linked back to individuals

### Public Use Data
- This study uses publicly available de-identified NHANES data
- No direct contact with participants
- Analysis conducted in accordance with NCHS data use guidelines

## Advantages of NHANES for This Study

### Strengths

1. **Nationally Representative**: Results generalizable to US non-institutionalized population
2. **Standardized Protocols**: Consistent laboratory methods across cycles ensure comparability
3. **Comprehensive Data**: Simultaneous measurement of iron status, supplement use, and confounders
4. **Large Sample Size**: Sufficient power to detect associations in subgroups (8 cycles × ~10,000 = ~80,000 total)
5. **Quality Assurance**: Rigorous QC/QA protocols including blind duplicates and proficiency testing
6. **Longitudinal Trends**: Ability to examine temporal patterns across 17 years
7. **Oversampling**: Enhanced precision for minority populations and pregnant women (though excluded here)

### Limitations

1. **Cross-sectional Design**: Cannot establish temporal causality or treatment effects
2. **Self-reported Supplement Use**: Potential for recall bias and misclassification
3. **Single Time Point**: Iron status and supplement use measured at one time; no information on duration
4. **Survival Bias**: Severely ill individuals may not participate
5. **Missing Data**: Item non-response and missing laboratory measurements
6. **Changing Assays**: Subtle changes in laboratory methods across cycles may introduce drift
7. **Pandemic Disruption**: Cycle L (2021-2022) had modified protocols due to COVID-19

## Statistical Implications of Design

### Required Adjustments
1. **Survey Weights**: Must use `WTMEC2YR` adjusted for pooled cycles
2. **Variance Estimation**: Must account for stratification and clustering using Taylor series linearization
3. **Subpopulation Analysis**: Analyses restricted to subgroups must use full-sample weights with domain indicators
4. **Finite Population Correction**: Not required for variance estimation in NHANES

### Software Requirements
- **Survey Analysis**: `statsmodels` with `survey` design specification
- **Variance Estimation**: Supports Taylor series linearization
- **Weight Application**: `WTMEC2YR / 8` for combined cycles

## References

1. National Center for Health Statistics. NHANES 2005-2006 Documentation. Available at: https://wwwn.cdc.gov/nchs/nhanes/
2. Johnson CL, et al. National Health and Nutrition Examination Survey: analytic guidelines, 1999-2010. Vital Health Stat 2013;2(161).
3. Cogswell ME, et al. Assessment of iron deficiency in US childbearing-age women. Am J Clin Nutr 2009;89(4):1334-42.
4. World Health Organization. Hemoglobin concentrations for the diagnosis of anemia. WHO; 2011.
