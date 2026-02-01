#!/usr/bin/env python3
"""
NHANES Iron Deficiency Without Anemia Study - Regression Analysis Script
=======================================================================

This script:
1. Runs survey-weighted linear regression models
2. Model 1: Unadjusted (log ferritin ~ supplement use)
3. Model 2: Demographics-adjusted
4. Model 3: Fully adjusted (add BMI)
5. Performs dose-response analysis
6. Generates forest plot of regression coefficients
7. Outputs regression results in LaTeX table format

Author: NHANES Analysis Pipeline
Date: 2026-01-31
"""

import pandas as pd
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
from statsmodels.regression.linear_model import WLS

# Set random seed for reproducibility
np.random.seed(42)

OUTPUT_DIR = "studies/iron-deficiency-women-2026-01-31/04-analysis"
TABLES_DIR = os.path.join(OUTPUT_DIR, "outputs", "tables")
FIGURES_DIR = os.path.join(OUTPUT_DIR, "outputs", "figures")

def prepare_data_for_regression(df):
    """Prepare data for regression analysis."""
    
    # Create binary variables for race
    df['race_nhw'] = (df['race_category'] == 'Non-Hispanic White').astype(int)
    df['race_nhb'] = (df['race_category'] == 'Non-Hispanic Black').astype(int)
    df['race_mex'] = (df['race_category'] == 'Mexican American').astype(int)
    df['race_oth_hisp'] = (df['race_category'] == 'Other Hispanic').astype(int)
    df['race_other'] = (df['race_category'] == 'Other Race').astype(int)
    
    # Create poverty binary variable
    df['poverty_low'] = (df['poverty_category'] == 'Low (<1.3)').astype(int)
    
    # Create age squared for potential non-linearity
    df['age_sq'] = df['RIDAGEYR'] ** 2
    
    # Create iron supplement binary and categorical variables
    df['supp_any'] = df['iron_supplement']
    
    # Dose categories as dummy variables
    df['dose_low'] = (df['iron_dose'] == 'Low').astype(int)
    df['dose_mod'] = (df['iron_dose'] == 'Moderate').astype(int)
    df['dose_high'] = (df['iron_dose'] == 'High').astype(int)
    
    # Create BMI categories
    df['bmi_under'] = (df['BMXBMI'] < 18.5).astype(int)
    df['bmi_normal'] = ((df['BMXBMI'] >= 18.5) & (df['BMXBMI'] < 25)).astype(int)
    df['bmi_over'] = ((df['BMXBMI'] >= 25) & (df['BMXBMI'] < 30)).astype(int)
    df['bmi_obese'] = (df['BMXBMI'] >= 30).astype(int)
    
    return df

def weighted_least_squares(X, y, weights):
    """Perform weighted least squares regression."""
    
    # Remove rows with missing values
    mask = (~np.isnan(y)) & (~np.isnan(weights)) & (weights > 0)
    for col in X.columns:
        mask = mask & (~np.isnan(X[col]))
    
    X_clean = X[mask].copy()
    y_clean = y[mask].copy()
    w_clean = weights[mask].copy()
    
    if len(y_clean) < 10:
        return None, None, None
    
    # Add constant
    X_clean = sm.add_constant(X_clean)
    
    # Fit WLS
    try:
        model = WLS(y_clean, X_clean, weights=w_clean)
        results = model.fit()
        return results, X_clean, y_clean
    except Exception as e:
        print(f"Error fitting model: {e}")
        return None, None, None

