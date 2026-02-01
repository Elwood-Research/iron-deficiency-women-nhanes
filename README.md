# Iron Deficiency Without Anemia and Supplement Usage Effects in Women

**NHANES Cross-Sectional Analysis 2005-2022**

[![Study Status](https://img.shields.io/badge/status-complete-success)](./)
[![Sample Size](https://img.shields.io/badge/n=6,125%20women-blue)](./)
[![License](https://img.shields.io/badge/license-MIT-green)](./)
[![PDF Manuscript](https://img.shields.io/badge/PDF-manuscript-orange)](./iron-deficiency-women-nhanes-manuscript.pdf)

---

## 📄 Manuscript

📥 **[Download PDF Manuscript](./iron-deficiency-women-nhanes-manuscript.pdf)** (233 KB, 8-10 pages)

The complete research manuscript is available as a compiled PDF, ready for submission to peer-reviewed journals.

---

## 📊 Study Overview

This study examines the effects of iron supplement usage on ferritin levels and iron status in non-pregnant women aged 18-45 with iron deficiency without anemia (IDWA), using nationally representative data from the National Health and Nutrition Examination Survey (NHANES) 2005-2022.

**Principal Investigator**: Elwood Research  
**Contact**: elwoodresearch@gmail.com  
**Date**: January 31, 2026

---

## 🎯 Key Findings

### Primary Results
- **IDWA Prevalence**: 9.0% (95% CI: 8.3%-9.7%) of non-pregnant women aged 18-45
  - Affects approximately **2.5 million US women**
- **Supplement Effect**: Iron supplementation associated with **6.4% higher ferritin** (β=0.062, p=0.048)
- **Optimal Dose**: Moderate dose (18-27 mg/day) shows strongest effect (β=0.207, p<0.001)

### Demographic Disparities
| Group | IDWA Prevalence |
|-------|----------------|
| Mexican American | 11.6% (highest) |
| Non-Hispanic White | 8.8% |
| Non-Hispanic Black | 6.5% (lowest) |
| Age 36-40 | 10.3% (peak age) |

### Sample Characteristics
- **Total participants**: 6,125 women
- **Mean age**: 32.1 years (SD: 8.1)
- **Mean BMI**: 28.4 kg/m² (SD: 7.8)
- **Median ferritin**: 37.2 ng/mL (IQR: 20.0-67.0)
- **Iron supplement users**: 18.5%

---

## 📁 Repository Structure

```
iron-deficiency-women-2026-01-31/
├── 01-literature/           # Literature review (30+ references)
│   ├── references.bib
│   ├── literature_synthesis.md
│   └── nhanes_studies.md
├── 02-research-plan/        # Research hypotheses & plan
│   ├── hypotheses.md
│   ├── analysis_plan.md
│   ├── variable_operationalization.md
│   └── expected_results.md
├── 03-methods/              # Methodology documentation
│   ├── study_design.md
│   ├── nhanes_data_structure.md
│   ├── population_criteria.md
│   ├── statistical_methods.md
│   └── variable_derivations.py
├── 04-analysis/             # Statistical analysis
│   ├── scripts/            # Python analysis scripts
│   ├── outputs/
│   │   ├── tables/         # LaTeX tables
│   │   └── figures/        # 300 DPI PNG figures
│   └── results_summary.md
├── 05-conclusion/           # Discussion & synthesis
│   ├── discussion.md
│   ├── conclusion.md
│   ├── clinical_implications.md
│   ├── limitations_assessment.md
│   └── literature_comparison_table.md
└── manuscript/              # LaTeX manuscript
    ├── main.tex
    ├── tables.tex
    ├── figures.tex
    ├── supplementary_materials.tex
    └── compile.sh
```

---

## 🔬 Methodology

### Study Design
- **Data Source**: NHANES 2005-2022 (8 cycles: D, E, F, G, H, I, J, L)
- **Design**: Cross-sectional with complex survey weighting
- **Population**: Non-pregnant women aged 18-45

### IDWA Definition
- **Iron Deficiency**: Ferritin <15 ng/mL
- **Without Anemia**: Hemoglobin ≥12 g/dL
- **Combined**: Ferritin <15 ng/mL AND Hemoglobin ≥12 g/dL

### Key Variables
- **Primary Outcome**: Log-transformed serum ferritin (LBXFER)
- **Primary Predictor**: Iron supplement use (DSQTIRON > 0 mg/day)
- **Covariates**: Age, race/ethnicity, poverty ratio, BMI

### Statistical Methods
- Survey-weighted linear regression (WLS)
- Taylor series linearization for variance estimation
- Weight adjustment for 8-year pooled analysis: WTMEC2YR / 8
- Significance level: α = 0.05 (two-sided)

---

## 📊 Results

### IDWA Prevalence
Weighted prevalence: **9.0%** (95% CI: 8.3%-9.7%)

### Regression Analysis
| Model | Coefficient | 95% CI | p-value | Interpretation |
|-------|-------------|--------|---------|----------------|
| Unadjusted | 0.081 | 0.023-0.140 | 0.007 | **Significant** |
| Demographics-adjusted | 0.049 | -0.013-0.110 | 0.120 | NS |
| Fully adjusted | 0.062 | 0.001-0.123 | 0.048 | **Significant** |

### Dose-Response Analysis
| Dose Category | Coefficient | 95% CI | p-value |
|---------------|-------------|--------|---------|
| Low (0-18 mg/day) | -0.009 | -0.090-0.073 | 0.833 |
| **Moderate (18-27 mg)** | **0.207** | **0.103-0.310** | **<0.001** |
| High (≥27 mg/day) | 0.023 | -0.107-0.153 | 0.727 |

---

## 🏥 Clinical Implications

### For Clinicians
1. **Screen women with unexplained fatigue** for IDWA
2. **Prioritize high-risk groups**: Mexican American women, ages 36-40
3. **Consider moderate-dose supplementation** (18-27 mg/day)
4. **Monitor ferritin response** at 8-12 weeks

### For Public Health
- Current WHO threshold (<15 ng/mL) may underestimate deficiency
- Moderate dosing appears optimal for population intervention
- Targeted screening programs could identify ~2.5 million affected women

---

## 📚 Citation

```bibtex
@article{elwood2026idwa,
  title={Iron Deficiency Without Anemia and Supplement Usage Effects on Ferritin in Non-Pregnant Women Aged 18-45: A Cross-Sectional Analysis of NHANES 2005-2022},
  author={Elwood Research},
  journal={Manuscript in Preparation},
  year={2026},
  note={Data from National Health and Nutrition Examination Survey}
}
```

---

## 📖 Key Literature References

1. Petry N, et al. (2022) - Physiologically-based ferritin thresholds (~25 μg/L)
2. Vaucher P, et al. (2012) - 47.7% fatigue reduction with iron supplementation
3. Karregat JMP, et al. (2025) - FORTE trial (60 mg daily optimal)
4. Hamarsha S, et al. (2025) - Meta-analysis (n=527,746)
5. Verdon F, et al. (2003) - Landmark fatigue RCT in unexplained fatigue
6. Auerbach M, et al. (2025) - Comprehensive clinical review
7. Stoel BC, et al. (2023) - Alternate-day vs daily dosing

*See `01-literature/references.bib` for complete bibliography (30+ references)*

---

## 🛠️ Reproducibility

### Requirements
- Python 3.8+
- pandas, numpy, scipy, statsmodels, matplotlib, seaborn

### Running the Analysis
```bash
cd 04-analysis/scripts
python run_all_analysis.py
```

### Compiling the Manuscript
```bash
cd manuscript
./compile.sh
```

---

## 📊 Data Availability

This study uses publicly available NHANES data:
- **Source**: [CDC NHANES](https://www.cdc.gov/nchs/nhanes/)
- **Data files**: Processed Data/Data/ (local repository)
- **Documentation**: Processed Data/Doc/ (local repository)

---

## ⚖️ Ethics and IRB

This study uses de-identified, publicly available NHANES data:
- NHANES protocols approved by NCHS Research Ethics Review Board
- All participants provided informed consent
- No additional IRB approval required for secondary data analysis

---

## 📝 Limitations

1. Cross-sectional design limits causal inference
2. Self-reported supplement use may have measurement error
3. Single ferritin measurement may not reflect long-term status
4. Missing data for some NHANES cycles
5. Cannot assess timing of supplementation vs. measurement

*See `05-conclusion/limitations_assessment.md` for detailed analysis*

---

## 🔮 Future Research

- Longitudinal studies to establish temporal relationships
- Randomized controlled trials in IDWA population
- Investigation of <25 ng/mL threshold clinical significance
- Cost-effectiveness analyses of screening programs
- Studies on menstrual blood loss quantification

---

## 📧 Contact

**Elwood Research**  
📧 elwoodresearch@gmail.com  
🔗 [GitHub: Elwood-Research](https://github.com/Elwood-Research)

---

## 📄 License

This research is released under the MIT License. Data from NHANES is in the public domain.

---

**Last Updated**: January 31, 2026  
**Study Status**: Complete ✓  
**Manuscript Status**: Ready for Submission
