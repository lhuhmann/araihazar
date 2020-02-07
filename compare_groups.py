# imports
import os

import pandas as pd
import matplotlib.pyplot as plt

from run_all import make_subset
from plots import get_binned_data

# import full dataset
data = pd.read_csv(os.path.abspath("data_for_regressions.csv"))

# get data subset
data_subset = make_subset(data, 'did_not_know')

# bin both and plot the binned data
binned_data = get_binned_data(data, 20, ['arsenic_ugl', 'urine_as'])
binned_data_subset = get_binned_data(data_subset, 20, ['arsenic_ugl', 'urine_as'])

fig, ax = plt.subplots(figsize=(8, 6))
ax.set_ylabel(r'Urinary Arsenic ($\mu g/L$)', fontsize=18)
ax.set_xlabel(r'Primary Well Arsenic ($\mu g/L$)', fontsize=18)
ax.errorbar(binned_data['arsenic_ugl_mean'], binned_data['urine_as_mean'],
            yerr=binned_data['urine_as_sem'], xerr=binned_data['arsenic_ugl_sem'],
            fmt='o', markersize=5, mfc='k', mec='none', ecolor='k', capsize=2)
ax.errorbar(binned_data_subset['arsenic_ugl_mean'], binned_data_subset['urine_as_mean'],
            yerr=binned_data_subset['urine_as_sem'], xerr=binned_data_subset['arsenic_ugl_sem'],
            fmt='o', markersize=5, mfc='b', mec='none', ecolor='b', capsize=2)
#ax.set_xlim([0, xmax])
#ax.set_ylim([0, ymax])
ax.xaxis.set_ticks([0, 100, 200, 300, 400])
ax.yaxis.set_ticks([0, 100, 200, 300, 400])
ax.tick_params(axis='both', labelsize=16)
plt.savefig('plots/subset_full_comparison_binned.png')
