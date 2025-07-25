#!/usr/bin/env python3
"""
EMERGE and ENGAGE SUVR Data Plotter
Creates a 2-panel plot showing SUVR change from baseline for both studies
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set up plotting style
plt.style.use('default')

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
        print(f"Series: {df['Series'].unique()}")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def plot_single_panel(ax, df, title, colors=None):
    """
    Plot SUVR data for a single panel
    
    Parameters:
    -----------
    ax : matplotlib.axes.Axes
        Axes to plot on
    df : pandas.DataFrame
        SUVR data with columns: Series, Time (weeks), measurement, CI
    title : str
        Title for the panel
    colors : list, optional
        List of colors for each series
    """
    # Get unique series
    series = df['Series'].unique()
    print(f"Plotting {len(series)} series for {title}: {series}")
    
    # Define color mapping for each series
    color_map = {
        'Placebo': 'gray',
        'Low-dose': 'cyan', 
        'High-dose': 'purple'
    }
    
    # Plot each series
    for i, series_name in enumerate(series):
        # Filter data for this series
        series_data = df[df['Series'] == series_name].copy()
        series_data = series_data.sort_values('Time (weeks)')
        
        # Extract data
        time = series_data['Time (weeks)'].values
        measurements = series_data['measurement'].values
        ci_values = series_data['CI'].values
        
        # Get the correct color for this series
        series_color = color_map.get(series_name, 'black')
        
        # Handle NaN CI values
        if np.isnan(ci_values).all():
            # No CI data, plot without error bars
            ax.plot(time, measurements, 
                   marker='s' if series_name != 'Placebo' else 'D', 
                   linewidth=2, 
                   markersize=6,
                   label=series_name,
                   color=series_color)
        else:
            # Plot with error bars
            ax.errorbar(time, measurements, yerr=ci_values,
                       marker='s' if series_name != 'Placebo' else 'D', 
                       linewidth=2, 
                       markersize=6,
                       capsize=4,
                       capthick=1.5,
                       elinewidth=1.5,
                       label=series_name,
                       color=series_color)
    
    # Customize the plot to match reference
    ax.set_xlabel('Analysis visit (weeks)', fontsize=14, fontweight='bold')
    ax.set_ylabel('SUVR Change from Baseline', fontsize=14, fontweight='bold')
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    
    # Set axis limits to match reference plots
    ax.set_xlim(-5, 85)
    ax.set_ylim(-0.35, 0.05)
    
    # Add horizontal line at y=0
    ax.axhline(y=0, color='black', linestyle='--', alpha=0.5)
    
    # Set tick parameters
    ax.tick_params(axis='both', which='major', labelsize=12)
    
    # Add sample sizes below x-axis
    sample_sizes = []
    for series_name in series:
        series_data = df[df['Series'] == series_name]
        sizes = []
        for _, row in series_data.iterrows():
            if row['Time (weeks)'] == 0:
                sizes.append(f"n={int(row['n'])}")
            else:
                sizes.append(str(int(row['n'])))
        sample_sizes.append(sizes)
    
    # Add sample size text below x-axis
    y_pos = -0.42
    for i, sizes in enumerate(sample_sizes):
        for j, size in enumerate(sizes):
            x_pos = df[df['Series'] == series[i]]['Time (weeks)'].iloc[j]
            ax.text(x_pos, y_pos, size, ha='center', va='top', fontsize=10)
        y_pos -= 0.03
    
    # Add series labels for sample sizes
    y_pos = -0.42
    for i, series_name in enumerate(series):
        series_color = color_map.get(series_name, 'black')
        ax.text(-10, y_pos, series_name, ha='right', va='top', fontsize=10, 
               color=series_color)
        y_pos -= 0.03

def create_emerge_engage_plot(emerge_df, engage_df, save_plot=True):
    """
    Create a 2-panel plot for EMERGE and ENGAGE data
    
    Parameters:
    -----------
    emerge_df : pandas.DataFrame
        EMERGE SUVR data
    engage_df : pandas.DataFrame
        ENGAGE SUVR data
    save_plot : bool, default True
        Whether to save the plot
    """
    # Create figure with 2 panels
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    # Plot EMERGE data
    plot_single_panel(ax1, emerge_df, 'EMERGE')
    
    # Plot ENGAGE data
    plot_single_panel(ax2, engage_df, 'ENGAGE')
    
    # Add legend to the right of the plots
    handles, labels = ax1.get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper right', bbox_to_anchor=(0.98, 0.95), 
              fontsize=12, frameon=True, fancybox=True, shadow=True)
    
    # Remove individual legends if they exist
    if ax1.get_legend() is not None:
        ax1.get_legend().remove()
    if ax2.get_legend() is not None:
        ax2.get_legend().remove()
    
    plt.tight_layout()
    
    if save_plot:
        # Ensure the figures directory exists
        fig_dir = Path('figures/empirical_data')
        fig_dir.mkdir(parents=True, exist_ok=True)
        
        plt.savefig('figures/empirical_data/EMERGE_ENGAGE_SUVR_Reduction.png', 
                   dpi=300, bbox_inches='tight')
        print("Plot saved as 'figures/empirical_data/EMERGE_ENGAGE_SUVR_Reduction.png'")
    
    plt.show()

def explore_suvr_data(df, study_name):
    """
    Explore SUVR data structure and statistics
    
    Parameters:
    -----------
    df : pandas.DataFrame
        SUVR data to explore
    study_name : str
        Name of the study
    """
    print(f"\n=== {study_name} SUVR DATA EXPLORATION ===")
    print(f"Data shape: {df.shape}")
    print(f"\nSeries: {df['Series'].unique()}")
    print(f"Time points: {sorted(df['Time (weeks)'].unique())}")
    
    print(f"\nSummary by series:")
    for series in df['Series'].unique():
        series_data = df[df['Series'] == series]
        print(f"\n{series}:")
        print(f"  Number of observations: {len(series_data)}")
        print(f"  Measurement range: {series_data['measurement'].min():.4f} to {series_data['measurement'].max():.4f}")
        print(f"  Mean measurement: {series_data['measurement'].mean():.4f}")
        if not series_data['CI'].isna().all():
            print(f"  Mean CI: {series_data['CI'].mean():.4f}")

# Main execution
if __name__ == "__main__":
    # Load SUVR data
    data_dir = Path("data/SUVR")
    emerge_file = data_dir / "EMERGE_ADUCANUMAB.xlsx"
    engage_file = data_dir / "ENGAGE_ADUCANUMAB.xlsx"
    
    if emerge_file.exists() and engage_file.exists():
        print("Loading EMERGE and ENGAGE SUVR data...")
        
        # Load EMERGE data
        emerge_df = load_suvr_data(emerge_file)
        if emerge_df is not None:
            explore_suvr_data(emerge_df, "EMERGE")
        
        # Load ENGAGE data
        engage_df = load_suvr_data(engage_file)
        if engage_df is not None:
            explore_suvr_data(engage_df, "ENGAGE")
        
        # Create the 2-panel plot
        if emerge_df is not None and engage_df is not None:
            print("\nCreating 2-panel plot for EMERGE and ENGAGE...")
            create_emerge_engage_plot(emerge_df, engage_df)
        else:
            print("Failed to load one or both datasets")
            
    else:
        print("One or both files not found:")
        print(f"EMERGE file exists: {emerge_file.exists()}")
        print(f"ENGAGE file exists: {engage_file.exists()}")
        print("\nAvailable files in data directory:")
        for file in data_dir.glob("*.xlsx"):
            print(f"  - {file.name}") 