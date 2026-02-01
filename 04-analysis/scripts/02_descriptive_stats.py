#!/usr/bin/env python3
"""
NHANES Iron Deficiency Without Anemia Study - Descriptive Statistics Script
==========================================================================

This script:
1. Calculates sample characteristics (Table 1)
2. Computes weighted prevalence of IDWA
3. Generates demographic breakdowns
4. Analyzes iron status distribution
5. Computes supplement use prevalence
6. Outputs LaTeX table and CSV

Author: NHANES Analysis Pipeline
Date: 2026-01-31
"""

import pandas as pd
import numpy as np
import os
import sys
from scipy import stats

# Set random seed for reproducibility
np.random.seed(42)

OUTPUT_DIR = "studies/iron-deficiency-women-2026-01-31/04-analysis"
TABLES_DIR = os.path.join(OUTPUT_DIR, "outputs", "tables")

def weighted_mean(x, weights):
    """Calculate weighted mean."""
    mask = ~np.isnan(x) & ~np.isnan(weights) & (weights > 0)
    if mask.sum() == 0:
        return np.nan
    return np.average(x[mask], weights=weights[mask])

def weighted_std(x, weights):
    """Calculate weighted standard deviation."""
    mask = ~np.isnan(x) & ~np.isnan(weights) & (weights > 0)
    if mask.sum() < 2:
        return np.nan
    
    mean = weighted_mean(x, weights)
    variance = np.average((x[mask] - mean)**2, weights=weights[mask])
    n_eff = mask.sum()
    if n_eff > 1:
        variance = variance * n_eff / (n_eff - 1)
    return np.sqrt(variance)

def weighted_proportion(x, weights):
    """Calculate weighted proportion."""
    mask = ~np.isnan(x) & ~np.isnan(weights) & (weights > 0)
    if mask.sum() == 0:
        return np.nan, np.nan
    
    x_clean = x[mask].astype(float)
    w_clean = weights[mask]
    
    prop = np.average(x_clean, weights=w_clean)
    n_eff = mask.sum()
    
    if n_eff > 1:
        se = np.sqrt(prop * (1 - prop) / n_eff)
    else:
        se = np.nan
    
    return prop, se

def format_percent(value, se=None):
    """Format percentage with standard error."""
    if np.isnan(value):
        return "N/A"
    if se is not None and not np.isnan(se):
        return f"{value*100:.1f} ({se*100:.1f})"
    return f"{value*100:.1f}"

def format_mean_sd(mean, sd):
    """Format mean (SD)."""
    if np.isnan(mean):
        return "N/A"
    if sd is not None and not np.isnan(sd):
        return f"{mean:.1f} ({sd:.1f})"
    return f"{mean:.1f}"

def format_median_iqr(median, q25, q75):
    """Format median [IQR]."""
    if np.isnan(median):
        return "N/A"
    return f"{median:.1f} [{q25:.1f}, {q75:.1f}]"

