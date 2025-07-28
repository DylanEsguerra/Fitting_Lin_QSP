#!/usr/bin/env python3
"""
Donanemab Phase 3 SUVR Data Plotter
Specialized tool for plotting Donanemab Phase 3 data with Amyloid PET levels
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

def load_donanemab_data(file_path):
    """
    Load Donanemab Phase 3 data from Excel file
    
    Parameters:
    -----------
    file_path : str or Path
        Path to the Donanemab Excel file
        
    Returns:
    --------
    pandas.DataFrame
        Loaded Donanemab data
    """
    try:
        df = pd.read_excel(file_path)
        print(f"Successfully loaded Donanemab data from {file_path}")
        print(f"Data shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print(f"Series: {df['Series'].unique()}")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def plot_donanemab_amyloid_pet(df, save_plot=True):
    """
    Plot Donanemab Phase 3 Amyloid PET data with proper styling
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Donanemab data with columns: Series, Time (weeks), measurement
    save_plot : bool, default True
        Whether to save the plot
    """
    # Get unique series
    series = df['Series'].unique()
    print(f"Plotting {len(series)} series: {series}")
    
    # Set up the plot for better readability
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Define colors and markers to match the reference plot
    # Orange for Donanemab, Dark teal for Placebo
    colors = {
        'Donanemab Low/Meduium tau': '#ff7f0e',  # Orange
        'Donanemab Combined': '#ff7f0e',          # Orange
        'Placebo Low/Meduium tau': '#1f77b4',     # Dark teal/blue
        'Placebo Combined': '#1f77b4'             # Dark teal/blue
    }
    
    markers = {
        'Donanemab Low/Meduium tau': '^',         # Upward triangle
        'Donanemab Combined': 'o',                # Circle
        'Placebo Low/Meduium tau': '^',           # Upward triangle
        'Placebo Combined': 'o'                   # Circle
    }
    
    # Plot each series
    for series_name in series:
        # Filter data for this series
        series_data = df[df['Series'] == series_name].copy()
        series_data = series_data.sort_values('Time (weeks)')
        
        print(f"  Plotting {series_name}: {len(series_data)} points")
        print(f"    Time values: {series_data['Time (weeks)'].values}")
        print(f"    Measurement values: {series_data['measurement'].values}")
        
        # Extract data
        time = series_data['Time (weeks)'].values
        measurements = series_data['measurement'].values
        
        # Plot the main line with markers
        ax.plot(time, measurements,
               marker=markers[series_name], 
               linewidth=2, 
               markersize=8,
               label=series_name,
               color='black',  # Black lines
               markerfacecolor=colors[series_name],  # Colored points
               markeredgecolor='black',  # Black edges on markers
               markeredgewidth=1)
    
    # Customize the plot to match reference
    ax.set_xlabel('Time after baseline, wk', fontsize=16, fontweight='bold')
    ax.set_ylabel('Amyloid PET, Centiloids', fontsize=16, fontweight='bold')
    ax.set_title('Amyloid PET, Centiloids', fontsize=18, fontweight='bold', pad=20)
    
    # Create legend with proper grouping
    legend_elements = [
        plt.Line2D([0], [0], marker='^', color='black', markerfacecolor='#ff7f0e', 
                  markeredgecolor='black', markersize=8, 
                  label='Low/medium tau - Donanemab', linewidth=2),
        plt.Line2D([0], [0], marker='^', color='black', markerfacecolor='#1f77b4', 
                  markeredgecolor='black', markersize=8, 
                  label='Low/medium tau - Placebo', linewidth=2),
        plt.Line2D([0], [0], marker='o', color='black', markerfacecolor='#ff7f0e', 
                  markeredgecolor='black', markersize=8, 
                  label='Combined - Donanemab', linewidth=2),
        plt.Line2D([0], [0], marker='o', color='black', markerfacecolor='#1f77b4', 
                  markeredgecolor='black', markersize=8, 
                  label='Combined - Placebo', linewidth=2)
    ]
    
    ax.legend(handles=legend_elements, fontsize=12, frameon=True, 
             fancybox=True, shadow=True)
    
    # Add grid
    ax.grid(True, alpha=0.4, linestyle='--')
    
    # Increase tick label sizes
    ax.tick_params(axis='both', which='major', labelsize=14)
    
    # Set axis limits to match reference plot
    ax.set_xlim(0, 80)
    ax.set_ylim(-100, 10)
    
    # Set x-axis ticks to match reference
    ax.set_xticks([0, 12, 24, 36, 52, 64, 76])
    
    # Set y-axis ticks to match reference
    ax.set_yticks([0, -20, -40, -60, -80, -100])
    
    plt.tight_layout()
    
    if save_plot:
        plt.savefig('figures/empirical_data/DONANEMAB_Phase3_Amyloid_PET.png', dpi=300, bbox_inches='tight')
        print("Plot saved as 'figures/empirical_data/DONANEMAB_Phase3_Amyloid_PET.png'")
    
    plt.show()

def explore_donanemab_data(df):
    """
    Explore Donanemab data structure and statistics
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Donanemab data to explore
    """
    print("\n=== DONANEMAB DATA EXPLORATION ===")
    print(f"Data shape: {df.shape}")
    print(f"\nSeries: {df['Series'].unique()}")
    print(f"Time points: {sorted(df['Time (weeks)'].unique())}")
    
    print(f"\nSummary by series:")
    for series_name in df['Series'].unique():
        series_data = df[df['Series'] == series_name]
        print(f"\n{series_name}:")
        print(f"  Number of observations: {len(series_data)}")
        print(f"  Measurement range: {series_data['measurement'].min():.4f} to {series_data['measurement'].max():.4f}")
        print(f"  Mean measurement: {series_data['measurement'].mean():.4f}")
        if 'CI' in df.columns:
            print(f"  Mean CI: {series_data['CI'].mean():.4f}")

# Main execution
if __name__ == "__main__":
    # Load Donanemab data
    data_dir = Path("data/SUVR")
    excel_file = data_dir / "Ph_3_DONANEMAB_Sims_2023.xlsx"
    
    if excel_file.exists():
        print(f"Loading Donanemab data from {excel_file}")
        df = load_donanemab_data(excel_file)
        
        if df is not None:
            # Explore the data
            explore_donanemab_data(df)
            
            # Create the main plot
            print("\nCreating Donanemab Phase 3 Amyloid PET plot...")
            plot_donanemab_amyloid_pet(df)
            
    else:
        print(f"File not found: {excel_file}")
        print("Available files in data directory:")
        for file in data_dir.glob("*.xlsx"):
            print(f"  - {file.name}") 