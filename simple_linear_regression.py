#%% package imports
import pandas as pd
import os
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import scipy.stats as stats

from matplotlib.offsetbox import AnchoredText
from statsmodels.sandbox.regression.predstd import wls_prediction_std

#%% file imports

# people data
data = pd.read_csv(os.path.abspath("data_for_regressions.csv"))
# print(data.head(5))

#%% plot formatting
def format_scatter_plot(ax):
    ax.tick_params(axis='both', labelsize=16)
    ax.set_ylabel(r'Urinary Arsenic ($\mu g/L$)', fontsize=16)
    ax.set_ylim([0,2500])
    ax.yaxis.set_ticks([0, 500, 1000, 1500, 2000, 2500])
    return ax
    
#%% base case
def simple_regress(data, group_name):
    # need to add a column of ones to the x-data to get a constant term in the model
    x = sm.add_constant(data.arsenic_ugl)

    model = sm.OLS(data.urine_as, x)
    results = model.fit()
    print(results.summary())

    urine_as_pred = results.params[1]*data.arsenic_ugl + results.params[0]
    fig, ax = plt.subplots(figsize=(8,6))

    ax = format_scatter_plot(ax)
    ax.set_xlabel(r'Primary Household Well Arsenic ($\mu g/L$)', fontsize=16)
    ax.scatter(data.arsenic_ugl, data.urine_as, marker='o', s=5, c='k', alpha=.2, edgecolors='none')
    ax.scatter(data.arsenic_ugl, urine_as_pred, marker='o', s=5, c='r', edgecolors='none')
    ax.set_xlim([0,800])
    ax.xaxis.set_ticks([0, 200, 400, 600, 800])
    # using latex math formatting here according to https://matplotlib.org/tutorials/text/mathtext.html
    ax.add_artist(AnchoredText(r'$R^2 = ' + str(round(results.rsquared, 3)) + \
            '$\n$n = ' + str(int(results.nobs)) + \
            '$\n$slope = ' + str(round(results.params[1], 2)) + \
            '$\n$intercept = $' + str(int(results.params[0])),
            loc=2, frameon=False))
    plt.savefig(group_name + '_simple_regression.png')

    data['urine_as_pred_simple'] = urine_as_pred
    return data

#%% add wells in family compound
def two_slope_regress(data, group_name):
    # need to add a column of ones to the x-data to get a constant term in the model
    x = sm.add_constant(pd.concat([data.arsenic_ugl, data.other_as_50m], axis=1))

    model = sm.OLS(data.urine_as, x)
    results = model.fit()
    print(results.summary())

    urine_as_pred = results.params[1]*data.arsenic_ugl + \
                    results.params[2]*data.other_as_50m + \
                    results.params[0]

    fig, ax = plt.subplots(figsize=(8,6))
    ax = format_scatter_plot(ax)
    ax.set_xlabel(r'Primary Household Well Arsenic ($\mu g/L$)', fontsize=16)
    ax.scatter(data.arsenic_ugl, data.urine_as, marker='o', s=5, c='k', alpha=.2, edgecolors='none')
    ax.scatter(data.arsenic_ugl, urine_as_pred, marker='o', s=5, c='r', edgecolors='none')
    ax.set_xlim([0,800])
    ax.xaxis.set_ticks([0, 200, 400, 600, 800])
    ax.add_artist(AnchoredText(r'$R^2 = ' + str(round(results.rsquared, 3)) + \
            '$\n$n = ' + str(int(results.nobs)) + \
            '$\n$slope_{PrimaryWell} = ' + str(round(results.params[1], 2)) + \
            '$\n$intercept = $' + str(int(results.params[0])),
            loc=2, frameon=False))
    plt.savefig(group_name + '_two_slope_regression_primary_well.png')

    fig, ax = plt.subplots(figsize=(8,6))
    ax.set_xlabel(r'Average Arsenic of Wells within 50 m ($\mu g/L$)', fontsize=16)
    ax = format_scatter_plot(ax)
    ax.scatter(data.other_as_50m, data.urine_as, marker='o', s=5, c='k', alpha=.2, edgecolors='none')
    ax.scatter(data.other_as_50m, urine_as_pred, marker='o', s=5, c='r', edgecolors='none')
    ax.set_xlim([0,350])
    ax.xaxis.set_ticks([0, 50, 100, 150, 200, 250, 300, 350])
    ax.add_artist(AnchoredText(r'$R^2 = ' + str(round(results.rsquared, 3)) + \
            '$\n$n = ' + str(int(results.nobs)) + \
            '$\n$slope_{50mWellAverage} = ' + str(round(results.params[1], 2)) + \
            '$\n$intercept = $' + str(int(results.params[0])),
            loc=2, frameon=False))
    plt.savefig(group_name + '_two_slope_regression_compound_wells.png')

    data['urine_as_pred_multiple'] = urine_as_pred
    return data

