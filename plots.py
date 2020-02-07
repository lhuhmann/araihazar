import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
import scipy.stats as stats
import numpy as np

def make_plots(distributed_results, distributed_params, household_results, household_params, data, group_name, numbins, household_well_as):
    """Make plots from model results."""
    # scatter plots of individual data points
    scatter_plot_simple_regress(distributed_results, data, group_name)
    scatter_plot_multiple_regress(household_results, data, group_name, household_well_as)
    # scatter plots of binned data
    binned_data = get_binned_data(data, numbins, ['arsenic_ugl', household_well_as, 'urine_as', 'urine_as_pred_distributed',
                    'urine_as_pred_household'])
    plot_binned(binned_data, group_name, 'arsenic_ugl', 'urine_as_pred_distributed',
                400, 400, 'Primary Household Well Arsenic')
    plot_binned(binned_data, group_name, 'arsenic_ugl', 'urine_as_pred_household',
                400, 400, 'Primary Household Well Arsenic')
    # area plot of contributions (for distributed model only)
    plot_contributions(data, distributed_params, group_name)
    plot_contributions_percentile(data, distributed_params, group_name)

def format_scatter_plot(ax):
    """Do formatting common to scatter plots from all models."""
    ax.tick_params(axis='both', labelsize=16)
    ax.set_ylabel(r'Urinary Arsenic ($\mu g/L$)', fontsize=18)
    ax.set_ylim([0, 2500])
    ax.yaxis.set_ticks([0, 500, 1000, 1500, 2000, 2500])
    return ax

def scatter_plot_simple_regress(results, data, group_name):
    """Make scatter plot from distributed wells model results"""
    fig, ax = plt.subplots(figsize=(8, 6))
    ax = format_scatter_plot(ax)
    ax.set_xlabel(r'Primary Household Well Arsenic ($\mu g/L$)', fontsize=18)
    ax.scatter(data.arsenic_ugl, data.urine_as, marker='o', s=5, c='k', alpha=.2, edgecolors='none')
    ax.scatter(data.arsenic_ugl, data['urine_as_pred_distributed'], marker='o', s=5, c='r', edgecolors='none')
    ax.set_xlim([0, 800])
    ax.xaxis.set_ticks([0, 200, 400, 600, 800])
    # using latex math formatting according to https://matplotlib.org/tutorials/text/mathtext.html
    ax.add_artist(AnchoredText(
            fr'$R^2 = {results.rsquared:.2f}$' +
            '\n' +
            fr'$n = {int(results.nobs)}$' +
            '\n' +
            fr'$slope = {results.params[1]:.2f}$' +
            '\n' +
            fr'$intercept = {results.params[0]:.0f}$',
            loc=2, frameon=False, prop=dict(size=14)))
    plt.savefig('plots/' + group_name + '_distributed_model.png')

def scatter_plot_multiple_regress(results, data, group_name, household_well_as):
    """Make scatter plots from household well model results"""
    # urinary As vs primary well As
    fig, ax = plt.subplots(figsize=(8, 6))
    ax = format_scatter_plot(ax)
    ax.set_xlabel(r'Primary Household Well Arsenic ($\mu g/L$)', fontsize=18)
    ax.scatter(data.arsenic_ugl, data.urine_as, marker='o', s=5, c='k', alpha=.2, edgecolors='none')
    ax.scatter(data.arsenic_ugl, data['urine_as_pred_household'], marker='o', s=5, c='r', edgecolors='none')
    ax.set_xlim([0, 800])
    ax.xaxis.set_ticks([0, 200, 400, 600, 800])
    ax.add_artist(AnchoredText(
            fr'$R^2 = {results.rsquared:.3f}$' +
            '\n' +
            fr'$n = {int(results.nobs)}$' +
            '\n' +
            fr'$slope_{{PrimaryWell}} = {results.params[1]:.2f}$' +
            '\n' +
            fr'$intercept = {results.params[0]:.0f}$',
            loc=2, frameon=False, prop=dict(size=14)))
    plt.savefig('plots/' + group_name + '_household_model_primary_well.png')

    # urinary As vs household well As
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlabel(r'Average Arsenic of Household Wells ($\mu g/L$)', fontsize=18)
    ax = format_scatter_plot(ax)
    ax.scatter(data[household_well_as], data.urine_as, marker='o',
               s=5, c='k', alpha=.2, edgecolors='none')
    ax.scatter(data[household_well_as], data['urine_as_pred_household'],
               marker='o', s=5, c='r', edgecolors='none')
    ax.set_xlim([0, 350])
    ax.xaxis.set_ticks([0, 50, 100, 150, 200, 250, 300, 350])
    ax.add_artist(AnchoredText(
                  fr'$R^2 = {results.rsquared:.3f}$' +
                  '\n' +
                  fr'$n = {int(results.nobs)}$' +
                  '\n' +
                  fr'$slope_{{HouseholdWellAverage}} = {results.params[1]:.2f}$' +
                  '\n' +
                  fr'$intercept = {results.params[0]:.0f}$',
                  loc=2, frameon=False, prop=dict(size=14)))
    plt.savefig('plots/' + group_name + '_household_model_household_wells.png')