def run_regression_models(df):
    """Run all regression models."""
    
    results = {}
    y = df['log_ferritin'].values
    weights = df['weight_adjusted'].values
    
    print("\n" + "=" * 70)
    print("Fitting Regression Models")
    print("=" * 70)
    
    # Model 1: Unadjusted
    print("\n--- Model 1: Unadjusted ---")
    X1 = df[['supp_any']].copy()
    res1, X1_clean, y1_clean = weighted_least_squares(X1, y, weights)
    
    if res1 is not None:
        conf_int_1 = res1.conf_int()
        results['model1'] = {
            'name': 'Unadjusted',
            'n': len(y1_clean),
            'r2': res1.rsquared,
            'coef_supp': res1.params.get('supp_any', np.nan),
            'se_supp': res1.bse.get('supp_any', np.nan),
            'pvalue_supp': res1.pvalues.get('supp_any', np.nan),
            'ci_low_supp': conf_int_1.loc['supp_any', 0] if 'supp_any' in conf_int_1.index else np.nan,
            'ci_high_supp': conf_int_1.loc['supp_any', 1] if 'supp_any' in conf_int_1.index else np.nan,
            'summary': str(res1.summary())
        }
        print(f"  N: {results['model1']['n']}")
        print(f"  Iron supplement coefficient: {results['model1']['coef_supp']:.4f}")
        print(f"  95% CI: [{results['model1']['ci_low_supp']:.4f}, {results['model1']['ci_high_supp']:.4f}]")
        print(f"  p-value: {results['model1']['pvalue_supp']:.4f}")
    
    # Model 2: Demographics-adjusted
    print("\n--- Model 2: Demographics-adjusted ---")
    X2 = df[['supp_any', 'RIDAGEYR', 'race_nhb', 'race_mex', 'race_oth_hisp', 
             'race_other', 'INDFMPIR']].copy()
    res2, X2_clean, y2_clean = weighted_least_squares(X2, y, weights)
    
    if res2 is not None:
        conf_int_2 = res2.conf_int()
        results['model2'] = {
            'name': 'Demographics-adjusted',
            'n': len(y2_clean),
            'r2': res2.rsquared,
            'coef_supp': res2.params.get('supp_any', np.nan),
            'se_supp': res2.bse.get('supp_any', np.nan),
            'pvalue_supp': res2.pvalues.get('supp_any', np.nan),
            'ci_low_supp': conf_int_2.loc['supp_any', 0] if 'supp_any' in conf_int_2.index else np.nan,
            'ci_high_supp': conf_int_2.loc['supp_any', 1] if 'supp_any' in conf_int_2.index else np.nan,
            'coef_age': res2.params.get('RIDAGEYR', np.nan),
            'coef_nhb': res2.params.get('race_nhb', np.nan),
            'coef_mex': res2.params.get('race_mex', np.nan),
            'coef_pov': res2.params.get('INDFMPIR', np.nan),
            'summary': str(res2.summary())
        }
        print(f"  N: {results['model2']['n']}")
        print(f"  Iron supplement coefficient: {results['model2']['coef_supp']:.4f}")
        print(f"  95% CI: [{results['model2']['ci_low_supp']:.4f}, {results['model2']['ci_high_supp']:.4f}]")
        print(f"  p-value: {results['model2']['pvalue_supp']:.4f}")
    
    # Model 3: Fully adjusted (add BMI)
    print("\n--- Model 3: Fully adjusted ---")
    X3 = df[['supp_any', 'RIDAGEYR', 'race_nhb', 'race_mex', 'race_oth_hisp', 
             'race_other', 'INDFMPIR', 'BMXBMI']].copy()
    res3, X3_clean, y3_clean = weighted_least_squares(X3, y, weights)
    
    if res3 is not None:
        conf_int_3 = res3.conf_int()
        results['model3'] = {
            'name': 'Fully adjusted',
            'n': len(y3_clean),
            'r2': res3.rsquared,
            'coef_supp': res3.params.get('supp_any', np.nan),
            'se_supp': res3.bse.get('supp_any', np.nan),
            'pvalue_supp': res3.pvalues.get('supp_any', np.nan),
            'ci_low_supp': conf_int_3.loc['supp_any', 0] if 'supp_any' in conf_int_3.index else np.nan,
            'ci_high_supp': conf_int_3.loc['supp_any', 1] if 'supp_any' in conf_int_3.index else np.nan,
            'coef_age': res3.params.get('RIDAGEYR', np.nan),
            'coef_nhb': res3.params.get('race_nhb', np.nan),
            'coef_mex': res3.params.get('race_mex', np.nan),
            'coef_pov': res3.params.get('INDFMPIR', np.nan),
            'coef_bmi': res3.params.get('BMXBMI', np.nan),
            'summary': str(res3.summary())
        }
        print(f"  N: {results['model3']['n']}")
        print(f"  Iron supplement coefficient: {results['model3']['coef_supp']:.4f}")
        print(f"  95% CI: [{results['model3']['ci_low_supp']:.4f}, {results['model3']['ci_high_supp']:.4f}]")
        print(f"  p-value: {results['model3']['pvalue_supp']:.4f}")
    
    return results

