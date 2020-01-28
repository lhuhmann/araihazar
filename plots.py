import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
import scipy.stats as stats
import numpy as np

def make_plots(simple_results, two_slope_results, both_data, group_name, numbins, household_well_as):
    scatter_plot_simple_regress(simple_results, both_data, group_name)
    scatter_plot_multiple_regress(two_slope_results, both_data, group_name, household_well_as)
    binned_data = get_binned_data(both_data, numbins, household_well_as)
    plot_binned(binned_data, group_name, 'arsenic_ugl', 'urine_as_pred_simple', 
            400, 400, 'Primary Household Well Arsenic')
    plot_binned(binned_data, group_name, 'arsenic_ugl', 'urine_as_pred_multiple', 
            400, 400, 'Primary Household Well Arsenic')

def format_scatter_plot(ax):
    """Do formatting common to scatter plots from simple linear regression and multiple linear regression."""
    ax.tick_params(axis='both', labelsize=16)
    ax.set_ylabel(r'Urinary Arsenic ($\mu g/L$)', fontsize=18)
    ax.set_ylim([0,2500])
    ax.yaxis.set_ticks([0, 500, 1000, 1500, 2000, 2500])
    return ax

def scatter_plot_simple_regress(results, data, group_name):
    """Make scatter plot from simple linear regression results"""
    fig, ax = plt.subplots(figsize=(8,6))
    ax = format_scatter_plot(ax)
    ax.set_xlabel(r'Primary Household Well Arsenic ($\mu g/L$)', fontsize=18)
    ax.scatter(data.arsenic_ugl, data.urine_as, marker='o', s=5, c='k', alpha=.2, edgecolors='none')
    ax.scatter(data.arsenic_ugl, data['urine_as_pred_simple'], marker='o', s=5, c='r', edgecolors='none')
    ax.set_xlim([0,800])
    ax.xaxis.set_ticks([0, 200, 400, 600, 800])
    # using latex math formatting here according to https://matplotlib.org/tutorials/text/mathtext.html
    ax.add_artist(AnchoredText(r'$R^2 = ' + str(round(results.rsquared, 3)) + \
            '$\n$n = ' + str(int(results.nobs)) + \
            '$\n$slope = ' + str(round(results.params[1], 2)) + \
            '$\n$intercept = $' + str(int(results.params[0])),
            loc=2, frameon=False, prop=dict(size=14)))
    plt.savefig('plots/' + group_name + '_simple_regression.png')

def scatter_plot_multiple_regress(results, data, group_name, household_well_as):
    """Make scatter plot from multiple linear regression results"""
    fig, ax = plt.subplots(figsize=(8,6))
    ax = format_scatter_plot(ax)
    ax.set_xlabel(r'Primary Household Well Arsenic ($\mu g/L$)', fontsize=18)
    ax.scatter(data.arsenic_ugl, data.urine_as, marker='o', s=5, c='k', alpha=.2, edgecolors='none')
    ax.scatter(data.arsenic_ugl, data['urine_as_pred_multiple'], marker='o', s=5, c='r', edgecolors='none')
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
    ax.scatter(data[household_well_as], data.urine_as, marker='o', s=5, c='k', alpha=.2, edgecolors='none')
    ax.scatter(data[household_well_as], data['urine_as_pred_multiple'], marker='o', s=5, c='r', edgecolors='none')
    ax.set_xlim([0,350])
    ax.xaxis.set_ticks([0, 50, 100, 150, 200, 250, 300, 350])
    ax.add_artist(AnchoredText(r'$R^2 = ' + str(round(results.rsquared, 3)) + \
            '$\n$n = ' + str(int(results.nobs)) + \
            '$\n$slope_{50mWellAverage} = ' + str(round(results.params[1], 2)) + \
            '$\n$intercept = $' + str(int(results.params[0])),
            loc=2, frameon=False, prop=dict(size=14)))
    plt.savefig('plots/' + group_name + '_two_slope_regression_compound_wells.png')

def get_average(data, colname, first_index, last_index):
    return np.mean(data.loc[first_index:last_index, colname])

def get_sem(data, colname, first_index, last_index):
    return stats.sem(data.loc[first_index:last_index, colname])

def add_values(data, binned_data, first_index, last_index, household_well_as):
    val_dict = {}
    for colname in ['arsenic_ugl', household_well_as, 'urine_as', 'urine_as_pred_simple', 
                       'urine_as_pred_multiple']:
        val_dict[colname + '_mean'] = get_average(data, colname, first_index, last_index)
        val_dict[colname + '_sem'] = get_sem(data, colname, first_index, last_index)
    binned_data = binned_data.append(val_dict, ignore_index=True)
    #print(binned_data)
    return binned_data

def get_binned_data(data, nbins, household_well_as):
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
            binned_data = add_values(data, binned_data, first_index, last_index, household_well_as)
    i += 1
    first_index = i*bin_size
    last_index = n_tot
    # print(n_tot, first_index, last_index)
    binned_data = add_values(data, binned_data, first_index, last_index, household_well_as)
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