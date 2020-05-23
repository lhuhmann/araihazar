import os
import csv

import scipy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

from plots import get_binned_data

def compare_subsets(distributed_results, data):
    # get data subset
    not_know_subset = make_subset(data, 'did_not_know')
    not_know_subset.to_csv('../araihazar-data/analysis_output/not_know_subset.csv')
    may_know_subset = make_subset(data, 'may_have_known')
    may_know_subset.to_csv('../araihazar-data/analysis_output/may_know_subset.csv')

    # comparison of full data with data subset
    plot_group_comparison(distributed_results, not_know_subset, may_know_subset, 'subset_comparison_binned', xmax=500, ymax=400, tick_spacing=100)
    # inset (lower left)
    plot_group_comparison(distributed_results, not_know_subset, may_know_subset, 'subset_comparison_binned_inset', xmax=100, ymax=100, tick_spacing=25)

    # hypothesis: for the people with primary well arsenic greater than 250 ug/L, 
    # the group that may have been informed of their well arsenic has lower urinary 
    # arsenic than the group that was not informed
    compare_well_and_urine_as_means(not_know_subset, may_know_subset, arsenic_ugl_lower_bound=250, arsenic_ugl_upper_bound=100000)

    # hypothesis: for the people with primary well arsenic less than 10 ug/L,
    # the group that may have been informed of their well arsenic has lower urinary 
    # arsenic than the group that was not informed
    compare_well_and_urine_as_means(not_know_subset, may_know_subset, arsenic_ugl_lower_bound=0, arsenic_ugl_upper_bound=10)


def make_subset(data, group_name): # pylint: disable=too-many-return-statements
    """Given a group name and the full data set, return the subset of the data that corresponds
    to the group name."""
    if group_name == 'did_not_know':
        # keep only the rows where people did not know their well As
        # when their urine As was measured
        return data[data['knew_well_as'] == False]
    if group_name == 'may_have_known':
        # keep only the rows where people may have known their well As
        # when their urine As was measured
        return data[data['knew_well_as'] == True]
    if group_name == 'women':
        return data[data['sex'] == 'female']
    if group_name == 'women_did_not_know':
        return data[(data['knew_well_as'] == False) & (data['sex'] == 'female')]
    if group_name == 'women_may_have_known':
        return data[(data['knew_well_as'] == True) & (data['sex'] == 'female')]
    if group_name == 'men':
        return data[data['sex'] == 'male']
    if group_name == 'men_did_not_know':
        return data[(data['knew_well_as'] == False) & (data['sex'] == 'male')]
    if group_name == 'men_may_have_known':
        return data[(data['knew_well_as'] == True) & (data['sex'] == 'male')]
    if group_name == 'all':
        return data
    assert False, 'Group does not exist'
    return False


def plot_group_comparison(results, not_know_subset, may_know_subset, plotname, xmax, ymax, tick_spacing):
    """Binned errorbar plots of the two subsets alongisde the model fit line"""
    # bin both and plot the binned data
    binned_data_may_know = get_binned_data(may_know_subset, 15, ['arsenic_ugl', 'urine_as'])
    binned_data_not_know = get_binned_data(not_know_subset, 15, ['arsenic_ugl', 'urine_as'])

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_ylabel(r'Urinary Arsenic ($\mu g/L$)', fontsize=18)
    ax.set_xlabel(r'Primary Well Arsenic ($\mu g/L$)', fontsize=18)
    # zorder=1 is needed to ensure the fit line is in front of the markers, 
    # as discussed in https://github.com/matplotlib/matplotlib/issues/409
    ax.errorbar(binned_data_not_know['arsenic_ugl_mean'], binned_data_not_know['urine_as_mean'],
                xerr=binned_data_not_know['arsenic_ugl_sem'], yerr=binned_data_not_know['urine_as_sem'],
                fmt='ok', markersize=10, mfc='k', mec='none', ecolor='k', capsize=2, zorder=1)
    ax.errorbar(binned_data_may_know['arsenic_ugl_mean'], binned_data_may_know['urine_as_mean'],
                xerr=binned_data_may_know['arsenic_ugl_sem'], yerr=binned_data_may_know['urine_as_sem'],
                fmt='ob', markersize=10, mfc='b', mec='none', ecolor='b', capsize=2, zorder=1)
    ax.plot(np.linspace(0, 1000, 100), np.linspace(0, 1000, 100)*results.params[1] + results.params[0],
                        'r', linewidth=3)
    ax.set_xlim([0, xmax])
    ax.set_ylim([0, ymax])
    ax.xaxis.set_major_locator(MultipleLocator(tick_spacing))
    ax.yaxis.set_major_locator(MultipleLocator(tick_spacing))
    ax.tick_params(axis='both', labelsize=16)
    plt.savefig(f'plots/{plotname}.png')