def calculate_table1_characteristics(df):
    """Calculate Table 1: Study population characteristics."""
    
    results = {}
    weights = df['weight_adjusted'].values
    
    # Overall N
    results['N'] = len(df)
    results['N_weighted'] = weights.sum()
    
    # Age
    results['age_mean'] = weighted_mean(df['RIDAGEYR'].values, weights)
    results['age_sd'] = weighted_std(df['RIDAGEYR'].values, weights)
    results['age_median'] = np.median(df['RIDAGEYR'].dropna())
    results['age_q25'] = df['RIDAGEYR'].quantile(0.25)
    results['age_q75'] = df['RIDAGEYR'].quantile(0.75)
    
    # Race/Ethnicity
    for race in ['Mexican American', 'Other Hispanic', 'Non-Hispanic White', 
                 'Non-Hispanic Black', 'Other Race']:
        race_indicator = (df['race_category'] == race).astype(int).values
        prop, se = weighted_proportion(race_indicator, weights)
        results[f'race_{race.replace(" ", "_").replace("-", "_")}'] = prop
        results[f'race_{race.replace(" ", "_").replace("-", "_")}_se'] = se
    
    # Poverty ratio
    poverty_mean = weighted_mean(df['INDFMPIR'].values, weights)
    poverty_sd = weighted_std(df['INDFMPIR'].values, weights)
    results['poverty_mean'] = poverty_mean
    results['poverty_sd'] = poverty_sd
    
    for pov_cat in ['Low (<1.3)', 'Medium (1.3-3.5)', 'High (>=3.5)']:
        pov_indicator = (df['poverty_category'] == pov_cat).astype(int).values
        prop, se = weighted_proportion(pov_indicator, weights)
        cat_key = pov_cat.replace(" ", "_").replace("(", "").replace(")", "").replace("<", "lt_").replace(">=", "ge_")
        results[f'poverty_{cat_key}'] = prop
        results[f'poverty_{cat_key}_se'] = se
    
    # BMI
    results['bmi_mean'] = weighted_mean(df['BMXBMI'].values, weights)
    results['bmi_sd'] = weighted_std(df['BMXBMI'].values, weights)
    
    # Iron status
    results['ferritin_mean'] = weighted_mean(df['LBXFER'].values, weights)
    results['ferritin_sd'] = weighted_std(df['LBXFER'].values, weights)
    results['ferritin_median'] = df['LBXFER'].median()
    results['ferritin_q25'] = df['LBXFER'].quantile(0.25)
    results['ferritin_q75'] = df['LBXFER'].quantile(0.75)
    
    results['hemoglobin_mean'] = weighted_mean(df['LBXHGB'].values, weights)
    results['hemoglobin_sd'] = weighted_std(df['LBXHGB'].values, weights)
    
    # IDWA prevalence
    idwa_prop, idwa_se = weighted_proportion(df['IDWA'].astype(int).values, weights)
    results['idwa_prevalence'] = idwa_prop
    results['idwa_se'] = idwa_se
    
    # Iron deficiency (any)
    iron_def_prop, iron_def_se = weighted_proportion(df['iron_deficient'].astype(int).values, weights)
    results['iron_deficiency_prevalence'] = iron_def_prop
    results['iron_deficiency_se'] = iron_def_se
    
    # Anemia
    anemia_prop, anemia_se = weighted_proportion((~df['not_anemic']).astype(int).values, weights)
    results['anemia_prevalence'] = anemia_prop
    results['anemia_se'] = anemia_se
    
    # Iron supplement use
    supp_prop, supp_se = weighted_proportion(df['iron_supplement'].values, weights)
    results['supplement_prevalence'] = supp_prop
    results['supplement_se'] = supp_se
    
    # Iron dose categories
    for dose in ['None', 'Low', 'Moderate', 'High']:
        dose_indicator = (df['iron_dose'] == dose).astype(int).values
        prop, se = weighted_proportion(dose_indicator, weights)
        results[f'dose_{dose.lower()}'] = prop
        results[f'dose_{dose.lower()}_se'] = se
    
    return results

def calculate_idwa_by_demographics(df):
    """Calculate IDWA prevalence by demographic subgroups."""
    
    results = []
    
    # Overall
    weights = df['weight_adjusted'].values
    idwa_prop, idwa_se = weighted_proportion(df['IDWA'].astype(int).values, weights)
    results.append({
        'group': 'Overall',
        'subgroup': 'All',
        'n_total': len(df),
        'n_idwa': df['IDWA'].sum(),
        'idwa_prevalence': idwa_prop,
        'idwa_se': idwa_se,
        'idwa_pct': format_percent(idwa_prop, idwa_se)
    })
    
    # By age group
    for age_grp in ['18-25', '26-30', '31-35', '36-40', '41-45']:
        subgroup_df = df[df['age_group'] == age_grp]
        if len(subgroup_df) > 0:
            weights = subgroup_df['weight_adjusted'].values
            idwa_prop, idwa_se = weighted_proportion(subgroup_df['IDWA'].astype(int).values, weights)
            results.append({
                'group': 'Age Group',
                'subgroup': age_grp,
                'n_total': len(subgroup_df),
                'n_idwa': subgroup_df['IDWA'].sum(),
                'idwa_prevalence': idwa_prop,
                'idwa_se': idwa_se,
                'idwa_pct': format_percent(idwa_prop, idwa_se)
            })
    
    # By race/ethnicity
    for race in ['Mexican American', 'Other Hispanic', 'Non-Hispanic White', 
                 'Non-Hispanic Black', 'Other Race']:
        subgroup_df = df[df['race_category'] == race]
        if len(subgroup_df) > 0:
            weights = subgroup_df['weight_adjusted'].values
            idwa_prop, idwa_se = weighted_proportion(subgroup_df['IDWA'].astype(int).values, weights)
            results.append({
                'group': 'Race/Ethnicity',
                'subgroup': race,
                'n_total': len(subgroup_df),
                'n_idwa': subgroup_df['IDWA'].sum(),
                'idwa_prevalence': idwa_prop,
                'idwa_se': idwa_se,
                'idwa_pct': format_percent(idwa_prop, idwa_se)
            })
    
    # By poverty category
    for pov in ['Low (<1.3)', 'Medium (1.3-3.5)', 'High (>=3.5)']:
        subgroup_df = df[df['poverty_category'] == pov]
        if len(subgroup_df) > 0:
            weights = subgroup_df['weight_adjusted'].values
            idwa_prop, idwa_se = weighted_proportion(subgroup_df['IDWA'].astype(int).values, weights)
            results.append({
                'group': 'Poverty Status',
                'subgroup': pov,
                'n_total': len(subgroup_df),
                'n_idwa': subgroup_df['IDWA'].sum(),
                'idwa_prevalence': idwa_prop,
                'idwa_se': idwa_se,
                'idwa_pct': format_percent(idwa_prop, idwa_se)
            })
    
    # By supplement use
    for supp in [0, 1]:
        subgroup_df = df[df['iron_supplement'] == supp]
        if len(subgroup_df) > 0:
            weights = subgroup_df['weight_adjusted'].values
            idwa_prop, idwa_se = weighted_proportion(subgroup_df['IDWA'].astype(int).values, weights)
            label = 'No' if supp == 0 else 'Yes'
            results.append({
                'group': 'Iron Supplement',
                'subgroup': label,
                'n_total': len(subgroup_df),
                'n_idwa': subgroup_df['IDWA'].sum(),
                'idwa_prevalence': idwa_prop,
                'idwa_se': idwa_se,
                'idwa_pct': format_percent(idwa_prop, idwa_se)
            })
    
    return pd.DataFrame(results)

