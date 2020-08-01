import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
import scipy.stats as stats
import numpy as np

def make_plots(distributed_results, distributed_params, household_results, household_params,
               data_subset, group_name, numbins, household_well_as):
    """Make plots from model results."""
    # scatter plots of individual data points
    scatter_plot_simple_regress(distributed_results, data_subset, group_name, xmax=900, ymax=1600)
    scatter_plot_multiple_regress(household_results, data_subset, group_name, household_well_as, xmax=900, ymax=1600)
    # scatter plots of binned data_subset
    binned_data = get_binned_data(data_subset, numbins, ['arsenic_ugl', household_well_as, 'urine_as', 'urine_as_pred_distributed',
                    'urine_as_pred_household'])
    plot_binned_distributed(distributed_results, binned_data, group_name, 'arsenic_ugl', 'urine_as_pred_distributed',
                500, 500, 'Primary Household Well Arsenic')
    plot_binned_household(household_results, binned_data, group_name, 'arsenic_ugl', 'urine_as_pred_household',
                500, 500, 'Primary Household Well Arsenic')
    # area plot of contributions (for distributed model only)
    plot_contributions(data_subset, distributed_params, group_name)
    plot_contributions_percentile(data_subset, distributed_params, group_name)

def format_scatter_plot(ax):
    """Do formatting common to scatter plots from all models."""
    ax.tick_params(axis='both', labelsize=16)
    ax.set_ylabel(r'Urinary Arsenic ($\mu g/L$)', fontsize=18)
    return ax

def scatter_plot_simple_regress(results, data, group_name, xmax, ymax):
    """Make scatter plot from distributed wells model results"""
    fig, ax = plt.subplots(figsize=(8, 6))
    ax = format_scatter_plot(ax)
    ax.set_xlabel(r'Primary Household Well Arsenic ($\mu g/L$)', fontsize=18)
    ax.scatter(data.arsenic_ugl, data.urine_as, marker='o', s=15, c='k', alpha=.3, edgecolors='none')
    #ax.scatter(data.arsenic_ugl, data['urine_as_pred_distributed'], marker='o', s=5, c='r', edgecolors='none')
    # switch this out for the above line of code to make a line rather than scatter for the fit
    ax.plot(np.linspace(0, 1000, 100), np.linspace(0, 1000, 100)*results.params[1] + results.params[0], 'r', linewidth=3)
    ax.set_xlim([0, xmax])
    ax.xaxis.set_ticks([0, 100, 200, 300, 400, 500, 600, 700, 800, 900])
    ax.set_ylim([0, ymax])
    ax.yaxis.set_ticks([0, 200, 400, 600, 800, 1000, 1200, 1400, 1600])
    outside_y_axis_bounds = data[data.urine_as > ymax]
    outside_x_axis_bounds = data[data.arsenic_ugl > xmax]
    # print(outside_plot_bounds.arsenic_ugl)
    # print(outside_plot_bounds.urine_as)
    print(f'there are {outside_y_axis_bounds.shape[0]} data points outside the y-axis bounds')
    print(f'there are {outside_x_axis_bounds.shape[0]} data points outside the x-axis bounds')
    # print(results.pvalues)
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
    # print('saving figure as plots/' + group_name + '_distributed_model.png')
    plt.savefig('plots/' + group_name + '_distributed_model.png', dpi=600)