def run_dose_response_analysis(df):
    """Run dose-response analysis."""
    
    print("\n" + "=" * 70)
    print("Dose-Response Analysis")
    print("=" * 70)
    
    y = df['log_ferritin'].values
    weights = df['weight_adjusted'].values
    
    # Model with dose categories (None = reference)
    print("\n--- Dose Categories ---")
    X_dose = df[['dose_low', 'dose_mod', 'dose_high', 'RIDAGEYR', 'race_nhb', 
                 'race_mex', 'race_oth_hisp', 'race_other', 'INDFMPIR', 'BMXBMI']].copy()
    
    res_dose, X_clean, y_clean = weighted_least_squares(X_dose, y, weights)
    
    dose_results = {}
    
    if res_dose is not None:
        conf_int_dose = res_dose.conf_int()
        dose_results = {
            'n': len(y_clean),
            'coef_low': res_dose.params.get('dose_low', np.nan),
            'se_low': res_dose.bse.get('dose_low', np.nan),
            'pvalue_low': res_dose.pvalues.get('dose_low', np.nan),
            'ci_low_low': conf_int_dose.loc['dose_low', 0] if 'dose_low' in conf_int_dose.index else np.nan,
            'ci_high_low': conf_int_dose.loc['dose_low', 1] if 'dose_low' in conf_int_dose.index else np.nan,
            'coef_mod': res_dose.params.get('dose_mod', np.nan),
            'se_mod': res_dose.bse.get('dose_mod', np.nan),
            'pvalue_mod': res_dose.pvalues.get('dose_mod', np.nan),
            'ci_low_mod': conf_int_dose.loc['dose_mod', 0] if 'dose_mod' in conf_int_dose.index else np.nan,
            'ci_high_mod': conf_int_dose.loc['dose_mod', 1] if 'dose_mod' in conf_int_dose.index else np.nan,
            'coef_high': res_dose.params.get('dose_high', np.nan),
            'se_high': res_dose.bse.get('dose_high', np.nan),
            'pvalue_high': res_dose.pvalues.get('dose_high', np.nan),
            'ci_low_high': conf_int_dose.loc['dose_high', 0] if 'dose_high' in conf_int_dose.index else np.nan,
            'ci_high_high': conf_int_dose.loc['dose_high', 1] if 'dose_high' in conf_int_dose.index else np.nan,
        }
        
        print(f"  N: {dose_results['n']}")
        print(f"\n  Low dose coefficient: {dose_results['coef_low']:.4f}")
        print(f"    95% CI: [{dose_results['ci_low_low']:.4f}, {dose_results['ci_high_low']:.4f}]")
        print(f"    p-value: {dose_results['pvalue_low']:.4f}")
        
        print(f"\n  Moderate dose coefficient: {dose_results['coef_mod']:.4f}")
        print(f"    95% CI: [{dose_results['ci_low_mod']:.4f}, {dose_results['ci_high_mod']:.4f}]")
        print(f"    p-value: {dose_results['pvalue_mod']:.4f}")
        
        print(f"\n  High dose coefficient: {dose_results['coef_high']:.4f}")
        print(f"    95% CI: [{dose_results['ci_low_high']:.4f}, {dose_results['ci_high_high']:.4f}]")
        print(f"    p-value: {dose_results['pvalue_high']:.4f}")
    
    return dose_results

