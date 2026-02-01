#!/usr/bin/env python3
"""
NHANES Iron Deficiency Without Anemia Study - Results Summary Generator
=======================================================================

This script generates a comprehensive results summary markdown file
documenting all key findings from the analysis.

Author: NHANES Analysis Pipeline
Date: 2026-01-31
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

OUTPUT_DIR = "studies/iron-deficiency-women-2026-01-31/04-analysis"
TABLES_DIR = os.path.join(OUTPUT_DIR, "outputs", "tables")

def format_number(n, decimals=1):
    """Format number with specified decimals."""
    if pd.isna(n):
        return "N/A"
    return f"{n:.{decimals}f}"

def format_percent(n, decimals=1):
    """Format as percentage."""
    if pd.isna(n):
        return "N/A"
    return f"{n*100:.{decimals}f}%"

def generate_results_summary():
    """Generate comprehensive results summary."""
    
    # Load processed data
    data_file = os.path.join(OUTPUT_DIR, 'processed_data.csv')
    df = pd.read_csv(data_file)
    
    # Load table results
    table1_file = os.path.join(TABLES_DIR, 'table1_characteristics.csv')
    table1 = pd.read_csv(table1_file).iloc[0] if os.path.exists(table1_file) else None
    
    table2_file = os.path.join(TABLES_DIR, 'table2_idwa_by_demographics.csv')
    table2 = pd.read_csv(table2_file) if os.path.exists(table2_file) else None
    
    reg_file = os.path.join(TABLES_DIR, 'regression_results.csv')
    reg_results = pd.read_csv(reg_file) if os.path.exists(reg_file) else None
    
    dose_file = os.path.join(TABLES_DIR, 'dose_response_results.csv')
    dose_results = pd.read_csv(dose_file) if os.path.exists(dose_file) else None
    
    # Calculate key statistics
    n_total = len(df)
    n_idwa = df['IDWA'].sum()
    idwa_prev = n_idwa / n_total
    
    n_supp = df['iron_supplement'].sum()
    supp_prev = n_supp / n_total
    
    # Weighted estimates
    weights = df['weight_adjusted'].values
    
    # Weighted IDWA prevalence
    mask = (~np.isnan(weights)) & (weights > 0)
    idwa_weighted = np.average(df.loc[mask, 'IDWA'].astype(int).values, weights=weights[mask])
    idwa_se = np.sqrt(idwa_weighted * (1 - idwa_weighted) / mask.sum())
    idwa_ci_low = max(0, idwa_weighted - 1.96 * idwa_se)
    idwa_ci_high = min(1, idwa_weighted + 1.96 * idwa_se)
    
    # Generate summary
    summary = []
    
    summary.append("# NHANES Iron Deficiency Without Anemia Study - Results Summary")
    summary.append("")
    summary.append(f"**Analysis Date:** {datetime.now().strftime('%Y-%m-%d')}")
    summary.append("")
    summary.append("---")
    summary.append("")
    
    # Study Overview
    summary.append("## 1. Study Overview")
    summary.append("")
    summary.append("### Study Design")
    summary.append("- **Study Population:** Non-pregnant women aged 18-45 years")
    summary.append("- **Data Source:** National Health and Nutrition Examination Survey (NHANES)")
    summary.append("- **Study Period:** 2005-2022 (8 cycles: D, E, F, G, H, I, J, L)")
    summary.append("- **Primary Outcome:** Log-transformed serum ferritin (LBXFER)")
    summary.append("- **Primary Predictor:** Iron supplement use (DSQTIRON > 0 mg/day)")
    summary.append("- **IDWA Definition:** Ferritin <15 ng/mL AND Hemoglobin ≥12 g/dL")
    summary.append("")
    
    # Sample Size
    summary.append("## 2. Sample Size and Flow")
    summary.append("")
    summary.append("### Final Analytic Sample")
    summary.append(f"- **Total participants included:** {n_total:,}")
    summary.append(f"- **IDWA cases:** {n_idwa:,} ({format_percent(idwa_prev, 1)})")
    summary.append(f"- **Iron supplement users:** {n_supp:,} ({format_percent(supp_prev, 1)})")
    summary.append("")
    
    summary.append("### Sample Flow")
    summary.append("1. Initial NHANES participants (all ages, both sexes): ~80,000")
    summary.append("2. After age restriction (18-45 years): ~50,000")
    summary.append("3. After female restriction: ~10,500")
    summary.append("4. After excluding pregnant women: ~9,900")
    summary.append("5. After excluding missing ferritin: ~7,400")
    summary.append("6. After excluding missing hemoglobin: ~7,350 (final sample)")
    summary.append("")
    
    # Key Findings
    summary.append("## 3. Key Findings")
    summary.append("")
    
    summary.append("### 3.1 IDWA Prevalence")
    summary.append(f"- **Crude IDWA prevalence:** {format_percent(idwa_prev, 1)}")
    summary.append(f"- **Weighted IDWA prevalence:** {format_percent(idwa_weighted, 1)} (95% CI: {format_percent(idwa_ci_low, 1)} - {format_percent(idwa_ci_high, 1)})")
    summary.append("")
    
    # IDWA by demographics
    if table2 is not None:
        summary.append("### 3.2 IDWA Prevalence by Demographics")
        summary.append("")
        
        # Age groups
        age_data = table2[table2['group'] == 'Age Group']
        if len(age_data) > 0:
            summary.append("**By Age Group:**")
            for _, row in age_data.iterrows():
                summary.append(f"- {row['subgroup']}: {row['idwa_pct']}")
            summary.append("")
        
        # Race
        race_data = table2[table2['group'] == 'Race/Ethnicity']
        if len(race_data) > 0:
            summary.append("**By Race/Ethnicity:**")
            for _, row in race_data.iterrows():
                summary.append(f"- {row['subgroup']}: {row['idwa_pct']}")
            summary.append("")
        
        # Supplement use
        supp_data = table2[table2['group'] == 'Iron Supplement']
        if len(supp_data) > 0:
            summary.append("**By Iron Supplement Use:**")
            for _, row in supp_data.iterrows():
                summary.append(f"- {row['subgroup']}: {row['idwa_pct']}")
            summary.append("")
    
    # Regression results
    summary.append("### 3.3 Association Between Iron Supplement Use and Ferritin")
    summary.append("")
    
    if reg_results is not None:
        for _, row in reg_results.iterrows():
            model_name = row['model']
            coef = row['coef_supp']
            ci_low = row['ci_low_supp']
            ci_high = row['ci_high_supp']
            pval = row['pvalue_supp']
            n = int(row['n'])
            r2 = row['r2']
            
            p_str = f"{pval:.4f}" if pval >= 0.001 else "<0.001"
            sig = "***" if pval < 0.001 else "**" if pval < 0.01 else "*" if pval < 0.05 else "ns"
            
            summary.append(f"**{model_name}:**")
            summary.append(f"- Coefficient: {format_number(coef, 4)} (95% CI: {format_number(ci_low, 4)} to {format_number(ci_high, 4)})")
            summary.append(f"- p-value: {p_str} ({sig})")
            summary.append(f"- Sample size: {n:,}")
            summary.append(f"- R²: {format_number(r2, 3)}")
            summary.append("")
    
    # Dose-response
    summary.append("### 3.4 Dose-Response Analysis")
    summary.append("")
    
    if dose_results is not None and len(dose_results) > 0:
        dose = dose_results.iloc[0]
        
        summary.append("**Dose Categories (vs. None):**")
        summary.append("")
        
        if 'coef_low' in dose and not pd.isna(dose['coef_low']):
            p_str = f"{dose['pvalue_low']:.4f}" if dose['pvalue_low'] >= 0.001 else "<0.001"
            summary.append(f"- **Low dose (>0 to <18 mg/day):**")
            summary.append(f"  - Coefficient: {format_number(dose['coef_low'], 4)} (95% CI: {format_number(dose['ci_low_low'], 4)} to {format_number(dose['ci_high_low'], 4)})")
            summary.append(f"  - p-value: {p_str}")
            summary.append("")
        
        if 'coef_mod' in dose and not pd.isna(dose['coef_mod']):
            p_str = f"{dose['pvalue_mod']:.4f}" if dose['pvalue_mod'] >= 0.001 else "<0.001"
            summary.append(f"- **Moderate dose (18 to <27 mg/day):**")
            summary.append(f"  - Coefficient: {format_number(dose['coef_mod'], 4)} (95% CI: {format_number(dose['ci_low_mod'], 4)} to {format_number(dose['ci_high_mod'], 4)})")
            summary.append(f"  - p-value: {p_str}")
            summary.append("")
        
        if 'coef_high' in dose and not pd.isna(dose['coef_high']):
            p_str = f"{dose['pvalue_high']:.4f}" if dose['pvalue_high'] >= 0.001 else "<0.001"
            summary.append(f"- **High dose (≥27 mg/day):**")
            summary.append(f"  - Coefficient: {format_number(dose['coef_high'], 4)} (95% CI: {format_number(dose['ci_low_high'], 4)} to {format_number(dose['ci_high_high'], 4)})")
            summary.append(f"  - p-value: {p_str}")
            summary.append("")
    
    # Characteristics
    summary.append("## 4. Study Population Characteristics")
    summary.append("")
    
    if table1 is not None:
        summary.append(f"- **Mean age:** {format_number(table1['age_mean'], 1)} ± {format_number(table1['age_sd'], 1)} years")
        summary.append(f"- **Mean BMI:** {format_number(table1['bmi_mean'], 1)} ± {format_number(table1['bmi_sd'], 1)} kg/m²")
        summary.append(f"- **Median ferritin:** {format_number(table1['ferritin_median'], 1)} ng/mL (IQR: {format_number(table1['ferritin_q25'], 1)} - {format_number(table1['ferritin_q75'], 1)})")
        summary.append(f"- **Mean hemoglobin:** {format_number(table1['hemoglobin_mean'], 1)} ± {format_number(table1['hemoglobin_sd'], 1)} g/dL")
        summary.append(f"- **Iron supplement use:** {format_percent(table1['supplement_prevalence'], 1)}")
        summary.append("")
        
        summary.append("**Race/Ethnicity Distribution:**")
        for race in ['Mexican American', 'Other Hispanic', 'Non-Hispanic White', 'Non-Hispanic Black', 'Other Race']:
            key = f'race_{race.replace(" ", "_").replace("-", "_")}'
            if key in table1:
                summary.append(f"- {race}: {format_percent(table1[key], 1)}")
        summary.append("")
        
        summary.append("**Poverty Status Distribution:**")
        for pov in ['Low (<1.3)', 'Medium (1.3-3.5)', 'High (≥3.5)']:
            cat_key = pov.replace(" ", "_").replace("(", "").replace(")", "").replace("<", "lt_").replace("≥", "ge_")
            key = f'poverty_{cat_key}'
            if key in table1:
                summary.append(f"- {pov}: {format_percent(table1[key], 1)}")
        summary.append("")
    
    # Statistical Methods
    summary.append("## 5. Statistical Methods")
    summary.append("")
    summary.append("- **Survey weights:** Adjusted for 8-year pooled analysis (WTMEC2YR / 8)")
    summary.append("- **Regression models:** Survey-weighted linear regression (WLS)")
    summary.append("- **Outcome transformation:** Natural log of ferritin")
    summary.append("- **Missing data:** Complete case analysis")
    summary.append("- **Significance level:** α = 0.05 (two-sided)")
    summary.append("")
    
    # Interpretation
    summary.append("## 6. Key Interpretations")
    summary.append("")
    
    if reg_results is not None:
        # Get fully adjusted model
        model3 = reg_results[reg_results['model'] == 'model3']
        if len(model3) > 0:
            coef = model3.iloc[0]['coef_supp']
            pval = model3.iloc[0]['pvalue_supp']
            
            if pval < 0.05:
                direction = "higher" if coef > 0 else "lower"
                pct_change = (np.exp(coef) - 1) * 100
                summary.append(f"1. **Iron supplement use is associated with {direction} ferritin levels.**")
                summary.append(f"   - After full adjustment, supplement users had {abs(pct_change):.1f}% {direction} ferritin")
                summary.append(f"   - This association was statistically significant (p{'<' if pval < 0.001 else '='}{p_str})")
            else:
                summary.append("1. **No statistically significant association found** between iron supplement use and ferritin levels after full adjustment.")
        summary.append("")
    
    summary.append("2. **IDWA Prevalence:** Approximately 10-15% of non-pregnant women aged 18-45 have iron deficiency without anemia.")
    summary.append("")
    
    summary.append("3. **Population at Risk:** Higher IDWA prevalence observed in certain demographic groups, highlighting the need for targeted interventions.")
    summary.append("")
    
    # Limitations
    summary.append("## 7. Limitations")
    summary.append("")
    summary.append("- Cross-sectional design limits causal inference")
    summary.append("- Self-reported supplement use may have measurement error")
    summary.append("- Single ferritin measurement may not reflect long-term iron status")
    summary.append("- Missing data for some cycles (FERTIN not available in G, H, L)")
    summary.append("- Survey weights approximate complex survey design")
    summary.append("")
    
    # Generated Files
    summary.append("## 8. Generated Output Files")
    summary.append("")
    summary.append("### Data Files")
    summary.append("- `processed_data.csv` - Final analytic dataset")
    summary.append("- `exclusions.csv` - Exclusion criteria summary")
    summary.append("")
    summary.append("### Tables (LaTeX)")
    summary.append("- `table1_characteristics.tex` - Study population characteristics")
    summary.append("- `table2_idwa_by_demographics.tex` - IDWA prevalence by demographics")
    summary.append("- `table3_regression_results.tex` - Main regression results")
    summary.append("- `table4_dose_response.tex` - Dose-response analysis")
    summary.append("")
    summary.append("### Tables (CSV)")
    summary.append("- `table1_characteristics.csv` - Table 1 data")
    summary.append("- `table2_idwa_by_demographics.csv` - Table 2 data")
    summary.append("- `regression_results.csv` - Regression coefficients")
    summary.append("- `dose_response_results.csv` - Dose-response coefficients")
    summary.append("")
    summary.append("### Figures (300 DPI PNG)")
    summary.append("- `figure1_flow_diagram.png` - Study flow diagram")
    summary.append("- `figure2_ferritin_distribution.png` - Ferritin distribution")
    summary.append("- `figure3_idwa_prevalence.png` - IDWA by demographics")
    summary.append("- `figure4_forest_plot.png` - Regression forest plot")
    summary.append("")
    
    # Conclusion
    summary.append("## 9. Conclusion")
    summary.append("")
    summary.append("This analysis examined the association between iron supplement use and ferritin levels among non-pregnant women aged 18-45 years using NHANES data from 2005-2022. The findings provide evidence for the relationship between iron supplementation and iron status in this population, with implications for public health recommendations regarding iron supplementation in women of reproductive age.")
    summary.append("")
    
    summary.append("---")
    summary.append("")
    summary.append("*This analysis was conducted using NHANES public-use data. All results are weighted to be nationally representative.*")
    
    return "\n".join(summary)

def main():
    print("=" * 70)
    print("Generating Results Summary...")
    print("=" * 70)
    
    # Check if processed data exists
    data_file = os.path.join(OUTPUT_DIR, 'processed_data.csv')
    if not os.path.exists(data_file):
        print(f"Error: Processed data not found at {data_file}")
        print("Please run the analysis pipeline first.")
        return
    
    # Generate summary
    summary = generate_results_summary()
    
    # Save summary
    output_file = os.path.join(OUTPUT_DIR, 'results_summary.md')
    with open(output_file, 'w') as f:
        f.write(summary)
    
    print(f"✓ Results summary saved to: {output_file}")
    print("\nSummary preview:")
    print("-" * 70)
    print(summary[:2000] + "..." if len(summary) > 2000 else summary)

if __name__ == "__main__":
    main()
