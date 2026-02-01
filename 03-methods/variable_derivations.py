#!/usr/bin/env python3
"""
NHANES Iron Deficiency Without Anemia (IDWA) Study
Variable Derivation Script

This script contains all functions necessary to derive study variables
from NHANES 2005-2022 data for the IDWA in women study.

Author: Elwood Research
Date: 2026-01-31
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import warnings

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_nhanes_dataset(prefix: str, cycle: str, data_dir: str = "Processed Data/Data") -> pd.DataFrame:
    """
    Load a specific NHANES dataset for a given cycle.
    
    Parameters:
    -----------
    prefix : str
        Dataset prefix (e.g., 'FERTIN', 'CBC', 'DEMO')
    cycle : str
        Cycle letter (e.g., 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'L')
    data_dir : str
        Path to processed data directory
        
    Returns:
    --------
    pd.DataFrame
        Loaded NHANES dataset
    """
    file_path = f"{data_dir}/{prefix}_{cycle}.csv"
    try:
        df = pd.read_csv(file_path)
        # Add cycle identifier
        df['cycle'] = cycle
        return df
    except FileNotFoundError:
        warnings.warn(f"File not found: {file_path}")
        return pd.DataFrame()


def load_all_cycles(prefix: str, cycles: List[str], data_dir: str = "Processed Data/Data") -> pd.DataFrame:
    """
    Load and concatenate a dataset across multiple NHANES cycles.
    
    Parameters:
    -----------
    prefix : str
        Dataset prefix
    cycles : List[str]
        List of cycle letters to load
    data_dir : str
        Path to processed data directory
        
    Returns:
    --------
    pd.DataFrame
        Concatenated dataset across all specified cycles
    """
    dfs = []
    for cycle in cycles:
        df = load_nhanes_dataset(prefix, cycle, data_dir)
        if not df.empty:
            dfs.append(df)
    
    if dfs:
        return pd.concat(dfs, ignore_index=True)
    else:
        return pd.DataFrame()


def load_all_study_datasets(cycles: List[str], data_dir: str = "Processed Data/Data") -> Dict[str, pd.DataFrame]:
    """
    Load all datasets required for the IDWA study.
    
    Parameters:
    -----------
    cycles : List[str]
        List of NHANES cycles to include
    data_dir : str
        Path to processed data directory
        
    Returns:
    --------
    Dict[str, pd.DataFrame]
        Dictionary of loaded datasets
    """
    datasets = {}
    
    # Core datasets
    print("Loading DEMO (Demographics)...")
    datasets['demo'] = load_all_cycles('DEMO', cycles, data_dir)
    
    print("Loading CBC (Complete Blood Count)...")
    datasets['cbc'] = load_all_cycles('CBC', cycles, data_dir)
    
    print("Loading FERTIN (Ferritin)...")
    datasets['fertin'] = load_all_cycles('FERTIN', cycles, data_dir)
    
    print("Loading FETIB (Iron/TIBC)...")
    datasets['fetib'] = load_all_cycles('FETIB', cycles, data_dir)
    
    print("Loading DSQTOT (Supplements - main cycles)...")
    # DSQTOT available from E onward; D uses DSQ1/DSQ2
    dsq_cycles = [c for c in cycles if c in ['E', 'F', 'G', 'H', 'I', 'J', 'L']]
    if dsq_cycles:
        datasets['dsqtot'] = load_all_cycles('DSQTOT', dsq_cycles, data_dir)
    
    print("Loading DSQ1/DSQ2 (Supplements - cycle D)...")
    if 'D' in cycles:
        datasets['dsq1'] = load_nhanes_dataset('DSQ1', 'D', data_dir)
        datasets['dsq2'] = load_nhanes_dataset('DSQ2', 'D', data_dir)
    
    print("Loading BMX (Body Measurements)...")
    datasets['bmx'] = load_all_cycles('BMX', cycles, data_dir)
    
    print("Loading FASTQX (Fasting Questionnaire)...")
    datasets['fastqx'] = load_all_cycles('FASTQX', cycles, data_dir)
    
    print("Loading DSBI (Supplement Database)...")
    datasets['dsbi'] = load_nhanes_dataset('DSBI', '', data_dir)
    
    return datasets


# ============================================================================
# IDWA STATUS DERIVATION
# ============================================================================

def derive_idwa_status(df: pd.DataFrame, 
                       ferritin_col: str = 'LBXFER',
                       hemoglobin_col: str = 'LBXHGB',
                       ferritin_threshold: float = 15.0,
                       hemoglobin_threshold: float = 12.0) -> pd.DataFrame:
    """
    Derive Iron Deficiency Without Anemia (IDWA) status.
    
    IDWA Definition:
    - Ferritin < 15 ng/mL (iron deficient)
    - Hemoglobin >= 12.0 g/dL (not anemic)
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame containing ferritin and hemoglobin columns
    ferritin_col : str
        Column name for ferritin (ng/mL)
    hemoglobin_col : str
        Column name for hemoglobin (g/dL)
    ferritin_threshold : float
        Threshold for iron deficiency (default: 15.0 ng/mL)
    hemoglobin_threshold : float
        Threshold for anemia (default: 12.0 g/dL)
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with added IDWA status columns
    """
    df = df.copy()
    
    # Handle below detection limit (flag = 2 means below LLOD)
    if 'LBDFER' in df.columns:
        # If ferritin is below detection, assign LLOD/√2
        llod = 0.5  # Standard LLOD for ferritin
        df[ferritin_col] = np.where(
            df['LBDFER'] == 1,  # 1 = below LLOD
            llod / np.sqrt(2),
            df[ferritin_col]
        )
    
    # Create iron deficiency indicator
    df['iron_deficient'] = np.where(
        df[ferritin_col].notna(),
        (df[ferritin_col] < ferritin_threshold).astype(int),
        np.nan
    )
    
    # Create anemia indicator
    df['anemic'] = np.where(
        df[hemoglobin_col].notna(),
        (df[hemoglobin_col] < hemoglobin_threshold).astype(int),
        np.nan
    )
    
    # Create IDWA status
    conditions = [
        (df[ferritin_col].isna()) | (df[hemoglobin_col].isna()),  # Missing data
        (df['iron_deficient'] == 1) & (df['anemic'] == 0),         # IDWA
        (df['iron_deficient'] == 0) & (df['anemic'] == 0),         # Iron sufficient, not anemic
        (df['anemic'] == 1)                                         # Anemic (any iron status)
    ]
    
    choices = [
        np.nan,   # Missing
        1,        # IDWA
        0,        # Iron sufficient control
        2         # Anemic (excluded)
    ]
    
    df['idwa_status'] = np.select(conditions, choices, default=np.nan)
    
    # Create binary IDWA indicator (for primary analysis)
    df['idwa'] = np.where(df['idwa_status'] == 1, 1, 
                         np.where(df['idwa_status'] == 0, 0, np.nan))
    
    return df


def derive_iron_status_categories(df: pd.DataFrame,
                                  ferritin_col: str = 'LBXFER',
                                  hemoglobin_col: str = 'LBXHGB',
                                  tsat_col: str = 'LBXSTR') -> pd.DataFrame:
    """
    Derive detailed iron status categories (4 categories).
    
    Categories:
    1. Iron sufficient, not anemic (ferritin >=15, Hb >=12)
    2. Iron deficiency without anemia (ferritin <15, Hb >=12) - IDWA
    3. Iron deficiency with anemia (ferritin <15, Hb <12) - IDA
    4. Anemia without iron deficiency (ferritin >=15, Hb <12) - non-IDA anemia
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame containing iron biomarkers
    ferritin_col : str
        Ferritin column name
    hemoglobin_col : str
        Hemoglobin column name
    tsat_col : str
        Transferrin saturation column name (optional)
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with iron status category columns
    """
    df = df.copy()
    
    # Define thresholds
    FERRITIN_ID = 15.0
    HGB_ANEMIA = 12.0
    
    # Create category labels
    categories = {
        0: 'Iron sufficient',
        1: 'IDWA (Iron deficiency without anemia)',
        2: 'IDA (Iron deficiency anemia)',
        3: 'Non-iron deficiency anemia'
    }
    
    # Derive categories
    conditions = [
        (df[ferritin_col].isna()) | (df[hemoglobin_col].isna()),
        (df[ferritin_col] >= FERRITIN_ID) & (df[hemoglobin_col] >= HGB_ANEMIA),
        (df[ferritin_col] < FERRITIN_ID) & (df[hemoglobin_col] >= HGB_ANEMIA),
        (df[ferritin_col] < FERRITIN_ID) & (df[hemoglobin_col] < HGB_ANEMIA),
        (df[ferritin_col] >= FERRITIN_ID) & (df[hemoglobin_col] < HGB_ANEMIA)
    ]
    
    choices = [np.nan, 0, 1, 2, 3]
    
    df['iron_status_cat'] = np.select(conditions, choices, default=np.nan)
    df['iron_status_label'] = df['iron_status_cat'].map(categories)
    
    # Add transferrin saturation criteria if available
    if tsat_col in df.columns:
        df['tsat_low'] = np.where(
            df[tsat_col].notna(),
            (df[tsat_col] < 20.0).astype(int),
            np.nan
        )
    
    return df


# ============================================================================
# SUPPLEMENT DERIVATION
# ============================================================================

def identify_iron_supplements(dsqtot_df: pd.DataFrame, 
                               dsbi_df: pd.DataFrame) -> pd.DataFrame:
    """
    Identify iron-containing supplements from DSQTOT data.
    
    Uses the NHANES-DSD database (DSBI) to identify products containing iron.
    
    Parameters:
    -----------
    dsqtot_df : pd.DataFrame
        DSQTOT dataset with supplement use information
    dsbi_df : pd.DataFrame
        DSBI dataset with supplement product database
        
    Returns:
    --------
    pd.DataFrame
        DSQTOT data with iron supplement indicators added
    """
    df = dsqtot_df.copy()
    
    # Common iron supplement codes (DSDSUPP) - these are examples
    # In practice, would cross-reference with full DSBI database
    iron_supplement_codes = [
        # Prenatal vitamins with iron
        '618020', '618030', '618040', '618050',
        # Iron supplements
        '624010', '624020', '624030', '624040',
        # Multivitamins with iron
        '611010', '611020', '611030',
        # Additional codes would be added based on DSBI database
    ]
    
    # Iron-containing keywords in product names
    iron_keywords = [
        'iron', 'ferrous', 'ferric', 'ferrite', 
        'prenatal', 'prenatal vitamin'
    ]
    
    # Identify iron supplements by code
    df['iron_by_code'] = df['DSDSUPP'].isin(iron_supplement_codes).astype(int)
    
    # Identify by matching to DSBI database
    if 'DSDSUPP' in df.columns and dsbi_df is not None:
        # Merge with DSBI to get product details
        dsbi_iron = dsbi_df[dsbi_df['ingredient_name'].str.contains('iron', case=False, na=False)]
        iron_codes_from_dsbi = dsbi_iron['supplement_code'].unique()
        df['iron_by_dsbi'] = df['DSDSUPP'].isin(iron_codes_from_dsbi).astype(int)
    
    # Combined indicator
    df['is_iron_supplement'] = np.where(
        (df.get('iron_by_code', 0) == 1) | (df.get('iron_by_dsbi', 0) == 1),
        1, 0
    )
    
    return df


def calculate_iron_dose(supp_df: pd.DataFrame, dsbi_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate daily elemental iron dose from supplement data.
    
    Parameters:
    -----------
    supp_df : pd.DataFrame
        Supplement data (DSQTOT format)
    dsbi_df : pd.DataFrame
        DSBI product database with iron content
        
    Returns:
    --------
    pd.DataFrame
        Supplement data with calculated iron dose
    """
    df = supp_df.copy()
    
    # Merge with DSBI to get iron content per serving
    if dsbi_df is not None and 'DSDSUPP' in df.columns:
        dsbi_iron = dsbi_df[dsbi_df['ingredient_name'].str.contains('iron', case=False, na=False)]
        dsbi_iron = dsbi_iron.groupby('supplement_code')['amount_per_serving'].max().reset_index()
        dsbi_iron.columns = ['DSDSUPP', 'iron_per_serving_mg']
        
        df = df.merge(dsbi_iron, on='DSDSUPP', how='left')
    
    # Calculate daily dose
    # DSDQTY = quantity consumed per day
    # DSDSRVY = days supplement taken per month
    df['daily_iron_dose'] = np.where(
        (df['is_iron_supplement'] == 1) & (df['iron_per_serving_mg'].notna()),
        df['DSDQTY'] * df['iron_per_serving_mg'] * (df['DSDSRVY'] / 30),
        0
    )
    
    return df


