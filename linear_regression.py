#%% package imports
import pandas as pd
import os
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import scipy.stats as stats

from matplotlib.offsetbox import AnchoredText
from statsmodels.sandbox.regression.predstd import wls_prediction_std

#%% define parameters
# pick which column to use for neighbor well arsenic
neighbor_well_as = "other_as_50m"
#%% file imports

# people data
data = pd.read_csv(os.path.abspath("data_for_regressions_female.csv"))
# print(data.head(5))

#%% plot formatting
def format_scatter_plot(ax):
    ax.tick_params(axis='both', labelsize=16)
    ax.set_ylabel(r'Urinary Arsenic ($\mu g/L$)', fontsize=18)
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
    ax.set_xlabel(r'Primary Household Well Arsenic ($\mu g/L$)', fontsize=18)
    ax.scatter(data.arsenic_ugl, data.urine_as, marker='o', s=5, c='k', alpha=.2, edgecolors='none')
    ax.scatter(data.arsenic_ugl, urine_as_pred, marker='o', s=5, c='r', edgecolors='none')
    ax.set_xlim([0,800])
    ax.xaxis.set_ticks([0, 200, 400, 600, 800])
    # using latex math formatting here according to https://matplotlib.org/tutorials/text/mathtext.html
    ax.add_artist(AnchoredText(r'$R^2 = ' + str(round(results.rsquared, 3)) + \
            '$\n$n = ' + str(int(results.nobs)) + \
            '$\n$slope = ' + str(round(results.params[1], 2)) + \
            '$\n$intercept = $' + str(int(results.params[0])),
            loc=2, frameon=False, prop=dict(size=14)))
    plt.savefig('plots/' + group_name + '_simple_regression.png')

    data['urine_as_pred_simple'] = urine_as_pred
    return data, results

#%% add wells in family compound
def two_slope_regress(data, group_name):
    # need to add a column of ones to the x-data to get a constant term in the model
    x = sm.add_constant(pd.concat([data.arsenic_ugl, data[neighbor_well_as]], axis=1))

    model = sm.OLS(data.urine_as, x)
    results = model.fit()
    print(results.summary())

    urine_as_pred = results.params[1]*data.arsenic_ugl + \
                    results.params[2]*data[neighbor_well_as] + \
                    results.params[0]

    fig, ax = plt.subplots(figsize=(8,6))
    ax = format_scatter_plot(ax)
    ax.set_xlabel(r'Primary Household Well Arsenic ($\mu g/L$)', fontsize=18)
    ax.scatter(data.arsenic_ugl, data.urine_as, marker='o', s=5, c='k', alpha=.2, edgecolors='none')
    ax.scatter(data.arsenic_ugl, urine_as_pred, marker='o', s=5, c='r', edgecolors='none')
    ax.set_xlim([0,800])
    ax.xaxis.set_ticks([0, 200, 400, 600, 800])
    ax.add_artist(AnchoredText(r'$R^2 = ' + str(round(results.rsquared, 3)) + \
            '$\n$n = ' + str(int(results.nobs)) + \
            '$\n$slope_{PrimaryWell} = ' + str(round(results.params[1], 2)) + \
            '$\n$intercept = $' + str(int(results.params[0])),
            loc=2, frameon=False, prop=dict(size=14)))
    plt.savefig('plots/' + group_name + '_two_slope_regression_primary_well.png')

    fig, ax = plt.subplots(figsize=(8,6))
    ax.set_xlabel(r'Average Arsenic of Wells within 50 m ($\mu g/L$)', fontsize=18)
    ax = format_scatter_plot(ax)
    ax.scatter(data[neighbor_well_as], data.urine_as, marker='o', s=5, c='k', alpha=.2, edgecolors='none')
    ax.scatter(data[neighbor_well_as], urine_as_pred, marker='o', s=5, c='r', edgecolors='none')
    ax.set_xlim([0,350])
    ax.xaxis.set_ticks([0, 50, 100, 150, 200, 250, 300, 350])
    ax.add_artist(AnchoredText(r'$R^2 = ' + str(round(results.rsquared, 3)) + \
            '$\n$n = ' + str(int(results.nobs)) + \
            '$\n$slope_{50mWellAverage} = ' + str(round(results.params[1], 2)) + \
            '$\n$intercept = $' + str(int(results.params[0])),
            loc=2, frameon=False, prop=dict(size=14)))
    plt.savefig('plots/' + group_name + '_two_slope_regression_compound_wells.png')

    data['urine_as_pred_multiple'] = urine_as_pred
    return data, results

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
subset_data_with_pred_simple, subset_model_simple = simple_regress(subset_data, 'subset')
subset_data_with_pred_both, subset_model_multiple = two_slope_regress(subset_data_with_pred_simple, 'subset')
# three_slope_regress(subset_data, 'subset')

