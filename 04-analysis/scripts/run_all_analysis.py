#!/usr/bin/env python3
"""
NHANES Iron Deficiency Without Anemia Study - Master Analysis Script
====================================================================

This script runs the complete analysis pipeline:
1. Data preparation (01_data_prep.py)
2. Descriptive statistics (02_descriptive_stats.py)
3. Regression analysis (03_regression_analysis.py)
4. Figure generation (04_generate_figures.py)

Author: NHANES Analysis Pipeline
Date: 2026-01-31
"""

import subprocess
import sys
import os

OUTPUT_DIR = "studies/iron-deficiency-women-2026-01-31/04-analysis"

def run_script(script_name):
    """Run a Python script and capture output."""
    script_path = os.path.join(OUTPUT_DIR, "scripts", script_name)
    
    print(f"\n{'='*70}")
    print(f"Running {script_name}...")
    print('='*70)
    
    # Set PYTHONPATH to include local packages
    env = os.environ.copy()
    env['PYTHONPATH'] = '.opencode/python-packages'
    
    try:
        result = subprocess.run(
            ['python3', script_path],
            capture_output=True,
            text=True,
            env=env,
            timeout=300  # 5 minute timeout
        )
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode != 0:
            print(f"ERROR: {script_name} failed with return code {result.returncode}")
            return False
        
        print(f"✓ {script_name} completed successfully")
        return True
        
    except subprocess.TimeoutExpired:
        print(f"ERROR: {script_name} timed out after 5 minutes")
        return False
    except Exception as e:
        print(f"ERROR running {script_name}: {e}")
        return False

def main():
    print("="*70)
    print("NHANES Iron Deficiency Without Anemia - Master Analysis Script")
    print("="*70)
    print("\nThis will run the complete analysis pipeline:")
    print("  1. Data preparation")
    print("  2. Descriptive statistics")
    print("  3. Regression analysis")
    print("  4. Figure generation")
    print()
    
    scripts = [
        "01_data_prep.py",
        "02_descriptive_stats.py",
        "03_regression_analysis.py",
        "04_generate_figures.py"
    ]
    
    success_count = 0
    for script in scripts:
        if run_script(script):
            success_count += 1
        else:
            print(f"\nStopping due to failure in {script}")
            break
    
    print(f"\n{'='*70}")
    print(f"Analysis Complete: {success_count}/{len(scripts)} scripts successful")
    print('='*70)
    
    if success_count == len(scripts):
        print("\n✓ All analysis steps completed successfully!")
        print("\nGenerated outputs:")
        print(f"  - Processed data: {OUTPUT_DIR}/processed_data.csv")
        print(f"  - Tables: {OUTPUT_DIR}/outputs/tables/")
        print(f"  - Figures: {OUTPUT_DIR}/outputs/figures/")
        return 0
    else:
        print("\n✗ Some analysis steps failed. Check output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
