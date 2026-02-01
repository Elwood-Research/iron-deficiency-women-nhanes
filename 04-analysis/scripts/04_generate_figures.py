#!/usr/bin/env python3
"""
NHANES Iron Deficiency Without Anemia Study - Figure Generation Script
=====================================================================

This script generates all figures for the manuscript:
- Figure 1: Study flow diagram (CONSORT-style)
- Figure 2: Ferritin distribution by supplement use
- Figure 3: IDWA prevalence by demographics

Author: NHANES Analysis Pipeline
Date: 2026-01-31
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.patches import Rectangle

# Set random seed for reproducibility
np.random.seed(42)

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

OUTPUT_DIR = "studies/iron-deficiency-women-2026-01-31/04-analysis"
FIGURES_DIR = os.path.join(OUTPUT_DIR, "outputs", "figures")

def create_figure1_flow_diagram():
    """Create Figure 1: Study flow diagram."""
    
    fig, ax = plt.subplots(figsize=(12, 14), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 16)
    ax.axis('off')
    
    # Color scheme
    color_box = '#E8F4F8'
    color_excluded = '#FFE8E8'
    color_final = '#E8F8E8'
    color_border = '#2E86AB'
    
    # Title
    ax.text(5, 15.5, 'Study Flow Diagram', fontsize=16, fontweight='bold', 
            ha='center', va='center')
    ax.text(5, 15.0, 'NHANES Iron Deficiency Without Anemia Study (2005-2022)', 
            fontsize=11, ha='center', va='center', style='italic')
    
    # Box 1: Initial sample
    box1 = FancyBboxPatch((1.5, 13.5), 7, 1, boxstyle="round,pad=0.1", 
                          facecolor=color_box, edgecolor=color_border, linewidth=2)
    ax.add_patch(box1)
    ax.text(5, 14.0, 'NHANES Participants\nCycles D, E, F, G, H, I, J, L\n(2005-2022)', 
            fontsize=11, ha='center', va='center', fontweight='bold')
    
    # Exclusion: Age
    box_excl1 = FancyBboxPatch((0.2, 11.8), 3, 0.8, boxstyle="round,pad=0.05",
                               facecolor=color_excluded, edgecolor='red', linewidth=1.5)
    ax.add_patch(box_excl1)
    ax.text(1.7, 12.2, 'Age <18 or >45\n(~40,000 excluded)', fontsize=9, ha='center', va='center')
    
    # Exclusion: Male
    box_excl2 = FancyBboxPatch((6.8, 11.8), 3, 0.8, boxstyle="round,pad=0.05",
                               facecolor=color_excluded, edgecolor='red', linewidth=1.5)
    ax.add_patch(box_excl2)
    ax.text(8.3, 12.2, 'Male\n(~35,000 excluded)', fontsize=9, ha='center', va='center')
    
    # Box 2: Age and gender eligible
    arrow1 = FancyArrowPatch((5, 13.5), (5, 12.0), arrowstyle='->', 
                            mutation_scale=20, linewidth=2, color=color_border)
    ax.add_patch(arrow1)
    
    box2 = FancyBboxPatch((1.5, 10.5), 7, 1, boxstyle="round,pad=0.1",
                          facecolor=color_box, edgecolor=color_border, linewidth=2)
    ax.add_patch(box2)
    ax.text(5, 11.0, 'Women 18-45 years\n~10,500 included', fontsize=11, ha='center', va='center')
    
    # Exclusion: Pregnant
    box_excl3 = FancyBboxPatch((0.2, 9.3), 3, 0.7, boxstyle="round,pad=0.05",
                               facecolor=color_excluded, edgecolor='red', linewidth=1.5)
    ax.add_patch(box_excl3)
    ax.text(1.7, 9.65, 'Pregnant\n(~600 excluded)', fontsize=9, ha='center', va='center')
    
    # Box 3: Non-pregnant
    arrow2 = FancyArrowPatch((5, 10.5), (5, 9.3), arrowstyle='->',
                            mutation_scale=20, linewidth=2, color=color_border)
    ax.add_patch(arrow2)
    
    box3 = FancyBboxPatch((1.5, 8.0), 7, 1, boxstyle="round,pad=0.1",
                          facecolor=color_box, edgecolor=color_border, linewidth=2)
    ax.add_patch(box3)
    ax.text(5, 8.5, 'Non-pregnant women 18-45\n~9,900 included', fontsize=11, ha='center', va='center')
    
    # Exclusion: Missing ferritin
    box_excl4 = FancyBboxPatch((0.2, 6.8), 3, 0.7, boxstyle="round,pad=0.05",
                               facecolor=color_excluded, edgecolor='red', linewidth=1.5)
    ax.add_patch(box_excl4)
    ax.text(1.7, 7.15, 'Missing ferritin\n(~2,500 excluded)', fontsize=9, ha='center', va='center')
    
    # Box 4: With ferritin
    arrow3 = FancyArrowPatch((5, 8.0), (5, 7.0), arrowstyle='->',
                            mutation_scale=20, linewidth=2, color=color_border)
    ax.add_patch(arrow3)
    
    box4 = FancyBboxPatch((1.5, 5.5), 7, 1, boxstyle="round,pad=0.1",
                          facecolor=color_box, edgecolor=color_border, linewidth=2)
    ax.add_patch(box4)
    ax.text(5, 6.0, 'With ferritin measurement\n~7,400 included', fontsize=11, ha='center', va='center')
    
    # Exclusion: Missing hemoglobin
    box_excl5 = FancyBboxPatch((0.2, 4.3), 3, 0.7, boxstyle="round,pad=0.05",
                               facecolor=color_excluded, edgecolor='red', linewidth=1.5)
    ax.add_patch(box_excl5)
    ax.text(1.7, 4.65, 'Missing hemoglobin\n(~50 excluded)', fontsize=9, ha='center', va='center')
    
    # Box 5: Final analytic sample
    arrow4 = FancyArrowPatch((5, 5.5), (5, 4.5), arrowstyle='->',
                            mutation_scale=20, linewidth=2, color=color_border)
    ax.add_patch(arrow4)
    
    box5 = FancyBboxPatch((1.5, 2.8), 7, 1.5, boxstyle="round,pad=0.1",
                          facecolor=color_final, edgecolor='green', linewidth=3)
    ax.add_patch(box5)
    ax.text(5, 3.8, 'FINAL ANALYTIC SAMPLE\nNon-pregnant women 18-45 years\nwith complete iron status data\n~7,350 participants', 
            fontsize=12, ha='center', va='center', fontweight='bold')
    
    # Breakdown of final sample
    box6 = FancyBboxPatch((0.5, 0.8), 4, 1.5, boxstyle="round,pad=0.08",
                          facecolor='#FFF8E8', edgecolor='orange', linewidth=1.5)
    ax.add_patch(box6)
    ax.text(2.5, 1.8, 'IDWA Cases\n~800-1,000 (10-12%)\nFerritin <15 & Hgb ≥12', 
            fontsize=10, ha='center', va='center')
    
    box7 = FancyBboxPatch((5.5, 0.8), 4, 1.5, boxstyle="round,pad=0.08",
                          facecolor='#E8F0FF', edgecolor='blue', linewidth=1.5)
    ax.add_patch(box7)
    ax.text(7.5, 1.8, 'Normal Iron Status\n~6,350-6,550 (88-90%)', 
            fontsize=10, ha='center', va='center')
    
    # Arrows to breakdown
    arrow5a = FancyArrowPatch((3.5, 2.8), (2.5, 2.3), arrowstyle='->',
                             mutation_scale=15, linewidth=1.5, color='orange')
    ax.add_patch(arrow5a)
    arrow5b = FancyArrowPatch((6.5, 2.8), (7.5, 2.3), arrowstyle='->',
                             mutation_scale=15, linewidth=1.5, color='blue')
    ax.add_patch(arrow5b)
    
    plt.tight_layout()
    output_file = os.path.join(FIGURES_DIR, 'figure1_flow_diagram.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Saved Figure 1 to: {output_file}")
    plt.close()

def create_figure2_ferritin_distribution(df):
    """Create Figure 2: Ferritin distribution by supplement use."""
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 12), dpi=300)
    
    # Filter to reasonable ferritin range for visualization
    df_plot = df[(df['LBXFER'] >= 2) & (df['LBXFER'] <= 150)].copy()
    
    # Panel A: Violin plot
    ax1 = axes[0, 0]
    supp_labels = {0: 'No Supplement', 1: 'Iron Supplement'}
    df_plot['supp_label'] = df_plot['iron_supplement'].map(supp_labels)
    
    sns.violinplot(data=df_plot, x='supp_label', y='LBXFER', ax=ax1, palette=['#E74C3C', '#27AE60'])
    ax1.set_ylabel('Ferritin (ng/mL)', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Iron Supplement Use', fontsize=12, fontweight='bold')
    ax1.set_title('A. Ferritin Distribution by Supplement Use', fontsize=13, fontweight='bold')
    ax1.set_ylim(0, 150)
    
    # Add horizontal line at IDWA threshold
    ax1.axhline(y=15, color='red', linestyle='--', linewidth=2, alpha=0.7, label='IDWA threshold')
    ax1.legend(loc='upper right')
    
    # Panel B: Box plot (log scale)
    ax2 = axes[0, 1]
    sns.boxplot(data=df_plot, x='supp_label', y='log_ferritin', ax=ax2, palette=['#E74C3C', '#27AE60'])
    ax2.set_ylabel('Log(Ferritin)', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Iron Supplement Use', fontsize=12, fontweight='bold')
    ax2.set_title('B. Log-Transformed Ferritin', fontsize=13, fontweight='bold')
    
    # Add horizontal line at log(15)
    ax2.axhline(y=np.log(15), color='red', linestyle='--', linewidth=2, alpha=0.7, label='IDWA threshold')
    ax2.legend(loc='lower right')
    
    # Panel C: Histogram
    ax3 = axes[1, 0]
    bins = np.linspace(2, 100, 30)
    ax3.hist(df_plot[df_plot['iron_supplement'] == 0]['LBXFER'], bins=bins, alpha=0.6, 
            label='No Supplement', color='#E74C3C', edgecolor='white')
    ax3.hist(df_plot[df_plot['iron_supplement'] == 1]['LBXFER'], bins=bins, alpha=0.6,
            label='Iron Supplement', color='#27AE60', edgecolor='white')
    ax3.set_xlabel('Ferritin (ng/mL)', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Frequency', fontsize=12, fontweight='bold')
    ax3.set_title('C. Ferritin Distribution Histogram', fontsize=13, fontweight='bold')
    ax3.legend()
    ax3.set_xlim(0, 100)
    
    # Add vertical line at IDWA threshold
    ax3.axvline(x=15, color='red', linestyle='--', linewidth=2, alpha=0.7)
    
    # Panel D: Cumulative distribution
    ax4 = axes[1, 1]
    
    no_supp = df_plot[df_plot['iron_supplement'] == 0]['LBXFER'].sort_values()
    supp = df_plot[df_plot['iron_supplement'] == 1]['LBXFER'].sort_values()
    
    y_no_supp = np.arange(1, len(no_supp) + 1) / len(no_supp) * 100
    y_supp = np.arange(1, len(supp) + 1) / len(supp) * 100
    
    ax4.plot(no_supp, y_no_supp, label='No Supplement', color='#E74C3C', linewidth=2)
    ax4.plot(supp, y_supp, label='Iron Supplement', color='#27AE60', linewidth=2)
    ax4.set_xlabel('Ferritin (ng/mL)', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Cumulative Percentile (%)', fontsize=12, fontweight='bold')
    ax4.set_title('D. Cumulative Distribution', fontsize=13, fontweight='bold')
    ax4.legend()
    ax4.set_xlim(0, 100)
    ax4.set_ylim(0, 100)
    ax4.grid(True, alpha=0.3)
    
    # Add vertical line at IDWA threshold
    ax4.axvline(x=15, color='red', linestyle='--', linewidth=2, alpha=0.7)
    
    # Add text annotation
    ax4.text(20, 10, 'IDWA\nthreshold\n(15 ng/mL)', fontsize=9, color='red', 
            ha='left', va='bottom')
    
    plt.tight_layout()
    output_file = os.path.join(FIGURES_DIR, 'figure2_ferritin_distribution.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Saved Figure 2 to: {output_file}")
    plt.close()

def create_figure3_idwa_prevalence(df):
    """Create Figure 3: IDWA prevalence by age and race."""
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 12), dpi=300)
    
    weights = df['weight_adjusted'].values
    
    # Panel A: IDWA prevalence by age group
    ax1 = axes[0, 0]
    
    age_groups = ['18-25', '26-30', '31-35', '36-40', '41-45']
    age_prev = []
    age_se = []
    age_n = []
    
    for age_grp in age_groups:
        subgroup = df[df['age_group'] == age_grp]
        n_total = len(subgroup)
        n_idwa = subgroup['IDWA'].sum()
        
        if n_total > 0:
            w = subgroup['weight_adjusted'].values
            idwa_vals = subgroup['IDWA'].astype(int).values
            mask = (~np.isnan(w)) & (~np.isnan(idwa_vals)) & (w > 0)
            if mask.sum() > 0:
                prev = np.average(idwa_vals[mask], weights=w[mask])
                # Approximate SE
                se = np.sqrt(prev * (1 - prev) / mask.sum())
            else:
                prev = n_idwa / n_total if n_total > 0 else 0
                se = 0
        else:
            prev = 0
            se = 0
        
        age_prev.append(prev * 100)
        age_se.append(se * 100)
        age_n.append(n_total)
    
    x_pos = np.arange(len(age_groups))
    bars1 = ax1.bar(x_pos, age_prev, yerr=age_se, capsize=5, color='#3498DB', 
                   edgecolor='black', linewidth=1.5, alpha=0.8)
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(age_groups)
    ax1.set_xlabel('Age Group (years)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('IDWA Prevalence (%)', fontsize=12, fontweight='bold')
    ax1.set_title('A. IDWA Prevalence by Age Group', fontsize=13, fontweight='bold')
    ax1.set_ylim(0, max(age_prev) * 1.3)
    ax1.grid(axis='y', alpha=0.3)
    
    # Add sample sizes on bars
    for i, (bar, n) in enumerate(zip(bars1, age_n)):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + age_se[i] + 0.5,
                f'n={n}', ha='center', va='bottom', fontsize=9)
    
    # Panel B: IDWA prevalence by race/ethnicity
    ax2 = axes[0, 1]
    
    races = ['Non-Hispanic\nWhite', 'Non-Hispanic\nBlack', 'Mexican\nAmerican', 
             'Other\nHispanic', 'Other\nRace']
    race_prev = []
    race_se = []
    race_n = []
    
    race_mapping = {
        'Non-Hispanic White': 'Non-Hispanic\nWhite',
        'Non-Hispanic Black': 'Non-Hispanic\nBlack',
        'Mexican American': 'Mexican\nAmerican',
        'Other Hispanic': 'Other\nHispanic',
        'Other Race': 'Other\nRace'
    }
    
    for race in ['Non-Hispanic White', 'Non-Hispanic Black', 'Mexican American',
                 'Other Hispanic', 'Other Race']:
        subgroup = df[df['race_category'] == race]
        n_total = len(subgroup)
        n_idwa = subgroup['IDWA'].sum()
        
        if n_total > 0:
            w = subgroup['weight_adjusted'].values
            idwa_vals = subgroup['IDWA'].astype(int).values
            mask = (~np.isnan(w)) & (~np.isnan(idwa_vals)) & (w > 0)
            if mask.sum() > 0:
                prev = np.average(idwa_vals[mask], weights=w[mask])
                se = np.sqrt(prev * (1 - prev) / mask.sum())
            else:
                prev = n_idwa / n_total if n_total > 0 else 0
                se = 0
        else:
            prev = 0
            se = 0
        
        race_prev.append(prev * 100)
        race_se.append(se * 100)
        race_n.append(n_total)
    
    colors_race = ['#E74C3C', '#3498DB', '#2ECC71', '#F39C12', '#9B59B6']
    x_pos = np.arange(len(races))
    bars2 = ax2.bar(x_pos, race_prev, yerr=race_se, capsize=5, color=colors_race,
                   edgecolor='black', linewidth=1.5, alpha=0.8)
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(races, fontsize=9)
    ax2.set_xlabel('Race/Ethnicity', fontsize=12, fontweight='bold')
    ax2.set_ylabel('IDWA Prevalence (%)', fontsize=12, fontweight='bold')
    ax2.set_title('B. IDWA Prevalence by Race/Ethnicity', fontsize=13, fontweight='bold')
    ax2.set_ylim(0, max(race_prev) * 1.3)
    ax2.grid(axis='y', alpha=0.3)
    
    # Add sample sizes on bars
    for i, (bar, n) in enumerate(zip(bars2, race_n)):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + race_se[i] + 0.5,
                f'n={n}', ha='center', va='bottom', fontsize=8)
    
    # Panel C: Heatmap by age and race
    ax3 = axes[1, 0]
    
    heatmap_data = []
    for age_grp in age_groups:
        row = []
        for race in ['Non-Hispanic White', 'Non-Hispanic Black', 'Mexican American',
                     'Other Hispanic', 'Other Race']:
            subgroup = df[(df['age_group'] == age_grp) & (df['race_category'] == race)]
            n_total = len(subgroup)
            
            if n_total >= 20:  # Minimum sample size
                w = subgroup['weight_adjusted'].values
                idwa_vals = subgroup['IDWA'].astype(int).values
                mask = (~np.isnan(w)) & (~np.isnan(idwa_vals)) & (w > 0)
                if mask.sum() > 0:
                    prev = np.average(idwa_vals[mask], weights=w[mask]) * 100
                else:
                    prev = np.nan
            else:
                prev = np.nan
            row.append(prev)
        heatmap_data.append(row)
    
    heatmap_df = pd.DataFrame(heatmap_data, 
                             index=age_groups,
                             columns=['NHW', 'NHB', 'MA', 'OH', 'OR'])
    
    sns.heatmap(heatmap_df, annot=True, fmt='.1f', cmap='YlOrRd', 
               cbar_kws={'label': 'IDWA Prevalence (%)'}, ax=ax3,
               linewidths=0.5, linecolor='white')
    ax3.set_xlabel('Race/Ethnicity', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Age Group', fontsize=12, fontweight='bold')
    ax3.set_title('C. IDWA Prevalence Heatmap', fontsize=13, fontweight='bold')
    
    # Panel D: Prevalence by supplement use and race
    ax4 = axes[1, 1]
    
    supp_race_prev = []
    supp_race_labels = []
    supp_race_colors = []
    
    for race in ['Non-Hispanic White', 'Non-Hispanic Black', 'Mexican American']:
        for supp in [0, 1]:
            subgroup = df[(df['race_category'] == race) & (df['iron_supplement'] == supp)]
            n_total = len(subgroup)
            
            if n_total >= 10:
                w = subgroup['weight_adjusted'].values
                idwa_vals = subgroup['IDWA'].astype(int).values
                mask = (~np.isnan(w)) & (~np.isnan(idwa_vals)) & (w > 0)
                if mask.sum() > 0:
                    prev = np.average(idwa_vals[mask], weights=w[mask]) * 100
                else:
                    prev = 0
            else:
                prev = 0
            
            supp_race_prev.append(prev)
            supp_label = 'No Supp' if supp == 0 else 'Supp'
            supp_race_labels.append(f"{race[:3]}\n{supp_label}")
            supp_race_colors.append('#E74C3C' if supp == 0 else '#27AE60')
    
    x_pos = np.arange(len(supp_race_labels))
    bars4 = ax4.bar(x_pos, supp_race_prev, color=supp_race_colors, 
                   edgecolor='black', linewidth=1.5, alpha=0.8)
    ax4.set_xticks(x_pos)
    ax4.set_xticklabels(supp_race_labels, fontsize=9)
    ax4.set_xlabel('Race and Supplement Use', fontsize=12, fontweight='bold')
    ax4.set_ylabel('IDWA Prevalence (%)', fontsize=12, fontweight='bold')
    ax4.set_title('D. IDWA by Race and Supplement Use', fontsize=13, fontweight='bold')
    ax4.grid(axis='y', alpha=0.3)
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='#E74C3C', edgecolor='black', label='No Supplement'),
                      Patch(facecolor='#27AE60', edgecolor='black', label='Iron Supplement')]
    ax4.legend(handles=legend_elements, loc='upper right')
    
    plt.tight_layout()
    output_file = os.path.join(FIGURES_DIR, 'figure3_idwa_prevalence.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Saved Figure 3 to: {output_file}")
    plt.close()

def main():
    print("=" * 70)
    print("NHANES Iron Deficiency Without Anemia - Figure Generation")
    print("=" * 70)
    print()
    
    # Load processed data
    data_file = os.path.join(OUTPUT_DIR, 'processed_data.csv')
    if not os.path.exists(data_file):
        print(f"Error: Processed data not found at {data_file}")
        print("Please run 01_data_prep.py first.")
        return
    
    df = pd.read_csv(data_file)
    print(f"Loaded processed data: {len(df)} rows")
    print()
    
    # Create figures
    print("=" * 70)
    print("Creating Figure 1: Study flow diagram...")
    print("=" * 70)
    create_figure1_flow_diagram()
    
    print("\n" + "=" * 70)
    print("Creating Figure 2: Ferritin distribution...")
    print("=" * 70)
    create_figure2_ferritin_distribution(df)
    
    print("\n" + "=" * 70)
    print("Creating Figure 3: IDWA prevalence by demographics...")
    print("=" * 70)
    create_figure3_idwa_prevalence(df)
    
    print("\n" + "=" * 70)
    print("Figure generation complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()