def scatter_plot_multiple_regress(results, data, group_name, household_well_as, xmax, ymax):
    """Make scatter plots from household well model results"""
    # urinary As vs primary well As
    fig, ax = plt.subplots(figsize=(8, 6))
    ax = format_scatter_plot(ax)
    ax.set_xlabel(r'Primary Household Well Arsenic ($\mu g/L$)', fontsize=18)
    ax.scatter(data.arsenic_ugl, data.urine_as, marker='o', s=15, c='k', alpha=.3, edgecolors='none')
    ax.scatter(data.arsenic_ugl, data['urine_as_pred_household'], marker='o', s=15, c='r', edgecolors='none')
    ax.set_xlim([0, xmax])
    ax.xaxis.set_ticks([0, 100, 200, 300, 400, 500, 600, 700, 800, 900])
    ax.set_ylim([0, ymax])
    ax.yaxis.set_ticks([0, 200, 400, 600, 800, 1000, 1200, 1400, 1600])
    ax.add_artist(AnchoredText(
            fr'$R^2 = {results.rsquared:.2f}$' +
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
    If data does not divide evenly into bins, final bin may have slightly more or fewer data points."""
    data = data.reset_index(drop=True)
    data = data.sort_values(by=['urine_as'])
    data = data.reset_index(drop=True)
    data = data.sort_values(by=['arsenic_ugl'])
    data = data.reset_index(drop=True)
    binned_data = pd.DataFrame()
    n_tot = data.shape[0]
    bin_size = round(n_tot/nbins, 0)
    # get mean and sem for each bin
    for i in range(0, nbins):
        # index of first and last item in bin
        first_index = i*bin_size
        last_index = (i+1)*bin_size-1
        # final bin may have different amount of data
        if i == nbins - 1:
            last_index = n_tot
        binned_data = binned_data.append(get_mean_sem_dict(data, first_index, last_index, columns), ignore_index=True)
        # print("i is " + str(i))
        # print("binned data length is " + str(binned_data.shape[0]))
    return binned_data

def plot_binned_distributed(results, binned_data, group_name, xvar, yvar, xmax, ymax, xlabel):
    """Plot binned data for distributed well model."""
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_ylabel(r'Urinary Arsenic ($\mu g/L$)', fontsize=18)
    ax.set_xlabel(xlabel + r' ($\mu g/L$)', fontsize=18)
    # zorder=1 is needed to ensure the fit line is in front of the markers, as discussed in https://github.com/matplotlib/matplotlib/issues/409
    ax.errorbar(binned_data[xvar + '_mean'], binned_data.urine_as_mean, 
                yerr=binned_data.urine_as_sem, xerr=binned_data[xvar + '_sem'],
                fmt='o', markersize=10, mfc='k', mec='none', ecolor='k', capsize=2, zorder=1)
    # ax.errorbar(data[xvar + '_mean'], data[yvar+'_mean'],
    #             yerr=data[yvar+'_sem'], xerr=data[xvar+'_sem'],
    #             fmt='o', markersize=5, mfc='r', mec='none', ecolor='r', capsize=2)
    ax.plot(np.linspace(0, 1000, 100), np.linspace(0, 1000, 100)*results.params[1] + results.params[0], 'r', linewidth=3)
    #xmax=300
    #ymax=300
    ax.set_xlim([0, xmax])
    ax.set_ylim([0, ymax])
    ax.xaxis.set_ticks([0, 100, 200, 300, 400, 500])
    ax.yaxis.set_ticks([0, 100, 200, 300, 400, 500])
    ax.tick_params(axis='both', labelsize=16)
    plt.savefig('plots/' + group_name + '_' + xvar + '_' + yvar + '_binned.png', dpi=600)

def plot_binned_household(results, binned_data, group_name, xvar, yvar, xmax, ymax, xlabel):
    """Plot binned data for household well model."""
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_ylabel(r'Urinary Arsenic ($\mu g/L$)', fontsize=18)
    ax.set_xlabel(xlabel + r' ($\mu g/L$)', fontsize=18)
    ax.errorbar(binned_data[xvar + '_mean'], binned_data.urine_as_mean, 
                yerr=binned_data.urine_as_sem, xerr=binned_data[xvar + '_sem'],
                fmt='o', markersize=10, mfc='k', mec='none', ecolor='k', capsize=2)
    ax.errorbar(binned_data[xvar + '_mean'], binned_data[yvar+'_mean'],
                yerr=binned_data[yvar+'_sem'], xerr=binned_data[xvar+'_sem'],
                fmt='-o', markersize=10, mfc='r', mec='none', ecolor='r', capsize=2, c='r', linewidth=1)
    ax.set_xlim([0, xmax])
    ax.set_ylim([0, ymax])
    ax.xaxis.set_ticks([0, 100, 200, 300, 400, 500])
    ax.yaxis.set_ticks([0, 100, 200, 300, 400, 500])
    ax.tick_params(axis='both', labelsize=16)
    plt.savefig('plots/' + group_name + '_' + xvar + '_' + yvar + '_binned.png', dpi=600)

def plot_contributions(data, params, group_name):
    # varies with an individual's primary well arsenic concentration
    contrib_primary_well = params['fp'].value*data['arsenic_ugl']
    contrib_primary_well = contrib_primary_well.to_numpy().astype(float)
    # both of these are constant across individuals, since we don't have a way to estimate them more granularly
    contrib_other_well = np.repeat(params['fo'].value*params['avgAs'].value, contrib_primary_well.shape[0])
    contrib_other_well = contrib_other_well.astype(float)
    contrib_food = np.repeat(params['Mf'].value/params['Q'].value, contrib_primary_well.shape[0])
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
    contrib_primary_well = params['frac_primary_well'].value*primary_well_arsenic*params['Q'].value
    contrib_primary_well = contrib_primary_well.astype(float)

    contrib_other_well = np.repeat(params['frac_other_well'].value*params['avgAs'].value*params['Q'].value, contrib_primary_well.shape[0])
    contrib_other_well = contrib_other_well.astype(float)
    contrib_food = np.repeat(params['Mf'].value, contrib_primary_well.shape[0])

    contrib_data = pd.DataFrame(data=[percentile, contrib_primary_well, contrib_other_well, 
                                contrib_food], index=['percentile', 'contrib_primary_well',
                                'contrib_other_well', 'contrib_food']).transpose()
    # find percentile where contrib_primary_well is closest in size to the sum of the other contributions
    contrib_data['contrib_diff'] = contrib_data.contrib_primary_well - contrib_data.contrib_other_well - contrib_data.contrib_food
    min_diff = abs(contrib_data.contrib_diff).min()
    min_diff_percentile = contrib_data[(abs(contrib_data.contrib_diff) - min_diff) < .0001].percentile.iloc[0]
    print(min_diff_percentile)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_ylabel(r'Contribution to Arsenic Consumption ($\mu g/d$)', fontsize=16)
    ax.set_xlabel(r'Primary Household Well Arsenic Percentile', fontsize=16)

    plt.axvline(x=min_diff_percentile, linewidth=3, color='k', linestyle='dashed')
    ax.stackplot(percentile, contrib_primary_well, contrib_other_well, contrib_food)
    ax.set_xlim([0, 100])
    ax.set_ylim([0, 1200])
    # ax.xaxis.set_ticks([0, 100, 200, 300, 400])
    # ax.yaxis.set_ticks([0, 100, 200, 300, 400])

    ax2 = ax.twiny()
    ax2_tick_locations = [0, 20, 40, 60, 80, 100]
    ax2.set_xlim(ax.get_xlim())
    ax2.set_xticks(ax2_tick_locations)
    ax2.set_xticklabels(np.percentile(data['arsenic_ugl'], ax2_tick_locations))
    ax2.set_xlabel(r'Primary Well Arsenic ($\mu g/L$)', fontsize=16)
    plt.savefig('plots/' + group_name + '_contrib_plot_percentile.png', dpi=600)