# 2. all participants
all_data_with_pred_simple, all_model_simple = simple_regress(data, 'all')
all_data_with_pred_both, all_model_multiple = two_slope_regress(data, 'all')
# three_slope_regress(data, 'all')

#%% get the binned plots

def get_average(data, colname, first_index, last_index):
    return np.mean(data.loc[first_index:last_index, colname])

def get_sem(data, colname, first_index, last_index):
    return stats.sem(data.loc[first_index:last_index, colname])

def add_values(data, binned_data, first_index, last_index):
    val_dict = {}
    for colname in ['arsenic_ugl', neighbor_well_as, 'urine_as', 'urine_as_pred_simple', 
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
    data = data.sort_values(by=['arsenic_ugl'])
    data = data.reset_index(drop=True)
    binned_data = pd.DataFrame()
    n_tot = data.shape[0]
    bin_size = n_tot//nbins
    # print('bin size is' + str(bin_size))
    for i in range(0,nbins-1):
            # index of first and last item in bin
            first_index = i*bin_size
            last_index = (i+1)*bin_size-1
            # print(n_tot, first_index, last_index)
            binned_data = add_values(data, binned_data, first_index, last_index)
    i += 1
    first_index = i*bin_size
    last_index = n_tot
    # print(n_tot, first_index, last_index)
    binned_data = add_values(data, binned_data, first_index, last_index)
    # print(binned_data.columns)
    return binned_data

def plot_binned(data, group_name, xvar, yvar, xmax, ymax, xlabel):
    fig, ax = plt.subplots(figsize=(8,6))
    ax.set_ylabel(r'Urinary Arsenic ($\mu g/L$)', fontsize=18)
    ax.set_xlabel(xlabel + r' ($\mu g/L$)', fontsize=18)
    ax.errorbar(data[xvar + '_mean'], data.urine_as_mean, 
                yerr=data.urine_as_sem, xerr=data[xvar + '_sem'],
                fmt='o', markersize=5, mfc='k', mec='none', ecolor='k', capsize=2)
    ax.errorbar(data[xvar + '_mean'], data[yvar+'_mean'], 
                yerr=data[yvar+'_sem'], xerr=data[xvar+'_sem'],
                fmt='o', markersize=5, mfc='r', mec='none', ecolor='r', capsize=2)
    ax.set_xlim([0,xmax])
    ax.set_ylim([0,ymax])
    ax.xaxis.set_ticks([0, 100, 200, 300, 400])
    ax.yaxis.set_ticks([0, 100, 200, 300, 400])
    ax.tick_params(axis='both', labelsize=16)
    plt.savefig('plots/' + group_name + '_' + xvar + '_' + yvar + '_binned.png')
        
# binned urine as vs primary well As for subset
subset_binned_data = get_binned_data(subset_data_with_pred_both, 15)
plot_binned(subset_binned_data, 'subset', 'arsenic_ugl', 'urine_as_pred_simple', 
            400, 400, 'Primary Household Well Arsenic')
plot_binned(subset_binned_data, 'subset', 'arsenic_ugl', 'urine_as_pred_multiple', 
            400, 400, 'Primary Household Well Arsenic')
plot_binned(subset_binned_data, 'subset', neighbor_well_as, 'urine_as_pred_multiple',
            400, 400, 'Average Arsenic of Wells within 50 m')

# binned urine as vs primary well As for all
all_binned_data = get_binned_data(all_data_with_pred_both, 15)
plot_binned(all_binned_data,'all', 'arsenic_ugl', 'urine_as_pred_simple', 
            400, 400, 'Primary Household Well Arsenic')
plot_binned(all_binned_data,'all', 'arsenic_ugl', 'urine_as_pred_multiple', 
            400, 400, 'Primary Household Well Arsenic')
plot_binned(all_binned_data, 'all', neighbor_well_as, 'urine_as_pred_multiple',
            400, 400, 'Average Arsenic of Wells within 50 m')

# compare binned data for subset vs all
fig, ax = plt.subplots(figsize=(8,6))
ax.set_ylabel(r'Urinary Arsenic ($\mu g/L$)', fontsize=18)
ax.set_xlabel(r'Primary Household Well Arsenic ($\mu g/L$)', fontsize=18)
ax.errorbar(all_binned_data['arsenic_ugl_mean'], all_binned_data['urine_as_mean'], 
            yerr=all_binned_data['urine_as_sem'], xerr=all_binned_data['arsenic_ugl_sem'],
            fmt='o', markersize=5, mfc='b', mec='none', ecolor='b', capsize=2)
ax.errorbar(subset_binned_data['arsenic_ugl_mean'], subset_binned_data['urine_as_mean'], 
            yerr=subset_binned_data['urine_as_sem'], xerr=subset_binned_data['arsenic_ugl_sem'],
            fmt='o', markersize=5, mfc='k', mec='none', ecolor='k', capsize=2)
# ax.set_xlim([0,xmax])
# ax.set_ylim([0,ymax])
ax.xaxis.set_ticks([0, 100, 200, 300, 400])
ax.yaxis.set_ticks([0, 100, 200, 300, 400])
ax.tick_params(axis='both', labelsize=16)
plt.savefig('plots/all_subset_comparison_binned.png')


#%% solve for fu and fp
# simple linear regression, distributed well model

# constant parameters
# mass fraction of water consumed via food
ff = 0.2
# mass fraction of water produced from cellular respiration
fc = 0.12
# mass fraction of arsenic lost to defection, 
md = 0.06
# mass fraction of arsenic lost to a sink in the body
mb = 0
# Mf/Q, mass of arsenic consumed via food, ug/d
Mf = 96
Q = 2.6
# average arsenic of all private wells in the data set (proxy for all wells in the study area), ug/L
avgAs = 95

def solve_fracs_simple(model):
    # slope (primary well arsenic)
    slope = model.params[1]
    # intercept
    intercept = model.params[0]

    # solve for fp, fu, and fo
    fp = (slope*(1-ff-fc)*avgAs+Mf/Q)/(slope*avgAs+intercept)
    fu = (1-md-mb)*(fp/slope)
    fo = 1 - fp - ff - fc

    frac_primary_well = fp/(fp+fo)
    frac_other_well = fo/(fp+fo)
    return {'fu':fu, 'fp':fp, 'fo':fo, 
            'frac_primary_well':frac_primary_well, 
            'frac_other_well':frac_other_well}

def solve_fracs_multiple(model):
    # slope (primary well arsenic)
    slope_primary = model.params[1]
    # slope (neighbor well arsenic)
    slope_neighbor = model.params[2]
    # intercept
    intercept = model.params[0]

    # solve for fp, fu, fo, fn
    fu = (1 - md - mb)*(1 - ff - fc + Mf/Q/avgAs)/(slope_primary + slope_neighbor + intercept/avgAs)
    fp = slope_primary*(1 - ff - fc + Mf/Q/avgAs)/(slope_primary + slope_neighbor + intercept/avgAs)
    fo = intercept*(1 - ff - fc + Mf/Q/avgAs)/(slope_primary*avgAs + slope_neighbor*avgAs + intercept) - Mf/Q/avgAs
    fn = 1 - fp - fo - ff - fc
    frac_primary_well = fp/(fp+fo+fn)
    frac_other_well = fo/(fp+fo+fn)
    frac_neighbor_well = fn/(fp+fo+fn)
    return {'fu':fu, 'fp':fp, 'fo':fo, 'fn':fn,
            'frac_primary_well':frac_primary_well, 
            'frac_other_well':frac_other_well,
            'frac_neighbor_well':frac_neighbor_well}

subset_simple_fracs = solve_fracs_simple(subset_model_simple)
print(subset_simple_fracs)
subset_multiple_fracs = solve_fracs_multiple(subset_model_multiple)
print(subset_multiple_fracs)

all_simple_fracs = solve_fracs_simple(all_model_simple)
print(all_simple_fracs)
all_multiple_fracs = solve_fracs_multiple(all_model_multiple)
print(all_multiple_fracs)





