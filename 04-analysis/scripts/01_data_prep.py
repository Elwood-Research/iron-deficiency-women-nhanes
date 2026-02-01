#!/usr/bin/env python3
"""
NHANES Iron Deficiency Without Anemia Study - Data Preparation Script
====================================================================

This script:
1. Loads all NHANES datasets from the specified cycles
2. Merges datasets by SEQN
3. Applies inclusion/exclusion criteria
4. Creates IDWA status variable
5. Handles below-detection ferritin values
6. Adjusts survey weights for pooled cycles
7. Saves processed dataset

Author: NHANES Analysis Pipeline
Date: 2026-01-31
"""

import pandas as pd
import numpy as np
import os
import sys

# Set random seed for reproducibility
np.random.seed(42)

# Data paths
DATA_DIR = "Processed Data/Data"
OUTPUT_DIR = "studies/iron-deficiency-women-2026-01-31/04-analysis"

# Study parameters
CYCLES = {
    'D': '2005-2006',
    'E': '2007-2008', 
    'F': '2009-2010',
    'G': '2011-2012',
    'H': '2013-2014',
    'I': '2015-2016',
    'J': '2017-2018',
    'L': '2021-2022'
}

# Number of cycles for weight adjustment
N_CYCLES = 8

def load_dataset(prefix, cycle):
    """Load a single NHANES dataset file."""
    filename = f"{prefix}_{cycle}.csv"
    filepath = os.path.join(DATA_DIR, filename)
    
    if not os.path.exists(filepath):
        print(f"Warning: {filepath} not found, skipping...")
        return None
    
    try:
        df = pd.read_csv(filepath, dtype=str)
        # Add cycle identifier
        df['cycle'] = cycle
        df['cycle_year'] = CYCLES[cycle]
        print(f"Loaded {filename}: {len(df)} rows")
        return df
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return None

def load_and_combine_datasets(prefix, cycles):
    """Load and combine datasets across multiple cycles."""
    dfs = []
    for cycle in cycles:
        df = load_dataset(prefix, cycle)
        if df is not None:
            dfs.append(df)
    
    if not dfs:
        return None
    
    combined = pd.concat(dfs, ignore_index=True)
    print(f"Combined {prefix}: {len(combined)} total rows from {len(dfs)} cycles")
    return combined

