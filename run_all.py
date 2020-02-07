#%% imports
import os
import pandas as pd

from regressions import run_regressions
from plots import make_plots
from solve_mass_balance import calculate_parameters, apply_formatting

#%%
def make_subset(data, group_name):
    """Given a group name and the full data set, return the subset of the data that corresponds
    to the group name."""
    if group_name == 'did_not_know':
        # keep only the rows where people did not know their well As
        # when their urine As was measured
        return data[data['knew_well_as'] == False]
    elif group_name == 'women':
        return data[data['sex'] == 'female']
    elif group_name == 'women_did_not_know':
        return data[(data['knew_well_as'] == False) & (data['sex'] == 'female')]
    elif group_name == 'men':
        return data[data['sex'] == 'male']
    elif group_name == 'men_did_not_know':
        return data[(data['knew_well_as'] == False) & (data['sex'] == 'male')]
    elif group_name == 'all':
        return data
    else:
        assert False, 'Group does not exist'
    return data

def run_one(parameters_with_uncertainties, household_well_as, group_name, data, numbins):
    """Run the two mass balance models for one set of input parameters. Outputs the data with predicted
    values appended, the results of the two regressions, and the parameters for the two models."""
    # get the correct subset of the data
    data = make_subset(data, group_name)
    # run regressions
    distributed_results, household_results, data = run_regressions(data, group_name, household_well_as)
    # calculate parameter values
    distributed_params, household_params = calculate_parameters(distributed_results, household_results, parameters_with_uncertainties, group_name)
    # plot results
    make_plots(distributed_results, distributed_params, household_results, household_params, data, group_name, numbins, household_well_as)
    return data, distributed_results, distributed_params, household_results, household_params

def run_many():
    """Run the two mass balance models for many sets input parameters. Saves one csv for each model,
    with as many columns of values as there are sets of parameters."""
    # parameters that may change across runs:
    # parameters that go into the mass balance equation and their uncertainties
    parameters_with_uncertainties = [{'ff':(0.2, 0.1), 'fc':(0.12, 0.06), 'md':(0.06, 0.03),
                                     'mb':(0, 0), 'Mf':(96, 6), 'Q':(3, 1), 'avgAs':(95.2, 1.4)},
                                     {'ff':(0.2, 0.1), 'fc':(0.12, 0.06), 'md':(0.06, 0.03),
                                     'mb':(0, 0), 'Mf':(96, 6), 'Q':(3, 1), 'avgAs':(95.2, 1.4)}]
    # which column to use for household well arsenic
    household_well_as = ['other_as_50m', 'other_as_50m']
    # which subset of the data to look at
    group_name = ['all', 'did_not_know']

    # parameters that I don't expect to change across runs:
    # full dataset
    data = pd.read_csv(os.path.abspath("data_for_regressions.csv"))
    # number of bins for plotting results
    numbins = 15

    # do run_one on each set of inputs
    all_distributed_params = []
    all_household_params = []
    all_data = []
    for params, household, group in zip(parameters_with_uncertainties, household_well_as,
                                        group_name):
        data_with_pred_vals, distributed_results, distributed_params, household_results, \
            household_params = run_one(params, household, group, data, numbins)
        all_distributed_params.append(apply_formatting(distributed_params))
        all_household_params.append(apply_formatting(household_params))
        all_data.append(data_with_pred_vals)
    # save all distributed params to one csv as adjacent columns
    all_distributed_params = pd.DataFrame(all_distributed_params)
    all_distributed_params = all_distributed_params.T
    all_distributed_params.to_csv('output_data/run_many_distributed_params.csv')
    # save all household params to another csv as adjacent columns
    all_household_params = pd.DataFrame(all_household_params)
    all_household_params = all_household_params.T
    all_household_params.to_csv('output_data/run_many_household_params.csv')
  
if __name__ == "__main__":
    run_many()
