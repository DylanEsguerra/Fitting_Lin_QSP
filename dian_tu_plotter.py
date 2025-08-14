#!/usr/bin/env python3
"""
DIAN-TU Gantenerumab Data Plotter
Creates plots showing Amyloid PET (Centiloids) and CSF AB42/40 CentiMarker data from the DIAN-TU study
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set up plotting style
plt.style.use('default')

def load_dian_tu_data(file_path):
    """
    Load DIAN-TU data from Excel file
    
    Parameters:
    -----------
    file_path : str or Path
        Path to the DIAN-TU Excel file
        
    Returns:
    --------
    pandas.DataFrame
        Loaded DIAN-TU data
    """
    try:
        df = pd.read_excel(file_path)
        print(f"Successfully loaded DIAN-TU data from {file_path}")
        print(f"Data shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print(f"Observations: {df['Observation'].unique()}")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def plot_centiloid_data(ax, df):
    """
    Plot Centiloid data on the given axis
    
    Parameters:
    -----------
    ax : matplotlib.axes.Axes
        Axis to plot on
    df : pandas.DataFrame
        DIAN-TU data filtered for Centiloid observations
    """
    # Filter for Centiloid data
    centiloid_data = df[df['Observation'] == 'Centiloid'].copy()
    
    # Convert time to numeric, handling 'OLE Baseline' as -0.5 years
    time_mapping = {'OLE Baseline': -0.5}
    centiloid_data['Time_numeric'] = centiloid_data['Time (years)'].map(time_mapping).fillna(centiloid_data['Time (years)'])
    
    # Sort by time
    centiloid_data = centiloid_data.sort_values('Time_numeric')
    
    # Extract data
    time = centiloid_data['Time_numeric'].values
    measurements = centiloid_data['measurement'].values
    sample_sizes = centiloid_data['n'].values
    
    # Plot the data (excluding baseline point)
    ax.plot(time[1:], measurements[1:], marker='o', linewidth=3, markersize=8, 
            color='#1f77b4', label='Gantenerumab')
    
    # Add sample sizes as text below points (excluding baseline)
    for i, (t, m, n) in enumerate(zip(time[1:], measurements[1:], sample_sizes[1:])):
        if not pd.isna(n):
            ax.text(t, m - 2, f'n={int(n)}', ha='center', va='top', fontsize=10)
    
    # Customize the plot
    ax.set_xlabel('Time (years)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Centiloid Change from Baseline', fontsize=14, fontweight='bold')
    ax.set_title('DIAN-TU: Amyloid PET (Centiloids)', fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Add horizontal line at y=0 (baseline reference)
    ax.axhline(y=0, color='black', linestyle='--', alpha=0.5, label='Baseline (y=62)')
    ax.legend(fontsize=12)
    
    # Set x-axis limits
    ax.set_xlim(-1, 3.5)

def plot_csf_data(ax, df):
    """
    Plot CSF AB42/40 CentiMarker data on the given axis
    
    Parameters:
    -----------
    ax : matplotlib.axes.Axes
        Axis to plot on
    df : pandas.DataFrame
        DIAN-TU data filtered for CSF observations
    """
    # Filter for CSF data
    csf_data = df[df['Observation'] == 'CSF AB42/40 CentiMarker'].copy()
    
    # Convert time to numeric, handling 'OLE Baseline' as -0.5 years
    time_mapping = {'OLE Baseline': -0.5}
    csf_data['Time_numeric'] = csf_data['Time (years)'].map(time_mapping).fillna(csf_data['Time (years)'])
    
    # Sort by time
    csf_data = csf_data.sort_values('Time_numeric')
    
    # Extract data
    time = csf_data['Time_numeric'].values
    measurements = csf_data['measurement'].values
    sample_sizes = csf_data['n'].values
    
    # Plot the data (excluding baseline point)
    ax.plot(time[1:], measurements[1:], marker='s', linewidth=3, markersize=8, 
            color='#1f77b4', label='Gantenerumab')
    
    # Add sample sizes as text below points (excluding baseline)
    for i, (t, m, n) in enumerate(zip(time[1:], measurements[1:], sample_sizes[1:])):
        if not pd.isna(n):
            ax.text(t, m - 2, f'n={int(n)}', ha='center', va='top', fontsize=10)
    
    # Customize the plot
    ax.set_xlabel('Time (years)', fontsize=14, fontweight='bold')
    ax.set_ylabel('CSF AB42/40 CentiMarker Change from Baseline', fontsize=14, fontweight='bold')
    ax.set_title('DIAN-TU: CSF AB42/40 CentiMarker', fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Add horizontal line at y=0 (baseline reference)
    ax.axhline(y=0, color='black', linestyle='--', alpha=0.5, label='Baseline (y=44)')
    ax.legend(fontsize=12)
    
    # Set x-axis limits
    ax.set_xlim(-1, 3.5)

def create_dian_tu_plots(df, save_plot=True):
    """
    Create a 2-panel plot showing both Centiloid and CSF data
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DIAN-TU data
    save_plot : bool, default True
        Whether to save the plot
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Plot Centiloid data
    plot_centiloid_data(ax1, df)
    
    # Plot CSF data
    plot_csf_data(ax2, df)
    
    plt.tight_layout()
    
    if save_plot:
        plt.savefig('figures/empirical_data/DIAN_TU_Gantenerumab.png', dpi=300, bbox_inches='tight')
        print("Plot saved as 'figures/empirical_data/DIAN_TU_Gantenerumab.png'")
    
    plt.show()

def explore_dian_tu_data(df):
    """
    Explore DIAN-TU data structure and statistics
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DIAN-TU data to explore
    """
    print("\n=== DIAN-TU DATA EXPLORATION ===")
    print(f"Data shape: {df.shape}")
    print(f"\nObservations: {df['Observation'].unique()}")
    print(f"Time points: {df['Time (years)'].unique()}")
    
    print(f"\nSummary by observation type:")
    for obs_type in df['Observation'].unique():
        obs_data = df[df['Observation'] == obs_type]
        print(f"\n{obs_type}:")
        print(f"  Number of observations: {len(obs_data)}")
        print(f"  Measurement range: {obs_data['measurement'].min():.4f} to {obs_data['measurement'].max():.4f}")
        print(f"  Mean measurement: {obs_data['measurement'].mean():.4f}")
        if not obs_data['n'].isna().all():
            print(f"  Mean sample size: {obs_data['n'].mean():.1f}")

# Main execution
if __name__ == "__main__":
    # Load DIAN-TU data
    data_dir = Path("data/SUVR")
    excel_file = data_dir / "DIAN-TU_GANT.xlsx"
    
    if excel_file.exists():
        print(f"Loading DIAN-TU data from {excel_file}")
        df = load_dian_tu_data(excel_file)
        
        if df is not None:
            # Explore the data
            explore_dian_tu_data(df)
            
            # Create the plots
            print("\nCreating DIAN-TU Gantenerumab plots...")
            create_dian_tu_plots(df)
            
    else:
        print(f"File not found: {excel_file}")
        print("Available files in data directory:")
        for file in data_dir.glob("*.xlsx"):
            print(f"  - {file.name}")