def convert_to_numeric(df, columns):
    """Convert specified columns to numeric, handling missing values."""
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def main():
    print("=" * 70)
    print("NHANES Iron Deficiency Without Anemia Study - Data Preparation")
    print("=" * 70)
    print()
    
    # Define which cycles have which datasets
    # Note: Not all datasets are available in all cycles
    demo_cycles = ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'L']
    fertin_cycles = ['D', 'E', 'F', 'I', 'J']  # G, H, L not available
    cbc_cycles = ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'L']
    dsqtot_cycles = ['E', 'F', 'G', 'H', 'I', 'J', 'L']  # D not available
    bmx_cycles = ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'L']
    fetib_cycles = ['D', 'J']  # Only available in D and J
    
    # Load datasets
    print("Loading DEMO (Demographics)...")
    demo = load_and_combine_datasets('DEMO', demo_cycles)
    
    print("\nLoading FERTIN (Ferritin)...")
    fertin = load_and_combine_datasets('FERTIN', fertin_cycles)
    
    print("\nLoading CBC (Complete Blood Count)...")
    cbc = load_and_combine_datasets('CBC', cbc_cycles)
    
    print("\nLoading DSQTOT (Dietary Supplements)...")
    dsqtot = load_and_combine_datasets('DSQTOT', dsqtot_cycles)
    
    print("\nLoading BMX (Body Measures)...")
    bmx = load_and_combine_datasets('BMX', bmx_cycles)
    
    print("\nLoading FETIB (Iron/TIBC - optional)...")
    fetib = load_and_combine_datasets('FETIB', fetib_cycles)
    
    # Check if critical datasets loaded
    if demo is None or fertin is None:
        print("\nError: Critical datasets (DEMO, FERTIN) not available!")
        sys.exit(1)
    
    # Select relevant columns
    print("\n" + "=" * 70)
    print("Selecting relevant columns...")
    print("=" * 70)
    
    # DEMO columns
    demo_cols = ['SEQN', 'cycle', 'cycle_year', 'RIAGENDR', 'RIDAGEYR', 'RIDRETH1', 
                 'INDFMPIR', 'WTMEC2YR', 'SDMVSTRA', 'SDMVPSU', 'RIDEXPRG']
    demo = demo[[col for col in demo_cols if col in demo.columns]].copy()
    
    # FERTIN columns
    fertin_cols = ['SEQN', 'LBXFER']
    fertin = fertin[[col for col in fertin_cols if col in fertin.columns]].copy()
    
    # CBC columns
    cbc_cols = ['SEQN', 'LBXHGB']
    if cbc is not None:
        cbc = cbc[[col for col in cbc_cols if col in cbc.columns]].copy()
    
    # DSQTOT columns
    dsqtot_cols = ['SEQN', 'DSQTIRON']
    if dsqtot is not None:
        dsqtot = dsqtot[[col for col in dsqtot_cols if col in dsqtot.columns]].copy()
    
    # BMX columns
    bmx_cols = ['SEQN', 'BMXBMI']
    if bmx is not None:
        bmx = bmx[[col for col in bmx_cols if col in bmx.columns]].copy()
    
    # FETIB columns (optional)
    fetib_cols = ['SEQN', 'LBXIRN', 'LBXTIB', 'LBDPCT']
    if fetib is not None:
        fetib = fetib[[col for col in fetib_cols if col in fetib.columns]].copy()
    
    # Convert to numeric
    print("\nConverting columns to numeric...")
    
    demo = convert_to_numeric(demo, ['RIAGENDR', 'RIDAGEYR', 'RIDRETH1', 'INDFMPIR', 
                                      'WTMEC2YR', 'SDMVSTRA', 'SDMVPSU', 'RIDEXPRG'])
    fertin = convert_to_numeric(fertin, ['LBXFER'])
    if cbc is not None:
        cbc = convert_to_numeric(cbc, ['LBXHGB'])
    if dsqtot is not None:
        dsqtot = convert_to_numeric(dsqtot, ['DSQTIRON'])
    if bmx is not None:
        bmx = convert_to_numeric(bmx, ['BMXBMI'])
    if fetib is not None:
        fetib = convert_to_numeric(fetib, ['LBXIRN', 'LBXTIB', 'LBDPCT'])
    
    # Merge datasets
    print("\n" + "=" * 70)
    print("Merging datasets...")
    print("=" * 70)
    
    # Start with DEMO as base
    df = demo.copy()
    print(f"DEMO base: {len(df)} rows")
    
    # Merge FERTIN (inner join - must have ferritin)
    df = df.merge(fertin, on='SEQN', how='inner')
    print(f"After FERTIN merge: {len(df)} rows")
    
    # Merge CBC (inner join - must have hemoglobin)
    if cbc is not None:
        df = df.merge(cbc, on='SEQN', how='inner')
        print(f"After CBC merge: {len(df)} rows")
    
    # Merge DSQTOT (left join - supplement data optional)
    if dsqtot is not None:
        df = df.merge(dsqtot, on='SEQN', how='left')
        print(f"After DSQTOT merge: {len(df)} rows")
    else:
        df['DSQTIRON'] = np.nan
    
    # Merge BMX (left join - BMI optional)
    if bmx is not None:
        df = df.merge(bmx, on='SEQN', how='left')
        print(f"After BMX merge: {len(df)} rows")
    else:
        df['BMXBMI'] = np.nan
    
    # Merge FETIB (left join - optional)
    if fetib is not None:
        df = df.merge(fetib, on='SEQN', how='left')
        print(f"After FETIB merge: {len(df)} rows")
    
    print(f"\nTotal merged dataset: {len(df)} rows")
    
    # Apply inclusion/exclusion criteria
    print("\n" + "=" * 70)
    print("Applying inclusion/exclusion criteria...")
    print("=" * 70)
    
    initial_n = len(df)
    print(f"Initial sample: {initial_n:,}")
    
    # Track exclusions
    exclusions = {}
    
    # Inclusion 1: Age 18-45 years
    df['age_eligible'] = (df['RIDAGEYR'] >= 18) & (df['RIDAGEYR'] <= 45)
    exclusions['age_18_45'] = initial_n - df['age_eligible'].sum()
    df = df[df['age_eligible']].copy()
    print(f"After age 18-45 inclusion: {len(df):,} (excluded {exclusions['age_18_45']:,})")
    
    # Inclusion 2: Female
    df['female'] = df['RIAGENDR'] == 2
    exclusions['female'] = len(df) - df['female'].sum()
    df = df[df['female']].copy()
    print(f"After female inclusion: {len(df):,} (excluded {exclusions['female']:,})")
    
    # Exclusion 1: Pregnant women
    # RIDEXPRG: 1 = Yes, pregnant, 2 = No, 3 = Could not be determined
    # Missing values are treated as not pregnant for conservatism, but we'll exclude definite pregnancies
    df['not_pregnant'] = (df['RIDEXPRG'] != 1) | (df['RIDEXPRG'].isna())
    exclusions['pregnant'] = len(df) - df['not_pregnant'].sum()
    df = df[df['not_pregnant']].copy()
    print(f"After excluding pregnant: {len(df):,} (excluded {exclusions['pregnant']:,})")
    
    # Exclusion 2: Missing ferritin
    df['has_ferritin'] = df['LBXFER'].notna()
    exclusions['missing_ferritin'] = len(df) - df['has_ferritin'].sum()
    df = df[df['has_ferritin']].copy()
    print(f"After excluding missing ferritin: {len(df):,} (excluded {exclusions['missing_ferritin']:,})")
    
    # Exclusion 3: Missing hemoglobin
    if 'LBXHGB' in df.columns:
        df['has_hemoglobin'] = df['LBXHGB'].notna()
        exclusions['missing_hemoglobin'] = len(df) - df['has_hemoglobin'].sum()
        df = df[df['has_hemoglobin']].copy()
        print(f"After excluding missing hemoglobin: {len(df):,} (excluded {exclusions['missing_hemoglobin']:,})")
    
    # Handle below-detection ferritin values
    # According to NHANES documentation, ferritin values below detection limit should be set to 2.0 ng/mL
    print("\n" + "=" * 70)
    print("Handling below-detection ferritin values...")
    print("=" * 70)
    
    # Check for very low or zero values (indicating below detection)
    below_detection = (df['LBXFER'] <= 0) | (df['LBXFER'].isna())
    n_below = below_detection.sum()
    
    # Set below-detection values to 2.0 ng/mL
    df.loc[below_detection, 'LBXFER'] = 2.0
    print(f"Set {n_below:,} below-detection ferritin values to 2.0 ng/mL")
    
    # Also set any ferritin < 2 to 2.0 (conservative approach)
    very_low = df['LBXFER'] < 2.0
    n_very_low = very_low.sum()
    df.loc[very_low, 'LBXFER'] = 2.0
    print(f"Set {n_very_low:,} very low ferritin values to 2.0 ng/mL")
    
    # Create IDWA status variable
    print("\n" + "=" * 70)
    print("Creating IDWA status variable...")
    print("=" * 70)
    
    # IDWA Definition: Ferritin <15 ng/mL AND Hemoglobin ≥12 g/dL
    df['iron_deficient'] = df['LBXFER'] < 15.0
    df['not_anemic'] = df['LBXHGB'] >= 12.0
    df['IDWA'] = df['iron_deficient'] & df['not_anemic']
    
    n_idwa = df['IDWA'].sum()
    n_iron_def = df['iron_deficient'].sum()
    n_anemic = (~df['not_anemic']).sum()
    
    print(f"Iron deficient (ferritin <15): {n_iron_def:,} ({100*n_iron_def/len(df):.1f}%)")
    print(f"Anemic (hemoglobin <12): {n_anemic:,} ({100*n_anemic/len(df):.1f}%)")
    print(f"IDWA cases: {n_idwa:,} ({100*n_idwa/len(df):.1f}%)")
    
    # Create iron supplement use variable
    print("\n" + "=" * 70)
    print("Creating iron supplement use variable...")
    print("=" * 70)
    
    # DSQTIRON > 0 indicates iron supplement use
    df['iron_supplement'] = (df['DSQTIRON'] > 0) & (df['DSQTIRON'].notna())
    df['iron_supplement'] = df['iron_supplement'].astype(int)
    
    # Create dose categories
    df['iron_dose'] = 'None'
    df.loc[df['DSQTIRON'] > 0, 'iron_dose'] = 'Low'
    df.loc[df['DSQTIRON'] >= 18, 'iron_dose'] = 'Moderate'  # ~100% RDA
    df.loc[df['DSQTIRON'] >= 27, 'iron_dose'] = 'High'  # Pregnancy RDA level
    
    n_supp = df['iron_supplement'].sum()
    print(f"Iron supplement users: {n_supp:,} ({100*n_supp/len(df):.1f}%)")
    print(f"Iron dose distribution:")
    print(df['iron_dose'].value_counts())
    
    # Create log-transformed ferritin
    df['log_ferritin'] = np.log(df['LBXFER'])
    
    # Adjust survey weights for pooled cycles
    print("\n" + "=" * 70)
    print("Adjusting survey weights for pooled cycles...")
    print("=" * 70)
    
    # Weight adjustment: WTMEC2YR / N_CYCLES (8 cycles)
    df['weight_adjusted'] = df['WTMEC2YR'] / N_CYCLES
    print(f"Adjusted weights: WTMEC2YR / {N_CYCLES}")
    print(f"Weight statistics:")
    print(df['weight_adjusted'].describe())
    
    # Create race/ethnicity categories
    print("\n" + "=" * 70)
    print("Creating race/ethnicity categories...")
    print("=" * 70)
    
    # RIDRETH1 coding:
    # 1 = Mexican American
    # 2 = Other Hispanic
    # 3 = Non-Hispanic White
    # 4 = Non-Hispanic Black
    # 5 = Other Race
    race_mapping = {
        1: 'Mexican American',
        2: 'Other Hispanic',
        3: 'Non-Hispanic White',
        4: 'Non-Hispanic Black',
        5: 'Other Race'
    }
    df['race_category'] = df['RIDRETH1'].map(race_mapping)
    df['race_category'] = df['race_category'].fillna('Unknown')
    print(df['race_category'].value_counts())
    
    # Create age groups
    print("\n" + "=" * 70)
    print("Creating age groups...")
    print("=" * 70)
    
    df['age_group'] = pd.cut(df['RIDAGEYR'], 
                              bins=[17, 25, 30, 35, 40, 45],
                              labels=['18-25', '26-30', '31-35', '36-40', '41-45'],
                              include_lowest=True)
    print(df['age_group'].value_counts().sort_index())
    
    # Create poverty category
    print("\n" + "=" * 70)
    print("Creating poverty categories...")
    print("=" * 70)
    
    # INDFMPIR: Family income to poverty ratio
    df['poverty_category'] = 'Unknown'
    df.loc[df['INDFMPIR'] < 1.3, 'poverty_category'] = 'Low (<1.3)'
    df.loc[(df['INDFMPIR'] >= 1.3) & (df['INDFMPIR'] < 3.5), 'poverty_category'] = 'Medium (1.3-3.5)'
    df.loc[df['INDFMPIR'] >= 3.5, 'poverty_category'] = 'High (≥3.5)'
    print(df['poverty_category'].value_counts())
    
    # Final dataset summary
    print("\n" + "=" * 70)
    print("Final Dataset Summary")
    print("=" * 70)
    print(f"Total eligible women (non-pregnant, 18-45): {len(df):,}")
    print(f"Cycles included: {df['cycle'].unique()}")
    print(f"IDWA cases: {df['IDWA'].sum():,} ({100*df['IDWA'].sum()/len(df):.1f}%)")
    print(f"Iron supplement users: {df['iron_supplement'].sum():,} ({100*df['iron_supplement'].sum()/len(df):.1f}%)")
    
    # Print exclusion summary
    print("\n" + "=" * 70)
    print("Exclusion Summary")
    print("=" * 70)
    for reason, count in exclusions.items():
        print(f"{reason}: {count:,}")
    
    # Save processed dataset
    output_file = os.path.join(OUTPUT_DIR, 'processed_data.csv')
    df.to_csv(output_file, index=False)
    print(f"\nSaved processed dataset to: {output_file}")
    print(f"Dataset shape: {df.shape}")
    
    # Save exclusion summary
    exclusion_df = pd.DataFrame(list(exclusions.items()), columns=['exclusion_reason', 'count'])
    exclusion_df.to_csv(os.path.join(OUTPUT_DIR, 'exclusions.csv'), index=False)
    
    print("\n" + "=" * 70)
    print("Data preparation complete!")
    print("=" * 70)
    
    return df

if __name__ == "__main__":
    main()
