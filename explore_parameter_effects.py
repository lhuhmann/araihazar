import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
import scipy.stats as stats
import numpy as np

from plots import get_binned_data
from compare_subsets import make_subset

# set parameters
data = pd.read_csv('../araihazar-data/to_analyze/data_for_regressions.csv')
group_name = 'did_not_know'
data_subset = make_subset(data, group_name)
numbins = 15
household_well_as = 'other_as_50m'

names = ['reference_case', 'fu=0.5', 'Mf=64', 'fp=0.5', 'ff_and_fc', 'md']
slopes = [1, 2, 1, .5, .68, 1]
intercepts = [0, 0, 64/3, 50, 0, 0]
colors = [(.18, .33, .59), (.18, .33, .59), (.18, .33, .59), (.18, .33, .59), 'tab:red', 'tab:red']

# bin data
binned_data = get_binned_data(data_subset, numbins,
                              ['arsenic_ugl', 'urine_as'])
for i in range(len(names)):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_ylabel(r'Urinary Arsenic ($\mu g/L$)', fontsize=18)
    ax.set_xlabel(r'Primary Household Well Arsenic ($\mu g/L$)', fontsize=18)
    # zorder=1 is needed to ensure the fit line is in front of the markers, as discussed in https://github.com/matplotlib/matplotlib/issues/409
    ax.errorbar(binned_data['arsenic_ugl_mean'], binned_data.urine_as_mean, 
                yerr=binned_data.urine_as_sem, xerr=binned_data['arsenic_ugl_sem'],
                fmt='o', markersize=10, mfc='k', mec='none', ecolor='k', capsize=2, zorder=1)
    ax.plot(np.linspace(0, 1000, 100), np.linspace(0, 1000, 100)*slopes[i] + intercepts[i], 
            color=colors[i], linewidth=3)
    ax.set_xlim([0, 400])
    ax.set_ylim([0, 400])
    ax.xaxis.set_ticks([0, 100, 200, 300, 400])
    ax.yaxis.set_ticks([0, 100, 200, 300, 400])
    ax.tick_params(axis='both', labelsize=16)
    plt.savefig(f'plots/explore_params/{names[i]}.png', dpi=600, transparent=True)