def get_mean_sem_dict(data, first_index, last_index, columns):
    """Return a dict containing the means and sems for a given bin"""
    mean_sem_dict = {}
    for colname in columns:
        mean_sem_dict[colname + '_mean'] = np.mean(data.loc[first_index:last_index, colname])
        mean_sem_dict[colname + '_sem'] = stats.sem(data.loc[first_index:last_index, colname])
    return mean_sem_dict

def get_binned_data(data, nbins, columns):
    """Divide data into nbins bins by primary well arsenic concentration and get average and sem for each bin.
    If data does not divide evenly into bins, 'extra' data is included in the final bin."""
    data = data.reset_index(drop=True)
    data = data.sort_values(by=['arsenic_ugl'])
    data = data.reset_index(drop=True)
    binned_data = pd.DataFrame()
    n_tot = data.shape[0]
    bin_size = n_tot//nbins
    # get mean and sem for each bin
    for i in range(0, nbins-1):
        # index of first and last item in bin
        first_index = i*bin_size
        last_index = (i+1)*bin_size-1
        # final bin may have 'extra' data
        if i == nbins - 1:
            last_index = n_tot
        binned_data = binned_data.append(get_mean_sem_dict(data, first_index, last_index, columns), ignore_index=True)
    return binned_data

def plot_binned(data, group_name, xvar, yvar, xmax, ymax, xlabel):
    """Plot binned data."""
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_ylabel(r'Urinary Arsenic ($\mu g/L$)', fontsize=18)
    ax.set_xlabel(xlabel + r' ($\mu g/L$)', fontsize=18)
    ax.errorbar(data[xvar + '_mean'], data.urine_as_mean, 
                yerr=data.urine_as_sem, xerr=data[xvar + '_sem'],
                fmt='o', markersize=5, mfc='k', mec='none', ecolor='k', capsize=2)
    ax.errorbar(data[xvar + '_mean'], data[yvar+'_mean'],
                yerr=data[yvar+'_sem'], xerr=data[xvar+'_sem'],
                fmt='o', markersize=5, mfc='r', mec='none', ecolor='r', capsize=2)
    ax.set_xlim([0, xmax])
    ax.set_ylim([0, ymax])
    ax.xaxis.set_ticks([0, 100, 200, 300, 400])
    ax.yaxis.set_ticks([0, 100, 200, 300, 400])
    ax.tick_params(axis='both', labelsize=16)
    plt.savefig('plots/' + group_name + '_' + xvar + '_' + yvar + '_binned.png')

def plot_contributions(data, params, group_name):
    # varies with an individual's primary well arsenic concentration
    contrib_primary_well = params['fp'][0]*data['arsenic_ugl']
    contrib_primary_well = contrib_primary_well.to_numpy().astype(float)
    # both of these are constant across individuals, since we don't have a way to estimate them more granularly
    contrib_other_well = np.repeat(params['fo'][0]*params['avgAs'][0], contrib_primary_well.shape[0])
    contrib_other_well = contrib_other_well.astype(float)
    contrib_food = np.repeat(params['Mf'][0]/params['Q'][0], contrib_primary_well.shape[0])
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_ylabel(r'Contribution to Urinary Arsenic ($\mu g/L$)', fontsize=18)
    ax.set_xlabel(r'Primary Household Well Arsenic Concentration ($\mu g/L$)', fontsize=18)
    print(max(data['arsenic_ugl']))
    ax.stackplot(data['arsenic_ugl'].to_numpy().astype(float), contrib_primary_well, contrib_other_well, contrib_food)
    plt.savefig('plots/' + group_name + '_contrib_plot.png')
    # fig, ax = plt.subplots(figsize=(8, 6))
    # ax.stackplot([1, 2, 10], [1, 3, 5], [2, 2, 2], [3, 3, 3])
    # plt.savefig('plots/test.png')

def plot_contributions_percentile(data, params, group_name):
    percentile = np.linspace(0, 100, 10000)
    primary_well_arsenic = np.percentile(data['arsenic_ugl'], percentile)
    contrib_primary_well = params['fp'][0]*primary_well_arsenic
    contrib_primary_well = contrib_primary_well.astype(float)
    contrib_other_well = np.repeat(params['fo'][0]*params['avgAs'][0], contrib_primary_well.shape[0])
    contrib_other_well = contrib_other_well.astype(float)
    contrib_food = np.repeat(params['Mf'][0]/params['Q'][0], contrib_primary_well.shape[0])
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_ylabel(r'Contribution to Urinary Arsenic ($\mu g/L$)', fontsize=18)
    ax.set_xlabel(r'Primary Household Well Arsenic Percentile', fontsize=18)
    ax.stackplot(percentile, contrib_primary_well, contrib_other_well, contrib_food)

    ax.set_xlim([0, 100])
    ax.set_ylim([0, 600])
    # ax.xaxis.set_ticks([0, 100, 200, 300, 400])
    # ax.yaxis.set_ticks([0, 100, 200, 300, 400])

    ax2 = ax.twiny()
    ax2_tick_locations = [0, 20, 40, 60, 80, 100]
    ax2.set_xlim(ax.get_xlim())
    ax2.set_xticks(ax2_tick_locations)
    ax2.set_xticklabels(np.percentile(data['arsenic_ugl'], ax2_tick_locations))
    ax2.set_xlabel(r'Contribution to Urinary Arsenic ($\mu g/L$)', fontsize=18)
    plt.savefig('plots/' + group_name + '_contrib_plot_percentile.png')
