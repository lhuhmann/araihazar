import os
import pandas as pd
import matplotlib.pyplot as plt

def scatter_plot_multiple_regress(group1, group2, data_group1, data_group2):
    """Make scatter plot comparing predictions from two groups"""
    fig, ax = plt.subplots(figsize=(8,6))
    ax.tick_params(axis='both', labelsize=16)
    ax.set_ylabel(r'Predicted Urinary Arsenic ($\mu g/L$)', fontsize=18)
    #ax.set_ylim([0,2500])
    #ax.yaxis.set_ticks([0, 500, 1000, 1500, 2000, 2500])
    ax.set_xlabel(r'Primary Household Well Arsenic ($\mu g/L$)', fontsize=18)
    ax.scatter(data_group2.arsenic_ugl, data_group2.urine_as_pred_multiple, 
        marker='o', s=5, c='r', alpha=.2, edgecolors='none')
    ax.scatter(data_group1.arsenic_ugl, data_group1.urine_as_pred_multiple, 
        marker='o', s=5, c='k', alpha=.2, edgecolors='none')

    #ax.set_xlim([0,800])
    #ax.xaxis.set_ticks([0, 200, 400, 600, 800])
    plt.savefig('plots/' + group1 + '_' + group2 + '_predicted_as_comparison.png')

subset_data = pd.read_csv(os.path.abspath("did_not_know_urine_as_pred_multiple.csv"))
all_data = pd.read_csv(os.path.abspath("all_urine_as_pred_multiple.csv"))

scatter_plot_multiple_regress('subset', 'all', subset_data, all_data)