def derive_supplement_categories(df: pd.DataFrame, 
                                  daily_dose_col: str = 'daily_iron_dose') -> pd.DataFrame:
    """
    Categorize iron supplement users by daily dose.
    
    Categories:
    - 0: Non-user (0 mg/day)
    - 1: Low dose (<18 mg/day)
    - 2: Moderate dose (18-65 mg/day)
    - 3: High dose (>65 mg/day)
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with daily iron dose
    daily_dose_col : str
        Column containing daily iron dose in mg
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with supplement categories added
    """
    df = df.copy()
    
    # Define dose categories
    conditions = [
        df[daily_dose_col] == 0,
        (df[daily_dose_col] > 0) & (df[daily_dose_col] < 18),
        (df[daily_dose_col] >= 18) & (df[daily_dose_col] <= 65),
        df[daily_dose_col] > 65
    ]
    
    choices = [0, 1, 2, 3]
    
    df['iron_dose_cat'] = np.select(conditions, choices, default=0)
    
    # Create labels
    labels = {
        0: 'Non-user',
        1: 'Low dose (<18 mg)',
        2: 'Moderate dose (18-65 mg)',
        3: 'High dose (>65 mg)'
    }
    df['iron_dose_label'] = df['iron_dose_cat'].map(labels)
    
    # Binary user indicator
    df['iron_supplement_user'] = (df['iron_dose_cat'] > 0).astype(int)
    
    return df


