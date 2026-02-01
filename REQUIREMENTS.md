# Data Requirements

## Primary Datasets

### 1. Ferritin (FERTIN)
- **Years Available**: D (2005-2006), E (2007-2008), F (2009-2010), I (2015-2016), J (2017-2018)
- **Key Variables**:
  - `LBXFER`: Ferritin (ng/mL)
  - `LBDFERSI`: Ferritin (µg/L)
- **Target Population**: Females 12-49 years (2005-2010), varies in later cycles

### 2. Iron, TIBC & Transferrin Saturation (FETIB)
- **Years Available**: D (2005-2006), J (2017-2018)
- **Key Variables**:
  - `LBXIRN`: Serum Iron (µg/dL)
  - `LBDIRNSI`: Serum Iron (µmol/L)
  - `LBXTIB`: TIBC (µg/dL)
  - `LBDTIBSI`: TIBC (µmol/L)
  - `LBDPCT`: Transferrin Saturation (%)
- **Target Population**: Females 12-59 years

### 3. Complete Blood Count (CBC)
- **Years Available**: D, E, F, G, H, I, J, L (2005-2022)
- **Key Variables**:
  - `LBXHGB`: Hemoglobin (g/dL) - for anemia definition
  - `LBXHCT`: Hematocrit (%)
  - `LBXMCVSI`: MCV (fL)
  - `LBXWBCSI`: White blood cell count
  - `LBXRBCSI`: Red blood cell count

### 4. Demographics (DEMO)
- **Years Available**: All cycles B-L (2001-2022)
- **Key Variables**:
  - `RIAGENDR`: Gender (1=Male, 2=Female)
  - `RIDAGEYR`: Age in years
  - `RIDRETH1/RIDRETH3`: Race/ethnicity
  - `DMDMARTL`: Marital status
  - `INDFMPIR`: Family income to poverty ratio
  - `SDMVSTRA`: Sampling strata
  - `SDMVPSU`: Primary sampling units
  - `WTMEC2YR/WTMECPRP`: MEC examination weights

### 5. Dietary Supplements (DSQTOT)
- **Years Available**: E, F, G, H, I, J, L (2007-2022)
- **Key Variables**:
  - `DSD010`: Any supplement use in past 30 days
  - `DSDCOUNT`: Number of supplements taken
  - `DSQTFIBE`: Total fiber from supplements (mg)
  - `DSQTCALC`: Total calcium from supplements (mg)
  - `DSQTFOLA`: Total folate from supplements (µg)
  - `DSQTIRON`: Total iron from supplements (mg) - CRITICAL
  - `DSQTVB12`: Total vitamin B12 from supplements (µg)
  - `DSQTVB6`: Total vitamin B6 from supplements (mg)
  - `DSQTVB1`: Total thiamin from supplements (mg)
  - `DSQTVB2`: Total riboflavin from supplements (mg)
  - `DSQTVITD`: Total vitamin D from supplements (µg)
  - `DSQTVITE`: Total vitamin E from supplements (mg)

### 6. Fasting Questionnaire (FASTQX)
- **Years Available**: D, E, F, G, H, I, J, L (2005-2022)
- **Key Variables**:
  - Pregnancy status variable (to be identified)
  - Fasting time variables

## Study Population Definition

### Inclusion Criteria:
1. Age: 18-45 years (using `RIDAGEYR`)
2. Sex: Female (using `RIAGENDR` = 2)
3. Not pregnant (to be identified from appropriate dataset)
4. Has valid ferritin measurement
5. Has valid hemoglobin measurement

### Exclusion Criteria:
1. Pregnant women
2. Missing ferritin or hemoglobin data
3. Age outside 18-45 range
4. Iron deficiency anemia (defined as both low ferritin AND anemia)

## Iron Deficiency Without Anemia (IDWA) Definition

### Criteria:
1. **Iron Deficiency**: Ferritin < 15 ng/mL (or < 15 µg/L)
   - Cutoff based on WHO/CDC guidelines for iron deficiency in non-pregnant women
2. **Without Anemia**: Hemoglobin ≥ 12.0 g/dL
   - Standard cutoff for non-pregnant women

### Additional Iron Status Classifications:
- **Normal Iron**: Ferritin ≥ 15 ng/mL and Hemoglobin ≥ 12 g/dL
- **Iron Deficiency Anemia**: Ferritin < 15 ng/mL AND Hemoglobin < 12 g/dL
- **Anemia without Iron Deficiency**: Ferritin ≥ 15 ng/mL AND Hemoglobin < 12 g/dL

## Supplement Use Definitions

### Iron Supplement User:
- `DSQTIRON` > 0 mg/day from supplements
- OR Individual supplement file indicates iron-containing supplement

### Non-User:
- `DSQTIRON` = 0 mg/day
- No iron-containing supplements reported

### Dosage Categories (to be created):
1. No iron supplement use (0 mg)
2. Low dose (>0 to <18 mg) - typical multivitamin
3. Moderate dose (18-65 mg) - standard iron supplement
4. High dose (>65 mg) - therapeutic dose

## Analytic Variables to Create

### Primary Outcomes:
1. Ferritin levels (continuous)
2. Iron deficiency without anemia (binary: yes/no)
3. Iron biomarker patterns (categorical)

### Secondary Outcomes:
1. Transferrin saturation levels
2. Serum iron levels
3. TIBC levels

### Primary Predictor:
- Iron supplement use (binary or categorical by dose)

### Covariates:
1. Age (continuous or categorical: 18-25, 26-35, 36-45)
2. Race/ethnicity (RIDRETH1: Mexican American, Other Hispanic, Non-Hispanic White, Non-Hispanic Black, Other)
3. BMI (from BMX dataset - to be added)
4. Family income to poverty ratio (INDFMPIR)
5. Menstrual status (if available)
6. Cycle/year (to account for temporal trends)

## Data Merging Strategy

1. Merge DEMO with CBC by SEQN (participant ID)
2. Merge with FERTIN by SEQN
3. Merge with FETIB by SEQN (where available)
4. Merge with DSQTOT by SEQN
5. Merge with FASTQX by SEQN
6. Apply inclusion/exclusion criteria
7. Create derived variables (IDWA status, supplement categories)

## Data Quality Considerations

1. Survey weights must be applied for population estimates
2. Complex survey design (strata and PSUs) must be accounted for in variance estimation
3. Multiple cycles will be combined; need to adjust weights accordingly
4. Missing data patterns to be examined
5. Detection limits for ferritin (values = 2 indicate below detection)

## Expected Sample Sizes

Based on NHANES sampling patterns:
- Total women 18-45: ~8,000-10,000 across all cycles
- After exclusions (pregnancy, missing data): ~6,000-8,000
- IDWA prevalence expected: 10-15% (~600-1,200)
- Supplement users within IDWA: Variable
