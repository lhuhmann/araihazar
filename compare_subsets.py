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
    may_know_subset = make_subset(data, 'may_have_known')

    # comparison of full data with data subset
    plot_group_comparison(distributed_results, not_know_subset, may_know_subset, 'subset_comparison_binned', xmax=500, ymax=400, tick_spacing=100)
    # inset (lower left)
    plot_group_comparison(distributed_results, not_know_subset, may_know_subset, 'subset_comparison_binned_inset', xmax=100, ymax=100, tick_spacing=25)

    # hypothesis: for the people with primary well arsenic greater than 250 ug/L, 
    # the group that may have been informed of their well arsenic has lower urinary 
    # arsenic than the group that was not informed
    compare_means(not_know_subset, may_know_subset, arsenic_ugl_lower_bound=300, arsenic_ugl_upper_bound=100000)

    # hypothesis: for the people with primary well arsenic less than 10 ug/L,
    # the group that may have been informed of their well arsenic has lower urinary 
    # arsenic than the group that was not informed
    compare_means(not_know_subset, may_know_subset, arsenic_ugl_lower_bound=100, arsenic_ugl_upper_bound=200)


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
    if group_name == 'men':
        return data[data['sex'] == 'male']
    if group_name == 'men_did_not_know':
        return data[(data['knew_well_as'] == False) & (data['sex'] == 'male')]
    if group_name == 'all':
        return data
    assert False, 'Group does not exist'
    return False

def plot_group_comparison(results, not_know_subset, may_know_subset, plotname, xmax, ymax, tick_spacing):
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

def compare_means(not_know_subset, may_know_subset, arsenic_ugl_lower_bound, arsenic_ugl_upper_bound):
    """For the given data subsets, within the given bounds, checks if the first data subset has a 
    significantly higher mean urinary arsenic than the second data subset."""
    not_know_subset = not_know_subset[(not_know_subset.arsenic_ugl > arsenic_ugl_lower_bound) & 
                                      (not_know_subset.arsenic_ugl < arsenic_ugl_upper_bound)]
    may_know_subset = may_know_subset[(may_know_subset.arsenic_ugl > arsenic_ugl_lower_bound) & 
                                      (may_know_subset.arsenic_ugl < arsenic_ugl_upper_bound)]
    test_statistic, p_value = scipy.stats.bartlett(not_know_subset.urine_as, may_know_subset.urine_as)
    if p_value < 0.05:
        equal_var = False
    else:
        equal_var = True
    # do a two-tailed t-test
    test_statistic, p_value_two_tailed = scipy.stats.ttest_ind(not_know_subset.urine_as,
                                                               may_know_subset.urine_as, equal_var=equal_var)
    # we want a one-tailed t-test, since we are specifically testing if may_know_subset has a lower
    # mean urinary arsenic, so divide p_value from two-tailed t-test by 2
    # (https://stats.idre.ucla.edu/other/mult-pkg/faq/general/faq-what-are-the-differences-between-one-tailed-and-two-tailed-tests/) 
    p_value_one_tailed = p_value_two_tailed/2
    # we expect a positive test statistic if mean of not_know_subset is greater than mean of may_know_subset
    print(equal_var, test_statistic, p_value_one_tailed)
    with open(os.path.abspath(f'output_data/well_as_{arsenic_ugl_lower_bound}_to_{arsenic_ugl_upper_bound}_urine_as_comparison.csv'), "w") as savefile:
        writer = csv.writer(savefile)
        writer.writerow(['equal variance', 'test statistic', 'one-tailed p-value'])
        writer.writerow([equal_var, test_statistic, p_value_one_tailed])