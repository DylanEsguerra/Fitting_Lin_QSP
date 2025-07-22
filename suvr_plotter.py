#!/usr/bin/env python3
"""
SUVR Data Plotter
Specialized tool for plotting SUVR data with confidence intervals
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set up plotting style
plt.style.use('default')
sns.set_palette("husl")

def load_suvr_data(file_path):
    """
    Load SUVR data from Excel file
    
    Parameters:
    -----------
    file_path : str or Path
        Path to the SUVR Excel file
        
    Returns:
    --------
    pandas.DataFrame
        Loaded SUVR data
    """
    try:
        df = pd.read_excel(file_path)
        print(f"Successfully loaded SUVR data from {file_path}")
        print(f"Data shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print(f"Conditions: {df['Condition'].unique()}")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def plot_suvr_with_ci(df, save_plot=True):
    """
    Plot SUVR data with confidence intervals for each condition
    
    Parameters:
    -----------
    df : pandas.DataFrame
        SUVR data with columns: Condition, Time (years), y, CI
    figsize : tuple, default (12, 8)
        Figure size
    save_plot : bool, default True
        Whether to save the plot
    """
    # Get unique conditions
    conditions = df['Condition'].unique()
    print(f"Plotting {len(conditions)} conditions: {conditions}")
    
    # Set up the plot with larger size for better readability
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Define colors to match the reference plot
    colors = ['#1f77b4', '#d62728', '#2ca02c', '#17a2b8', '#9467bd']  # Blue, Red, Green, Cyan, Purple
    
    # Plot each condition
    for i, condition in enumerate(conditions):
        # Filter data for this condition
        condition_data = df[df['Condition'] == condition].copy()
        condition_data = condition_data.sort_values('Time (years)')
        
        # Extract data
        time = condition_data['Time (years)'].values
        y_values = condition_data['y'].values
        ci_values = condition_data['CI'].values
        
        # Calculate upper and lower bounds
        y_upper = y_values + ci_values
        y_lower = y_values - ci_values
        
        # Plot the main line with error bars
        ax.errorbar(time*52, y_values, yerr=ci_values,
                   marker='o', 
                   linewidth=3, 
                   markersize=8,
                   capsize=8,   # Length of error bar caps
                   capthick=2,  # Thickness of error bar caps
                   elinewidth=2, # Thickness of error bar lines
                   label=condition,
                   color=colors[i % len(colors)])
    
    # Customize the plot to match reference with improved readability
    ax.set_xlabel('Time (weeks)', fontsize=16, fontweight='bold')
    ax.set_ylabel('SUVR Change from Baseline', fontsize=16, fontweight='bold')
    ax.set_title('Aducanumab SUVR Change from Baseline', fontsize=18, fontweight='bold', pad=20)
    ax.legend(title='Dose (mg/kg)', fontsize=14, title_fontsize=15, frameon=True, fancybox=True, shadow=True)
    ax.grid(True, alpha=0.4, linestyle='--')
    
    # Increase tick label sizes
    ax.tick_params(axis='both', which='major', labelsize=14)
    
    # Set axis limits with some padding
    x_min, x_max = 0, df['Time (years)'].max()*52 + 26
    y_min, y_max = df['y'].min(), df['y'].max()
    y_range = y_max - y_min
    
    ax.set_xlim(x_min - 0.1, x_max + 0.1)
    ax.set_ylim(-0.3, 0.05)
    
    plt.tight_layout()
    
    if save_plot:
        plt.savefig('figures/empirical_data/PRIME_SUVR_Reduction.png', dpi=300, bbox_inches='tight')
        print("Plot saved as 'figures/empirical_data/PRIME_SUVR_Reduction.png'")
    
    plt.show()



def explore_suvr_data(df):
    """
    Explore SUVR data structure and statistics
    
    Parameters:
    -----------
    df : pandas.DataFrame
        SUVR data to explore
    """
    print("\n=== SUVR DATA EXPLORATION ===")
    print(f"Data shape: {df.shape}")
    print(f"\nConditions: {df['Condition'].unique()}")
    print(f"Time points: {sorted(df['Time (years)'].unique())}")
    
    print(f"\nSummary by condition:")
    for condition in df['Condition'].unique():
        condition_data = df[df['Condition'] == condition]
        print(f"\n{condition}:")
        print(f"  Number of observations: {len(condition_data)}")
        print(f"  Y range: {condition_data['y'].min():.4f} to {condition_data['y'].max():.4f}")
        print(f"  Mean Y: {condition_data['y'].mean():.4f}")
        print(f"  Mean CI: {condition_data['CI'].mean():.4f}")

# Main execution
if __name__ == "__main__":
    # Load SUVR data
    data_dir = Path("data/SUVR")
    excel_file = data_dir / "SUVR_PRIME.xlsx"
    
    if excel_file.exists():
        print(f"Loading SUVR data from {excel_file}")
        df = load_suvr_data(excel_file)
        
        if df is not None:
            # Explore the data
            explore_suvr_data(df)
            
            # Create the main plot with all conditions
            print("\nCreating main plot with all conditions...")
            plot_suvr_with_ci(df)
            
            
    else:
        print(f"File not found: {excel_file}")
        print("Available files in data directory:")
        for file in data_dir.glob("*.xlsx"):
            print(f"  - {file.name}") 