def generate_regression_table_latex(results):
    """Generate LaTeX table for regression results."""
    
    latex = []
    latex.append("\\begin{table}[htbp]")
    latex.append("\\centering")
    latex.append("\\caption{Association Between Iron Supplement Use and Log-Transformed Ferritin}")
    latex.append("\\label{tab:regression}")
    latex.append("\\begin{tabular}{lccc}")
    latex.append("\\toprule")
    latex.append("\\textbf{Variable} & \\textbf{Model 1} & \\textbf{Model 2} & \\textbf{Model 3} \\\\")
    latex.append(" & \\textbf{(Unadjusted)} & \\textbf{(Demographics)} & \\textbf{(Fully Adjusted)} \\\\")
    latex.append("\\midrule")
    
    # Iron supplement use
    if 'model1' in results:
        m1 = results['model1']
        coef1 = f"{m1['coef_supp']:.3f}"
        ci1 = f"[{m1['ci_low_supp']:.3f}, {m1['ci_high_supp']:.3f}]"
        p1 = f"{m1['pvalue_supp']:.3f}"
        if m1['pvalue_supp'] < 0.001:
            p1 = "<0.001"
        m1_str = f"{coef1} {ci1}; p={p1}"
    else:
        m1_str = "N/A"
    
    if 'model2' in results:
        m2 = results['model2']
        coef2 = f"{m2['coef_supp']:.3f}"
        ci2 = f"[{m2['ci_low_supp']:.3f}, {m2['ci_high_supp']:.3f}]"
        p2 = f"{m2['pvalue_supp']:.3f}"
        if m2['pvalue_supp'] < 0.001:
            p2 = "<0.001"
        m2_str = f"{coef2} {ci2}; p={p2}"
    else:
        m2_str = "N/A"
    
    if 'model3' in results:
        m3 = results['model3']
        coef3 = f"{m3['coef_supp']:.3f}"
        ci3 = f"[{m3['ci_low_supp']:.3f}, {m3['ci_high_supp']:.3f}]"
        p3 = f"{m3['pvalue_supp']:.3f}"
        if m3['pvalue_supp'] < 0.001:
            p3 = "<0.001"
        m3_str = f"{coef3} {ci3}; p={p3}"
    else:
        m3_str = "N/A"
    
    latex.append(f"Iron supplement use & {m1_str} & {m2_str} & {m3_str} \\\\")
    latex.append("\\midrule")
    
    # Age
    if 'model2' in results and 'coef_age' in results['model2']:
        age2 = f"{results['model2']['coef_age']:.3f}"
        age3 = f"{results['model3']['coef_age']:.3f}" if 'model3' in results else "N/A"
        latex.append(f"Age, years & --- & {age2} & {age3} \\\\")
    
    # Race (Non-Hispanic Black)
    if 'model2' in results and 'coef_nhb' in results['model2']:
        nhb2 = f"{results['model2']['coef_nhb']:.3f}"
        nhb3 = f"{results['model3']['coef_nhb']:.3f}" if 'model3' in results else "N/A"
        latex.append(f"Non-Hispanic Black & --- & {nhb2} & {nhb3} \\\\")
    
    # Race (Mexican American)
    if 'model2' in results and 'coef_mex' in results['model2']:
        mex2 = f"{results['model2']['coef_mex']:.3f}"
        mex3 = f"{results['model3']['coef_mex']:.3f}" if 'model3' in results else "N/A"
        latex.append(f"Mexican American & --- & {mex2} & {mex3} \\\\")
    
    # Poverty ratio
    if 'model2' in results and 'coef_pov' in results['model2']:
        pov2 = f"{results['model2']['coef_pov']:.3f}"
        pov3 = f"{results['model3']['coef_pov']:.3f}" if 'model3' in results else "N/A"
        latex.append(f"Poverty ratio & --- & {pov2} & {pov3} \\\\")
    
    # BMI
    if 'model3' in results and 'coef_bmi' in results['model3']:
        bmi3 = f"{results['model3']['coef_bmi']:.3f}"
        latex.append(f"BMI, kg/m\\textsuperscript{{2}} & --- & --- & {bmi3} \\\\")
    
    latex.append("\\midrule")
    
    # Sample size
    n1 = str(results['model1']['n']) if 'model1' in results else "N/A"
    n2 = str(results['model2']['n']) if 'model2' in results else "N/A"
    n3 = str(results['model3']['n']) if 'model3' in results else "N/A"
    latex.append(f"N & {n1} & {n2} & {n3} \\\\")
    
    # R-squared
    r1 = f"{results['model1']['r2']:.3f}" if 'model1' in results else "N/A"
    r2 = f"{results['model2']['r2']:.3f}" if 'model2' in results else "N/A"
    r3 = f"{results['model3']['r2']:.3f}" if 'model3' in results else "N/A"
    latex.append(f"R\\textsuperscript{{2}} & {r1} & {r2} & {r3} \\\\")
    
    latex.append("\\bottomrule")
    latex.append("\\end{tabular}")
    latex.append("\\begin{flushleft}")
    latex.append("\\footnotesize{\\textit{Note:} Values are regression coefficients with 95\\% CI. ")
    latex.append("Model 1: Unadjusted. Model 2: Adjusted for age, race/ethnicity, and poverty ratio. ")
    latex.append("Model 3: Additionally adjusted for BMI. Reference category for race: Non-Hispanic White.}")
    latex.append("\\end{flushleft}")
    latex.append("\\end{table}")
    
    return "\n".join(latex)