def generate_table1_latex(results):
    """Generate Table 1 in LaTeX format."""
    
    lines = [
        r"\begin{table}[htbp]",
        r"\centering",
        r"\caption{Characteristics of Study Population}",
        r"\label{tab:table1}",
        r"\begin{tabular}{lc}",
        r"\toprule",
        r"\textbf{Characteristic} & \textbf{Value} \\",
        r"\midrule",
        f"Sample size, n & {results['N']:,} \\\\",
        r"\midrule",
        r"\textbf{Age, years} & \\",
        f"\quad Mean (SD) & {format_mean_sd(results['age_mean'], results['age_sd'])} \\\\",
        f"\quad Median [IQR] & {format_median_iqr(results['age_median'], results['age_q25'], results['age_q75'])} \\\\",
        r"\midrule",
    ]
    
    # Race/Ethnicity
    lines.append(r"\textbf{Race/Ethnicity, \\% (SE)} & \\")
    for race in ['Mexican American', 'Other Hispanic', 'Non-Hispanic White', 
                 'Non-Hispanic Black', 'Other Race']:
        key = f'race_{race.replace(" ", "_").replace("-", "_")}'
        pct = format_percent(results[key], results.get(f'{key}_se'))
        lines.append(f"\quad {race} & {pct} \\\\")
    lines.append(r"\midrule")
    
    # Poverty
    lines.append(r"\textbf{Poverty Status} & \\")
    lines.append(f"\quad Poverty ratio, mean (SD) & {format_mean_sd(results['poverty_mean'], results['poverty_sd'])} \\\\")
    lines.append(r"\quad Poverty category, \\% (SE) & \\")
    for pov_cat in ['Low (<1.3)', 'Medium (1.3-3.5)', 'High (>=3.5)']:
        cat_key = pov_cat.replace(" ", "_").replace("(", "").replace(")", "").replace("<", "lt_").replace(">=", "ge_")
        key = f'poverty_{cat_key}'
        pct = format_percent(results[key], results.get(f'{key}_se'))
        lines.append(f"\quad \quad {pov_cat} & {pct} \\\\")
    lines.append(r"\midrule")
    
    # BMI
    lines.append(f"\\textbf{{BMI, kg/m\\textsuperscript{{2}}, mean (SD)}} & {format_mean_sd(results['bmi_mean'], results['bmi_sd'])} \\\\")
    lines.append(r"\midrule")
    
    # Iron Status
    lines.append(r"\textbf{Iron Status} & \\")
    lines.append(f"\quad Ferritin, ng/mL, median [IQR] & {format_median_iqr(results['ferritin_median'], results['ferritin_q25'], results['ferritin_q75'])} \\\\")
    lines.append(f"\quad Hemoglobin, g/dL, mean (SD) & {format_mean_sd(results['hemoglobin_mean'], results['hemoglobin_sd'])} \\\\")
    lines.append(r"\midrule")
    
    # IDWA
    lines.append(f"\\textbf{{IDWA prevalence, \\% (SE)}} & {format_percent(results['idwa_prevalence'], results['idwa_se'])} \\\\")
    lines.append(f"Iron deficiency prevalence, \\% (SE) & {format_percent(results['iron_deficiency_prevalence'], results['iron_deficiency_se'])} \\\\")
    lines.append(f"Anemia prevalence, \\% (SE) & {format_percent(results['anemia_prevalence'], results['anemia_se'])} \\\\")
    lines.append(r"\midrule")
    
    # Supplements
    lines.append(f"\\textbf{{Iron supplement use, \\% (SE)}} & {format_percent(results['supplement_prevalence'], results['supplement_se'])} \\\\")
    lines.append(r"\quad Iron dose category, \\% (SE) & \\")
    for dose in ['None', 'Low', 'Moderate', 'High']:
        key = f'dose_{dose.lower()}'
        pct = format_percent(results[key], results.get(f'{key}_se'))
        lines.append(f"\quad \quad {dose} & {pct} \\\\")
    
    lines.extend([
        r"\bottomrule",
        r"\end{tabular}",
        r"\begin{flushleft}",
        r"\footnotesize{\textit{Note:} IDWA = Iron Deficiency Without Anemia. Values are weighted estimates unless otherwise noted. SE = standard error. IQR = interquartile range.}",
        r"\end{flushleft}",
        r"\end{table}",
    ])
    
    return "\n".join(lines)