def compare_well_and_urine_as_means(not_know_subset, may_know_subset, arsenic_ugl_lower_bound, arsenic_ugl_upper_bound):
    """For the given data subsets, within the given bounds, checks if the first data subset has a
    significantly higher mean well arsenic and mean urinary arsenic than the second data subset."""
    not_know_subset = not_know_subset[(not_know_subset.arsenic_ugl > arsenic_ugl_lower_bound) &
                                      (not_know_subset.arsenic_ugl < arsenic_ugl_upper_bound)]
    may_know_subset = may_know_subset[(may_know_subset.arsenic_ugl > arsenic_ugl_lower_bound) &
                                      (may_know_subset.arsenic_ugl < arsenic_ugl_upper_bound)]
    urine_comparison = compare_means(not_know_subset, may_know_subset, 'urine_as')
    make_histograms(not_know_subset, 'did_not_know', may_know_subset, 'may_have_known', 
                    arsenic_ugl_lower_bound, arsenic_ugl_upper_bound, 
                    'urine_as')
    well_comparison = compare_means(not_know_subset, may_know_subset, 'arsenic_ugl')
    make_histograms(not_know_subset, 'did_not_know', may_know_subset, 'may_have_known',
                    arsenic_ugl_lower_bound, arsenic_ugl_upper_bound, 
                    'arsenic_ugl')
    with open(os.path.abspath(f'../araihazar-data/analysis_output/well_as_{arsenic_ugl_lower_bound}_to_{arsenic_ugl_upper_bound}_well_and_urine_as_comparison.csv'), "w") as savefile:
        writer = csv.writer(savefile)
        writer.writerow(['mean compared', 'equal variance', 'test statistic', 'one-tailed p-value'])
        writer.writerow(['urine'] + urine_comparison)
        writer.writerow(['well water'] + well_comparison)


def make_histograms(subset1, subset1_name, subset2, subset2_name,
                    arsenic_ugl_lower_bound, arsenic_ugl_upper_bound, to_compare):
    """Compares histograms for the two subsets of the values in to_compare between the specified bounds."""
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_ylabel(r'Probability Density', fontsize=18)
    if to_compare == 'arsenic_ugl':
        ax.set_xlabel(r'Primary Well Arsenic ($\mu g/L$)', fontsize=18)
    else:
        ax.set_xlabel(r'Urinary Arsenic ($\mu g/L$)', fontsize=18)
    bins = 15
    density = True
    if arsenic_ugl_lower_bound == 0:
        xmax = 500
    else:
        xmax = 2500
    ax.set_xlim([0, xmax])
    # density='density' to show normalized histograms
    plt.rcParams['hatch.color'] = 'blue'
    plt.hist(subset1[to_compare], bins, alpha=0.5, color='black', density=density)
    plt.hist(subset2[to_compare], bins, facecolor='none', hatch='/', edgecolor='blue', density=density)
    ax.tick_params(axis='x', labelsize=16)
    ax.tick_params(axis='y', labelsize=10)
    plt.savefig(f'plots/{to_compare}_{subset1_name}_{subset2_name}_comparison_well_as_{arsenic_ugl_lower_bound}_to_{arsenic_ugl_upper_bound}.png', transparent=True)


def compare_means(not_know_subset, may_know_subset, to_compare):
    """Takes two subsets of study participants and a category to compare. Returns whether an equal or unequal
    variance t-test was conducted, along with the test statistic and the one-tailed p-value for the test."""
    test_statistic, p_value = scipy.stats.bartlett(not_know_subset[to_compare], may_know_subset[to_compare])
    if p_value < 0.05:
        equal_var = False
    else:
        equal_var = True
    # do a two-tailed t-test
    test_statistic, p_value_two_tailed = scipy.stats.ttest_ind(not_know_subset[to_compare],
                                                               may_know_subset[to_compare],
                                                               equal_var=equal_var)
    # we want a one-tailed t-test, since we are specifically testing if may_know_subset has a lower
    # mean urinary arsenic, so divide p_value from two-tailed t-test by 2
    # (https://stats.idre.ucla.edu/other/mult-pkg/faq/general/faq-what-are-the-differences-between-one-tailed-and-two-tailed-tests/) 
    p_value_one_tailed = p_value_two_tailed/2
    # we expect a positive test statistic if mean of not_know_subset is greater than mean of may_know_subset
    return [equal_var, test_statistic, p_value_one_tailed]