def generate_dose_response_table_latex(dose_results):
    """Generate LaTeX table for dose-response analysis."""
    
    latex = []
    latex.append("\\begin{table}[htbp]")
    latex.append("\\centering")
    latex.append("\\caption{Dose-Response Analysis: Iron Supplement Dose and Log-Transformed Ferritin}")
    latex.append("\\label{tab:dose_response}")
    latex.append("\\begin{tabular}{lcccc}")
    latex.append("\\toprule")
    latex.append("\\textbf{Dose Category} & \\textbf{Coefficient} & \\textbf{95\\% CI} & \\textbf{p-value} \\\\")
    latex.append("\\midrule")
    
    # None (reference)
    latex.append("None (reference) & 0.000 & Reference & --- \\\\")
    
    # Low dose
    if 'coef_low' in dose_results:
        coef = f"{dose_results['coef_low']:.3f}"
        ci = f"[{dose_results['ci_low_low']:.3f}, {dose_results['ci_high_low']:.3f}]"
        p = f"{dose_results['pvalue_low']:.3f}"
        if dose_results['pvalue_low'] < 0.001:
            p = "<0.001"
        latex.append(f"Low & {coef} & {ci} & {p} \\\\")
    
    # Moderate dose
    if 'coef_mod' in dose_results:
        coef = f"{dose_results['coef_mod']:.3f}"
        ci = f"[{dose_results['ci_low_mod']:.3f}, {dose_results['ci_high_mod']:.3f}]"
        p = f"{dose_results['pvalue_mod']:.3f}"
        if dose_results['pvalue_mod'] < 0.001:
            p = "<0.001"
        latex.append(f"Moderate & {coef} & {ci} & {p} \\\\")
    
    # High dose
    if 'coef_high' in dose_results:
        coef = f"{dose_results['coef_high']:.3f}"
        ci = f"[{dose_results['ci_low_high']:.3f}, {dose_results['ci_high_high']:.3f}]"
        p = f"{dose_results['pvalue_high']:.3f}"
        if dose_results['pvalue_high'] < 0.001:
            p = "<0.001"
        latex.append(f"High & {coef} & {ci} & {p} \\\\")
    
    latex.append("\\bottomrule")
    latex.append("\\end{tabular}")
    latex.append("\\begin{flushleft}")
    latex.append("\\footnotesize{\\textit{Note:} Low dose: >0 to <18 mg/day. ")
    latex.append("Moderate dose: 18 to <27 mg/day. High dose: ≥27 mg/day. ")
    latex.append("Model adjusted for age, race/ethnicity, poverty ratio, and BMI.}")
    latex.append("\\end{flushleft}")
    latex.append("\\end{table}")
    
    return "\n".join(latex)