# #%% add wells beyond family compound
# def three_slope_regress(data, group_name):
#     # need to add a column of ones to the x-data to get a constant term in the model
#     x = sm.add_constant(pd.concat([data.arsenic_ugl, data.other_as_50m, data.other_as_hyp_beyond_50], axis=1))

#     model = sm.OLS(data.urine_as, x)
#     results = model.fit()
#     print(results.summary())

#     urine_as_pred = results.params[1]*data.arsenic_ugl + \
#                     results.params[2]*data.other_as_50m + \
#                     results.params[2]*data.other_as_hyp_beyond_50 + \
#                     results.params[0]

#     fig, ax = plt.subplots(figsize=(8,6))
#     ax.plot(data.arsenic_ugl, data.urine_as)
#     ax.plot(data.arsenic_ugl, urine_as_pred, 'b-')
#     plt.savefig(group_name + '_three_slope_regression_primary_well.png')

#     fig, ax = plt.subplots(figsize=(8,6))
#     ax.plot(data.other_as_50m, data.urine_as, marker='o', s=5, c='k', alpha=.2, edgecolors='none')
#     ax.plot(data.other_as_50m, urine_as_pred, 'b-')
#     plt.savefig(group_name + '_three_slope_regression_compound_wells.png')

#     fig, ax = plt.subplots(figsize=(8,6))
#     ax.plot(data.other_as_hyp_beyond_50, data.urine_as, marker='o', s=5, c='k', alpha=.2, edgecolors='none')
#     ax.plot(data.other_as_hyp_beyond_50, urine_as_pred, 'b-')
#     plt.savefig(group_name + '_three_slope_regression_distant_wells.png')

#%% run regressions on:

# keep only the rows where people did not know their well As when their urine As was measured
subset_data = data[data['knew_well_as'] == False]

# 1. participants who did not know their well As
subset_data_with_pred_simple = simple_regress(subset_data, 'subset')
subset_data_with_pred_both = two_slope_regress(subset_data_with_pred_simple, 'subset')
# three_slope_regress(subset_data, 'subset')

# 2. all participants
all_data_with_pred_simple = simple_regress(data, 'all')
all_data_with_pred_both = two_slope_regress(data, 'all')
# three_slope_regress(data, 'all')

#%% get the binned plots

def get_average(data, colname, first_index, last_index):
    return np.mean(data.loc[first_index:last_index, colname])

def get_sem(data, colname, first_index, last_index):
    return stats.sem(data.loc[first_index:last_index, colname])

def add_values(data, binned_data, first_index, last_index):
    val_dict = {}
    for colname in ['arsenic_ugl', 'other_as_50m', 'urine_as', 'urine_as_pred_simple', 
                       'urine_as_pred_multiple']:
        val_dict[colname + '_mean'] = get_average(data, colname, first_index, last_index)
        val_dict[colname + '_sem'] = get_sem(data, colname, first_index, last_index)
    binned_data = binned_data.append(val_dict, ignore_index=True)
    #print(binned_data)
    return binned_data

def get_binned_data(data, nbins):
    #print(data.index)
    #print(data.head(5))
    #print(data.index.is_monotonic_increasing)
    data = data.reset_index(drop=True)
    data = data.sort_values(by=['urine_as'])
    data = data.reset_index(drop=True)
    binned_data = pd.DataFrame()
    n_tot = data.shape[0]
    bin_size = n_tot//nbins
    print('bin size is' + str(bin_size))
    for i in range(0,nbins-1):
            # index of first and last item in bin
            first_index = i*bin_size
            last_index = (i+1)*bin_size-1
            print(n_tot, first_index, last_index)
            binned_data = add_values(data, binned_data, first_index, last_index)
    i += 1
    first_index = i*bin_size
    last_index = n_tot
    print(n_tot, first_index, last_index)
    binned_data = add_values(data, binned_data, first_index, last_index)
    print(binned_data.head(5))
    return binned_data
        
# binned urine as vs primary well As for subset
subset_binned_data = get_binned_data(subset_data_with_pred_both, 10)

# binned urine as vs primary well As for all
all_binned_data = get_binned_data(all_data_with_pred_both, 10)


