# imports
import os

import pandas as pd
import matplotlib.pyplot as plt
import datetime

from run_all import make_subset
from plots import get_binned_data

def get_data():
    # import full dataset
    return pd.read_csv(os.path.abspath("data_for_regressions.csv"))

def get_data_matlab():
    # import full dataset
    data = pd.read_csv(os.path.abspath("data_from_matlab.csv"))

    # remove data with nans for water or urine arsenic
    print(data.shape[0])
    data = data[(~data['arsenic_ugl'].isnull())]
    data = data[(~data['urine_as'].isnull())] 
    print(data.shape[0])

    # add column for subsetting
    data['knew_well_as'] = False
    for i, row in data.iterrows():
        if ((datetime.datetime.strptime(row['interview_date'], '%Y-%m-%d') < datetime.datetime(2001, 1, 1)) or (row['well_id'] > 5000)):
            knew_well_as = False
        else:
            knew_well_as = True
        data.at[i, 'knew_well_as'] = knew_well_as

    return data

def make_plot(data, plotname):
    # get data subset
    not_know_subset = make_subset(data, 'did_not_know')
    print(not_know_subset.shape[0])
    may_know_subset = make_subset(data, 'may_have_known')
    print(may_know_subset.shape[0])

    # bin both and plot the binned data
    binned_data_may_know = get_binned_data(may_know_subset, 20, ['arsenic_ugl', 'urine_as'])
    binned_data_may_know.to_csv('temp_may_know.csv')
    binned_data_not_know = get_binned_data(not_know_subset, 20, ['arsenic_ugl', 'urine_as'])
    binned_data_not_know.to_csv('temp_not_know.csv')

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_ylabel(r'Urinary Arsenic ($\mu g/L$)', fontsize=18)
    ax.set_xlabel(r'Primary Well Arsenic ($\mu g/L$)', fontsize=18)
    ax.errorbar(binned_data_may_know['arsenic_ugl_mean'], binned_data_may_know['urine_as_mean'],
                xerr=binned_data_may_know['arsenic_ugl_sem'], yerr=binned_data_may_know['urine_as_sem'], 
                fmt='-ob', markersize=5, mfc='b', mec='none', ecolor='b', capsize=2)
    ax.errorbar(binned_data_not_know['arsenic_ugl_mean'], binned_data_not_know['urine_as_mean'],
                xerr=binned_data_not_know['arsenic_ugl_sem'], yerr=binned_data_not_know['urine_as_sem'], 
                fmt='-ok', markersize=5, mfc='k', mec='none', ecolor='k', capsize=2)
    #ax.set_xlim([0, xmax])
    #ax.set_ylim([0, ymax])
    ax.xaxis.set_ticks([0, 100, 200, 300, 400, 500])
    ax.yaxis.set_ticks([0, 100, 200, 300, 400, 500])
    ax.tick_params(axis='both', labelsize=16)
    plt.savefig(f'plots/{plotname}.png')

data = get_data()
make_plot(data, 'subset_comparison_binned')