def create_forest_plot(results, dose_results, output_file):
    """Create forest plot of regression coefficients."""
    
    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    
    # Prepare data for plotting
    labels = []
    coeffs = []
    ci_lows = []
    ci_highs = []
    colors = []
    
    # Main models
    if 'model1' in results:
        labels.append('Model 1: Unadjusted')
        coeffs.append(results['model1']['coef_supp'])
        ci_lows.append(results['model1']['ci_low_supp'])
        ci_highs.append(results['model1']['ci_high_supp'])
        colors.append('#2E86AB')
    
    if 'model2' in results:
        labels.append('Model 2: Demographics-adjusted')
        coeffs.append(results['model2']['coef_supp'])
        ci_lows.append(results['model2']['ci_low_supp'])
        ci_highs.append(results['model2']['ci_high_supp'])
        colors.append('#A23B72')
    
    if 'model3' in results:
        labels.append('Model 3: Fully adjusted')
        coeffs.append(results['model3']['coef_supp'])
        ci_lows.append(results['model3']['ci_low_supp'])
        ci_highs.append(results['model3']['ci_high_supp'])
        colors.append('#F18F01')
    
    # Add dose-response
    if 'coef_low' in dose_results:
        labels.append('Dose: Low')
        coeffs.append(dose_results['coef_low'])
        ci_lows.append(dose_results['ci_low_low'])
        ci_highs.append(dose_results['ci_high_low'])
        colors.append('#C73E1D')
    
    if 'coef_mod' in dose_results:
        labels.append('Dose: Moderate')
        coeffs.append(dose_results['coef_mod'])
        ci_lows.append(dose_results['ci_low_mod'])
        ci_highs.append(dose_results['ci_high_mod'])
        colors.append('#6A994E')
    
    if 'coef_high' in dose_results:
        labels.append('Dose: High')
        coeffs.append(dose_results['coef_high'])
        ci_lows.append(dose_results['ci_low_high'])
        ci_highs.append(dose_results['ci_high_high'])
        colors.append('#BC4B51')
    
    # Plot
    y_pos = np.arange(len(labels))
    
    # Reference line at 0
    ax.axvline(x=0, color='gray', linestyle='--', linewidth=0.8, alpha=0.7)
    
    # Plot points and error bars
    for i, (label, coef, ci_low, ci_high, color) in enumerate(zip(labels, coeffs, ci_lows, ci_highs, colors)):
        ax.errorbar(coef, i, xerr=[[coef - ci_low], [ci_high - coef]], 
                   fmt='o', color=color, ecolor=color, capsize=5, capthick=2, 
                   markersize=8, elinewidth=2)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=11)
    ax.set_xlabel('Regression Coefficient (Log Ferritin)', fontsize=12, fontweight='bold')
    ax.set_title('Forest Plot: Association Between Iron Supplement Use and Ferritin\n(Non-Pregnant Women 18-45 Years, NHANES 2005-2022)', 
                fontsize=13, fontweight='bold', pad=15)
    
    # Invert y-axis so first model is at top
    ax.invert_yaxis()
    
    # Add grid
    ax.grid(axis='x', alpha=0.3, linestyle=':')
    ax.set_axisbelow(True)
    
    # Tight layout
    plt.tight_layout()
    
    # Save
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"\nSaved forest plot to: {output_file}")
    plt.close()

def main():
    print("=" * 70)
    print("NHANES Iron Deficiency Without Anemia - Regression Analysis")
    print("=" * 70)
    print()
    
    # Load processed data
    data_file = os.path.join(OUTPUT_DIR, 'processed_data.csv')
    if not os.path.exists(data_file):
        print(f"Error: Processed data not found at {data_file}")
        print("Please run 01_data_prep.py first.")
        sys.exit(1)
    
    df = pd.read_csv(data_file)
    print(f"Loaded processed data: {len(df)} rows")
    print()
    
    # Prepare data for regression
    df = prepare_data_for_regression(df)
    
    # Run main regression models
    results = run_regression_models(df)
    
    # Run dose-response analysis
    dose_results = run_dose_response_analysis(df)
    
    # Generate LaTeX tables
    print("\n" + "=" * 70)
    print("Generating LaTeX tables...")
    print("=" * 70)
    
    # Table 3: Regression results
    table3_latex = generate_regression_table_latex(results)
    table3_file = os.path.join(TABLES_DIR, 'table3_regression_results.tex')
    with open(table3_file, 'w') as f:
        f.write(table3_latex)
    print(f"Saved Table 3 to: {table3_file}")
    
    # Table 4: Dose-response results
    table4_latex = generate_dose_response_table_latex(dose_results)
    table4_file = os.path.join(TABLES_DIR, 'table4_dose_response.tex')
    with open(table4_file, 'w') as f:
        f.write(table4_latex)
    print(f"Saved Table 4 to: {table4_file}")
    
    # Save regression results to CSV
    results_df = pd.DataFrame([{
        'model': key,
        **{k: v for k, v in value.items() if k != 'summary'}
    } for key, value in results.items()])
    results_csv = os.path.join(TABLES_DIR, 'regression_results.csv')
    results_df.to_csv(results_csv, index=False)
    print(f"Saved regression results CSV to: {results_csv}")
    
    # Save dose-response results to CSV
    dose_df = pd.DataFrame([dose_results])
    dose_csv = os.path.join(TABLES_DIR, 'dose_response_results.csv')
    dose_df.to_csv(dose_csv, index=False)
    print(f"Saved dose-response results CSV to: {dose_csv}")
    
    # Create forest plot
    print("\n" + "=" * 70)
    print("Creating forest plot...")
    print("=" * 70)
    
    forest_file = os.path.join(FIGURES_DIR, 'figure4_forest_plot.png')
    create_forest_plot(results, dose_results, forest_file)
    
    print("\n" + "=" * 70)
    print("Regression analysis complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()
