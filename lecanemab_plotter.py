#!/usr/bin/env python3
"""
Lecanemab SUVR Data Plotter
Creates a 2-panel plot showing SUVR change from baseline for Phase 2b and Phase 3 studies
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

def plot_phase2b_panel(ax, df):
    """
    Plot Phase 2b data with specific color scheme
    
    Parameters:
    -----------
    ax : matplotlib.axes.Axes
        Axes to plot on
    df : pandas.DataFrame
        Phase 2b SUVR data
    """
    # Get unique series
    series = df['Series'].unique()
    series = [s for s in series if pd.notna(s)]  # Remove NaN values
    print(f"Plotting {len(series)} series for Phase 2b: {series}")
    
    # Define specific color and style mapping for Phase 2b
    style_map = {
        'Placebo': {'color': 'black', 'linestyle': '-', 'marker': 'D'},
        '5 mg/kg bi-weekly': {'color': 'purple', 'linestyle': '--', 'marker': 's'},
        '2.5 mg/kg bi-weekly': {'color': 'magenta', 'linestyle': '--', 'marker': 's'},
        '10 mg/kg monthy': {'color': 'blue', 'linestyle': '-', 'marker': 's'},
        '5 mg/kg monthy': {'color': 'gray', 'linestyle': '--', 'marker': 's'},
        '10 mg/kg bi-weekly': {'color': 'green', 'linestyle': '-', 'marker': 's'}
    }
    
    # Plot each series
    for series_name in series:
        if series_name in style_map:
            # Filter data for this series
            series_data = df[df['Series'] == series_name].copy()
            
            # Determine time column
            time_col = 'Time (weeks)' if 'Time (weeks)' in series_data.columns else 'Time (months)'
            series_data = series_data.sort_values(time_col)
            
            # Extract data
            time = series_data[time_col].values
            measurements = series_data['measurement'].values
            
            # Get the style for this series
            style = style_map[series_name]
            
            # Plot the line
            ax.plot(time, measurements, 
                   marker=style['marker'],
                   linestyle=style['linestyle'],
                   linewidth=3, 
                   markersize=8,
                   label=series_name,
                   color=style['color'])
    
    # Customize the plot
    time_col = 'Time (weeks)' if 'Time (weeks)' in df.columns else 'Time (months)'
    ax.set_xlabel('Time (weeks)' if 'Time (weeks)' in df.columns else 'Time (months)', 
                 fontsize=14, fontweight='bold')
    ax.set_ylabel('SUVR Change from Baseline', fontsize=14, fontweight='bold')
    ax.set_title('Phase 2b', fontsize=16, fontweight='bold', pad=20)
    
    # Set axis limits based on data
    x_max = df[time_col].max() + 2
    y_min = df['measurement'].min() - 0.02
    y_max = df['measurement'].max() + 0.02
    
    ax.set_xlim(0, x_max)
    ax.set_ylim(y_min, y_max)
    
    # Add horizontal line at y=0
    ax.axhline(y=0, color='black', linestyle='--', alpha=0.5)
    
    # Set tick parameters
    ax.tick_params(axis='both', which='major', labelsize=12)
    
    # No sample size information - keeping plot clean and simple

def plot_phase3_panel(ax, df):
    """
    Plot Phase 3 data with specific color scheme
    
    Parameters:
    -----------
    ax : matplotlib.axes.Axes
        Axes to plot on
    df : pandas.DataFrame
        Phase 3 SUVR data
    """
    # Get unique series
    series = df['Series'].unique()
    series = [s for s in series if pd.notna(s)]  # Remove NaN values
    print(f"Plotting {len(series)} series for Phase 3: {series}")
    
    # Define specific color mapping for Phase 3
    style_map = {
        'Placebo': {'color': 'blue', 'linestyle': '-', 'marker': 'D'},
        'Lecanemab': {'color': 'yellow', 'linestyle': '-', 'marker': 's'}
    }
    
    # Plot each series
    for series_name in series:
        if series_name in style_map:
            # Filter data for this series
            series_data = df[df['Series'] == series_name].copy()
            
            # Determine time column
            time_col = 'Time (weeks)' if 'Time (weeks)' in series_data.columns else 'Time (months)'
            series_data = series_data.sort_values(time_col)
            
            # Extract data
            time = series_data[time_col].values
            measurements = series_data['measurement'].values
            
            # Get the style for this series
            style = style_map[series_name]
            
            # Plot the line
            ax.plot(time, measurements, 
                   marker=style['marker'],
                   linestyle=style['linestyle'],
                   linewidth=3, 
                   markersize=8,
                   label=series_name,
                   color=style['color'])
    
    # Customize the plot
    time_col = 'Time (weeks)' if 'Time (weeks)' in df.columns else 'Time (months)'
    ax.set_xlabel('Time (weeks)' if 'Time (weeks)' in df.columns else 'Time (months)', 
                 fontsize=14, fontweight='bold')
    ax.set_ylabel('SUVR Change from Baseline', fontsize=14, fontweight='bold')
    ax.set_title('Phase 3', fontsize=16, fontweight='bold', pad=20)
    
    # Set axis limits based on data
    x_max = df[time_col].max() + 2
    y_min = df['measurement'].min() - 0.02
    y_max = df['measurement'].max() + 0.02
    
    ax.set_xlim(0, x_max)
    ax.set_ylim(y_min, y_max)
    
    # Add horizontal line at y=0
    ax.axhline(y=0, color='black', linestyle='--', alpha=0.5)
    
    # Set tick parameters
    ax.tick_params(axis='both', which='major', labelsize=12)
    
    # No sample size information - keeping plot clean and simple

def create_lecanemab_plots(phase2b_df, phase3_df, save_plot=True):
    """
    Create separate plots for Phase 2b and Phase 3 Lecanemab data
    
    Parameters:
    -----------
    phase2b_df : pandas.DataFrame
        Phase 2b SUVR data
    phase3_df : pandas.DataFrame
        Phase 3 SUVR data
    save_plot : bool, default True
        Whether to save the plots
    """
    # Create Phase 2b plot
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    plot_phase2b_panel(ax1, phase2b_df)
    
    # Add compact legend for Phase 2b (many curves)
    handles, labels = ax1.get_legend_handles_labels()
    ax1.legend(handles, labels, loc='upper right', fontsize=10, frameon=True, 
              fancybox=True, shadow=True, ncol=2)  # 2 columns to save space
    
    plt.tight_layout()
    
    if save_plot:
        # Ensure the figures directory exists
        fig_dir = Path('figures/empirical_data')
        fig_dir.mkdir(parents=True, exist_ok=True)
        
        plt.savefig('figures/empirical_data/LECANEMAB_Phase2b_SUVR_Reduction.png', 
                   dpi=300, bbox_inches='tight')
        print("Phase 2b plot saved as 'figures/empirical_data/LECANEMAB_Phase2b_SUVR_Reduction.png'")
    
    plt.show()
    
    # Create Phase 3 plot
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    plot_phase3_panel(ax2, phase3_df)
    
    # Add legend for Phase 3 (fewer curves)
    handles, labels = ax2.get_legend_handles_labels()
    ax2.legend(handles, labels, loc='upper right', fontsize=12, frameon=True, 
              fancybox=True, shadow=True)
    
    plt.tight_layout()
    
    if save_plot:
        plt.savefig('figures/empirical_data/LECANEMAB_Phase3_SUVR_Reduction.png', 
                   dpi=300, bbox_inches='tight')
        print("Phase 3 plot saved as 'figures/empirical_data/LECANEMAB_Phase3_SUVR_Reduction.png'")
    
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
    
    if 'Time (weeks)' in df.columns:
        print(f"Time points (weeks): {sorted(df['Time (weeks)'].unique())}")
    elif 'Time (months)' in df.columns:
        print(f"Time points (months): {sorted(df['Time (months)'].unique())}")
    
    print(f"\nSummary by series:")
    for series in df['Series'].unique():
        if pd.notna(series):
            series_data = df[df['Series'] == series]
            print(f"\n{series}:")
            print(f"  Number of observations: {len(series_data)}")
            print(f"  Measurement range: {series_data['measurement'].min():.4f} to {series_data['measurement'].max():.4f}")
            print(f"  Mean measurement: {series_data['measurement'].mean():.4f}")

# Main execution
if __name__ == "__main__":
    # Load SUVR data
    data_dir = Path("data/SUVR")
    phase2b_file = data_dir / "Phase_2b_LECANEMAB_Swanson_2021.xlsx"
    phase3_file = data_dir / "Phase_3_LECANEMAB_van_Dyck_2022.xlsx"
    
    if phase2b_file.exists() and phase3_file.exists():
        print("Loading Phase 2b and Phase 3 Lecanemab SUVR data...")
        
        # Load Phase 2b data
        phase2b_df = load_suvr_data(phase2b_file)
        if phase2b_df is not None:
            # Remove rows with NaN Series
            phase2b_df = phase2b_df.dropna(subset=['Series'])
            explore_suvr_data(phase2b_df, "Phase 2b")
        
        # Load Phase 3 data
        phase3_df = load_suvr_data(phase3_file)
        if phase3_df is not None:
            explore_suvr_data(phase3_df, "Phase 3")
        
        # Create the separate plots
        if phase2b_df is not None and phase3_df is not None:
            print("\nCreating separate plots for Phase 2b and Phase 3 Lecanemab...")
            create_lecanemab_plots(phase2b_df, phase3_df)
        else:
            print("Failed to load one or both datasets")
            
    else:
        print("One or both files not found:")
        print(f"Phase 2b file exists: {phase2b_file.exists()}")
        print(f"Phase 3 file exists: {phase3_file.exists()}")
        print("\nAvailable files in data directory:")
        for file in data_dir.glob("*.xlsx"):
            print(f"  - {file.name}") 