def aggregate_supplements_by_person(dsqtot_df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate supplement data to person-level.
    
    Some participants take multiple supplements; this sums total iron intake.
    
    Parameters:
    -----------
    dsqtot_df : pd.DataFrame
        DSQTOT data with iron dose calculated
        
    Returns:
    --------
    pd.DataFrame
        Person-level supplement summary
    """
    # Group by SEQN and sum iron doses
    person_summary = dsqtot_df.groupby('SEQN').agg({
        'daily_iron_dose': 'sum',
        'is_iron_supplement': 'max',  # 1 if any iron supplement
        'DSDSRVY': 'max'  # Days per month
    }).reset_index()
    
    # Rename columns
    person_summary.columns = [
        'SEQN', 'total_daily_iron_dose', 'any_iron_supplement', 'max_days_per_month'
    ]
    
    # Categorize total dose
    person_summary = derive_supplement_categories(
        person_summary, 
        daily_dose_col='total_daily_iron_dose'
    )
    
    return person_summary


# ============================================================================
# ANEMIA STATUS DEFINITION
# ============================================================================

def derive_anemia_status(df: pd.DataFrame,
                         hemoglobin_col: str = 'LBXHGB',
                         mcv_col: str = 'LBXMCV',
                         pregnancy_col: str = 'RIDEXPRG') -> pd.DataFrame:
    """
    Derive comprehensive anemia status with morphological classification.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with CBC data
    hemoglobin_col : str
        Hemoglobin column
    mcv_col : str
        MCV column
    pregnancy_col : str
        Pregnancy status column
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with anemia status columns
    """
    df = df.copy()
    
    # WHO Hemoglobin thresholds
    # Non-pregnant women: <12.0 g/dL
    # Pregnant women: <11.0 g/dL
    
    # Determine anemia threshold based on pregnancy status
    anemia_threshold = np.where(
        df[pregnancy_col] == 1,  # Pregnant
        11.0,
        12.0
    )
    
    # Anemia indicator
    df['anemic'] = np.where(
        df[hemoglobin_col].notna(),
        (df[hemoglobin_col] < anemia_threshold).astype(int),
        np.nan
    )
    
    # Anemia severity (WHO criteria for non-pregnant women)
    conditions = [
        df[hemoglobin_col].isna(),
        df[hemoglobin_col] >= 12.0,
        (df[hemoglobin_col] >= 11.0) & (df[hemoglobin_col] < 12.0),
        (df[hemoglobin_col] >= 8.0) & (df[hemoglobin_col] < 11.0),
        df[hemoglobin_col] < 8.0
    ]
    
    choices = [
        np.nan,     # Missing
        0,          # Not anemic
        1,          # Mild (11-11.9)
        2,          # Moderate (8-10.9)
        3           # Severe (<8)
    ]
    
    df['anemia_severity'] = np.select(conditions, choices, default=np.nan)
    
    # Anemia morphology (if MCV available)
    if mcv_col in df.columns:
        morph_conditions = [
            df[mcv_col].isna(),
            df[mcv_col] < 80,
            (df[mcv_col] >= 80) & (df[mcv_col] <= 100),
            df[mcv_col] > 100
        ]
        
        morph_choices = [np.nan, 1, 2, 3]
        df['mcv_category'] = np.select(morph_conditions, morph_choices, default=np.nan)
        
        mcv_labels = {1: 'Microcytic', 2: 'Normocytic', 3: 'Macrocytic'}
        df['mcv_label'] = df['mcv_category'].map(mcv_labels)
    
    return df


# ============================================================================
# DEMOGRAPHIC VARIABLE RECODING
# ============================================================================

def recode_demographics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Recode demographic variables for analysis.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with DEMO variables
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with recoded demographic variables
    """
    df = df.copy()
    
    # Age categories
    age_bins = [0, 18, 25, 35, 45, 100]
    age_labels = ['<18', '18-25', '26-35', '36-45', '>45']
    df['age_cat'] = pd.cut(df['RIDAGEYR'], bins=age_bins, labels=age_labels, right=False)
    
    # Study age indicator (18-45)
    df['age_study'] = ((df['RIDAGEYR'] >= 18) & (df['RIDAGEYR'] <= 45)).astype(int)
    
    # Race/ethnicity recoding
    race_map = {
        1: 'Mexican American',
        2: 'Other Hispanic',
        3: 'Non-Hispanic White',
        4: 'Non-Hispanic Black',
        5: 'Other Race'
    }
    df['race_ethnicity'] = df['RIDRETH1'].map(race_map)
    
    # Simplified race categories
    race_simple_map = {
        1: 'Hispanic',
        2: 'Hispanic',
        3: 'Non-Hispanic White',
        4: 'Non-Hispanic Black',
        5: 'Other'
    }
    df['race_simple'] = df['RIDRETH1'].map(race_simple_map)
    
    # Education categories
    edu_map = {
        1: 'Less than 9th grade',
        2: '9-11th grade',
        3: 'High school graduate',
        4: 'Some college',
        5: 'College graduate or above'
    }
    df['education'] = df['DMDEDUC2'].map(edu_map)
    
    # Poverty Income Ratio categories
    pir_bins = [0, 1.0, 2.0, 4.0, 999]
    pir_labels = ['<100% FPL', '100-199% FPL', '200-399% FPL', '≥400% FPL']
    df['pir_cat'] = pd.cut(df['INDFMPIR'], bins=pir_bins, labels=pir_labels)
    
    # Poverty indicator
    df['below_poverty'] = (df['INDFMPIR'] < 1.0).astype(int)
    
    # Gender
    df['female'] = (df['RIAGENDR'] == 2).astype(int)
    
    # Pregnancy status recoding
    preg_map = {
        1: 'Pregnant',
        2: 'Not pregnant',
        3: 'Unknown'
    }
    df['pregnancy_status'] = df['RIDEXPRG'].map(preg_map)
    df['not_pregnant'] = (df['RIDEXPRG'] == 2).astype(int)
    
    # Survey cycle year mapping
    cycle_year_map = {
        6: '2005-2006',
        7: '2007-2008',
        8: '2009-2010',
        9: '2011-2012',
        10: '2013-2014',
        11: '2015-2016',
        12: '2017-2018',
        13: '2021-2022'
    }
    df['cycle_years'] = df['SDDSRVYR'].map(cycle_year_map)
    
    return df


# ============================================================================
# SURVEY WEIGHT ADJUSTMENT
# ============================================================================

def adjust_survey_weights(df: pd.DataFrame, 
                          n_cycles: int = 8,
                          weight_col: str = 'WTMEC2YR') -> pd.DataFrame:
    """
    Adjust survey weights for pooled cycles.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with survey weights
    n_cycles : int
        Number of cycles combined (default: 8)
    weight_col : str
        Original weight column name
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with adjusted weights
    """
    df = df.copy()
    
    # Adjust weights
    df['WTMEC2YR_adj'] = df[weight_col] / n_cycles
    
    # Verify weights sum to population size
    pop_estimate = df['WTMEC2YR_adj'].sum()
    print(f"Weighted population estimate: {pop_estimate:,.0f}")
    
    # Flag extreme weights (>3 SD from mean)
    weight_mean = df['WTMEC2YR_adj'].mean()
    weight_std = df['WTMEC2YR_adj'].std()
    df['extreme_weight'] = (
        (df['WTMEC2YR_adj'] > weight_mean + 3*weight_std) |
        (df['WTMEC2YR_adj'] < weight_mean - 3*weight_std)
    ).astype(int)
    
    n_extreme = df['extreme_weight'].sum()
    if n_extreme > 0:
        print(f"Warning: {n_extreme} cases with extreme weights identified")
    
    return df


def create_survey_design_spec(df: pd.DataFrame) -> Dict:
    """
    Create survey design specification for statistical analysis.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Analysis dataset with survey design variables
        
    Returns:
    --------
    Dict
        Survey design specification
    """
    design = {
        'strata': 'SDMVSTRA',
        'psu': 'SDMVPSU',
        'weight': 'WTMEC2YR_adj',
        'nest': True  # PSUs are nested within strata
    }
    
    # Verify design variables exist
    for var in ['strata', 'psu', 'weight']:
        if design[var] not in df.columns:
            warnings.warn(f"Survey design variable {design[var]} not found in data")
    
    return design


# ============================================================================
# COMPLETE VARIABLE DERIVATION PIPELINE
# ============================================================================

def derive_all_study_variables(datasets: Dict[str, pd.DataFrame],
                                cycles: List[str]) -> pd.DataFrame:
    """
    Execute complete variable derivation pipeline.
    
    This is the main function that orchestrates all derivations.
    
    Parameters:
    -----------
    datasets : Dict[str, pd.DataFrame]
        Dictionary of loaded NHANES datasets
    cycles : List[str]
        List of cycles included
        
    Returns:
    --------
    pd.DataFrame
        Fully processed analysis dataset
    """
    print("=" * 60)
    print("NHANES IDWA Study - Variable Derivation Pipeline")
    print("=" * 60)
    
    # Step 1: Merge core datasets
    print("\nStep 1: Merging core datasets...")
    base = datasets['demo'].copy()
    
    # Merge CBC
    if 'cbc' in datasets:
        base = base.merge(datasets['cbc'], on='SEQN', how='left', suffixes=('', '_cbc'))
        print(f"  - CBC merged: {len(base)} records")
    
    # Merge FERTIN (ferritin)
    if 'fertin' in datasets:
        base = base.merge(datasets['fertin'], on='SEQN', how='left', suffixes=('', '_fertin'))
        print(f"  - FERTIN merged: {len(base)} records")
    
    # Merge FETIB (iron/TIBC) - limited cycles
    if 'fetib' in datasets and not datasets['fetib'].empty:
        base = base.merge(datasets['fetib'], on='SEQN', how='left', suffixes=('', '_fetib'))
        print(f"  - FETIB merged: {len(base)} records")
    
    # Merge BMX
    if 'bmx' in datasets:
        base = base.merge(datasets['bmx'], on='SEQN', how='left', suffixes=('', '_bmx'))
        print(f"  - BMX merged: {len(base)} records")
    
    # Merge FASTQX
    if 'fastqx' in datasets:
        base = base.merge(datasets['fastqx'], on='SEQN', how='left', suffixes=('', '_fastqx'))
        print(f"  - FASTQX merged: {len(base)} records")
    
    # Step 2: Process supplement data
    print("\nStep 2: Processing supplement data...")
    
    supp_data = []
    
    # Process DSQTOT cycles
    if 'dsqtot' in datasets and not datasets['dsqtot'].empty:
        dsqtot = identify_iron_supplements(datasets['dsqtot'], datasets.get('dsbi'))
        dsqtot = calculate_iron_dose(dsqtot, datasets.get('dsbi'))
        supp_data.append(dsqtot)
    
    # Process cycle D supplements (DSQ1/DSQ2)
    if 'dsq1' in datasets:
        dsq1 = identify_iron_supplements(datasets['dsq1'], datasets.get('dsbi'))
        dsq1 = calculate_iron_dose(dsq1, datasets.get('dsbi'))
        supp_data.append(dsq1)
    
    if 'dsq2' in datasets:
        dsq2 = identify_iron_supplements(datasets['dsq2'], datasets.get('dsbi'))
        dsq2 = calculate_iron_dose(dsq2, datasets.get('dsbi'))
        supp_data.append(dsq2)
    
    if supp_data:
        all_supp = pd.concat(supp_data, ignore_index=True)
        person_supp = aggregate_supplements_by_person(all_supp)
        base = base.merge(person_supp, on='SEQN', how='left')
        print(f"  - Supplement data merged: {person_supp['iron_supplement_user'].sum()} users")
    else:
        # Create empty supplement columns
        base['total_daily_iron_dose'] = 0
        base['iron_supplement_user'] = 0
        base['iron_dose_cat'] = 0
        print("  - No supplement data available")
    
    # Step 3: Derive IDWA status
    print("\nStep 3: Deriving IDWA status...")
    base = derive_idwa_status(base)
    base = derive_iron_status_categories(base)
    print(f"  - IDWA cases: {base['idwa'].sum():.0f}")
    print(f"  - Iron sufficient controls: {(base['idwa'] == 0).sum():.0f}")
    
    # Step 4: Derive anemia status
    print("\nStep 4: Deriving anemia status...")
    base = derive_anemia_status(base)
    
    # Step 5: Recode demographics
    print("\nStep 5: Recoding demographic variables...")
    base = recode_demographics(base)
    
    # Step 6: Adjust survey weights
    print("\nStep 6: Adjusting survey weights...")
    base = adjust_survey_weights(base, n_cycles=len(cycles))
    
    # Step 7: Apply inclusion criteria
    print("\nStep 7: Applying inclusion criteria...")
    
    # Create study inclusion flag
    inclusion_conditions = (
        (base['female'] == 1) &                           # Female
        (base['age_study'] == 1) &                        # Age 18-45
        (base['not_pregnant'] == 1) &                     # Not pregnant
        (base['WTMEC2YR_adj'].notna()) &                  # Has weight
        (base['WTMEC2YR_adj'] > 0) &                      # Valid weight
        (base['LBXHGB'].notna())                          # Has hemoglobin
    )
    
    base['study_eligible'] = inclusion_conditions.astype(int)
    
    # Create analytic sample flag (non-anemic with ferritin)
    analytic_conditions = (
        (base['study_eligible'] == 1) &
        (base['anemic'] == 0) &                           # Not anemic
        (base['LBXFER'].notna())                          # Has ferritin
    )
    
    base['analytic_sample'] = analytic_conditions.astype(int)
    
    print(f"  - Study eligible: {base['study_eligible'].sum():.0f}")
    print(f"  - Analytic sample: {base['analytic_sample'].sum():.0f}")
    
    # Step 8: Create derived biomarker variables
    print("\nStep 8: Creating derived biomarkers...")
    
    # Log-transform ferritin
    base['log_ferritin'] = np.where(
        base['LBXFER'].notna() & (base['LBXFER'] > 0),
        np.log(base['LBXFER']),
        np.nan
    )
    
    # Calculate BMI if not available
    if 'BMXBMI' not in base.columns or base['BMXBMI'].isna().all():
        if 'BMXWT' in base.columns and 'BMXHT' in base.columns:
            base['BMXBMI'] = base['BMXWT'] / ((base['BMXHT'] / 100) ** 2)
    
    # BMI categories
    bmi_bins = [0, 18.5, 25, 30, 100]
    bmi_labels = ['Underweight', 'Normal', 'Overweight', 'Obese']
    base['bmi_cat'] = pd.cut(base['BMXBMI'], bins=bmi_bins, labels=bmi_labels)
    
    # Fasting time (hours)
    if 'PHAFSTHR' in base.columns:
        base['fasting_hours'] = base['PHAFSTHR'] + base.get('PHAFSTMN', 0) / 60
    
    print("\n" + "=" * 60)
    print("Variable derivation complete!")
    print(f"Final dataset: {len(base)} records")
    print(f"Analytic sample: {base['analytic_sample'].sum():.0f}")
    print("=" * 60)
    
    return base


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Define study cycles
    STUDY_CYCLES = ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'L']
    
    # Load all datasets
    print("Loading NHANES datasets...")
    datasets = load_all_study_datasets(STUDY_CYCLES)
    
    # Run derivation pipeline
    analysis_data = derive_all_study_variables(datasets, STUDY_CYCLES)
    
    # Export processed data
    output_path = "studies/iron-deficiency-women-2026-01-31/04-analysis/processed_data.csv"
    analysis_data.to_csv(output_path, index=False)
    print(f"\nProcessed data saved to: {output_path}")
    
    # Create survey design specification
    design_spec = create_survey_design_spec(analysis_data)
    print("\nSurvey design specification:")
    for key, value in design_spec.items():
        print(f"  {key}: {value}")