def generate_table2_latex(df_idwa):
    """Generate Table 2 (IDWA by demographics) in LaTeX format."""
    
    lines = [
        r"\begin{table}[htbp]",
        r"\centering",
        r"\caption{Prevalence of Iron Deficiency Without Anemia by Demographic Characteristics}",
        r"\label{tab:table2}",
        r"\begin{tabular}{lccc}",
        r"\toprule",
        r"\textbf{Characteristic} & \textbf{n/N} & \textbf{Prevalence, \\% (SE)} \\",
        r"\midrule",
    ]
    
    # Group by category
    groups = df_idwa['group'].unique()
    
    for group in groups:
        group_data = df_idwa[df_idwa['group'] == group]
        
        if len(group_data) > 0:
            # Group header
            lines.append(f"\\textbf{{{group}}} & & \\\\")
            
            for _, row in group_data.iterrows():
                subgroup = row['subgroup']
                n_idwa = int(row['n_idwa'])
                n_total = int(row['n_total'])
                pct = row['idwa_pct']
                lines.append(f"\quad {subgroup} & {n_idwa}/{n_total} & {pct} \\\\")
            
            if group != groups[-1]:
                lines.append(r"\midrule")
    
    lines.extend([
        r"\bottomrule",
        r"\end{tabular}",
        r"\begin{flushleft}",
        r"\footnotesize{\textit{Note:} n = number with IDWA; N = total in subgroup. SE = standard error.}",
        r"\end{flushleft}",
        r"\end{table}",
    ])
    
    return "\n".join(lines)

def main():
    print("=" * 70)
    print("NHANES Iron Deficiency Without Anemia - Descriptive Statistics")
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
    
    # Calculate Table 1 characteristics
    print("=" * 70)
    print("Calculating Table 1: Study population characteristics...")
    print("=" * 70)
    
    table1_results = calculate_table1_characteristics(df)
    
    # Display results
    print(f"\nSample size: {table1_results['N']:,}")
    print(f"Weighted sample size: {table1_results['N_weighted']:,.0f}")
    print(f"\nAge: {format_mean_sd(table1_results['age_mean'], table1_results['age_sd'])} years")
    print(f"IDWA prevalence: {format_percent(table1_results['idwa_prevalence'], table1_results['idwa_se'])}")
    print(f"Iron supplement use: {format_percent(table1_results['supplement_prevalence'], table1_results['supplement_se'])}")
    
    # Calculate IDWA by demographics (Table 2)
    print("\n" + "=" * 70)
    print("Calculating Table 2: IDWA prevalence by demographics...")
    print("=" * 70)
    
    df_idwa = calculate_idwa_by_demographics(df)
    print(df_idwa[['group', 'subgroup', 'n_total', 'n_idwa', 'idwa_pct']].to_string(index=False))
    
    # Generate LaTeX tables
    print("\n" + "=" * 70)
    print("Generating LaTeX tables...")
    print("=" * 70)
    
    # Table 1
    table1_latex = generate_table1_latex(table1_results)
    table1_file = os.path.join(TABLES_DIR, 'table1_characteristics.tex')
    with open(table1_file, 'w') as f:
        f.write(table1_latex)
    print(f"Saved Table 1 to: {table1_file}")
    
    # Table 2
    table2_latex = generate_table2_latex(df_idwa)
    table2_file = os.path.join(TABLES_DIR, 'table2_idwa_by_demographics.tex')
    with open(table2_file, 'w') as f:
        f.write(table2_latex)
    print(f"Saved Table 2 to: {table2_file}")
    
    # Save CSVs for reference
    table1_df = pd.DataFrame([table1_results])
    table1_csv = os.path.join(TABLES_DIR, 'table1_characteristics.csv')
    table1_df.to_csv(table1_csv, index=False)
    print(f"Saved Table 1 CSV to: {table1_csv}")
    
    table2_csv = os.path.join(TABLES_DIR, 'table2_idwa_by_demographics.csv')
    df_idwa.to_csv(table2_csv, index=False)
    print(f"Saved Table 2 CSV to: {table2_csv}")
    
    print("\n" + "=" * 70)
    print("Descriptive statistics complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()
