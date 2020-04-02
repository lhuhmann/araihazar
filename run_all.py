#%% imports
import os
import pandas as pd

from uncertain_val import UncertainVal
from regressions import run_regressions
from plots import make_plots
from solve_mass_balance import calculate_parameters, apply_formatting
from compare_subsets import make_subset
from compare_subsets import compare_subsets

#%%
def run_one(parameters_with_uncertainties, household_well_as, group_name, data, numbins):
    """Run the two mass balance models for one set of input parameters. Outputs the data with predicted
    values appended, the results of the two regressions, and the parameters for the two models.
    
    >>> parameters_with_uncertainties = {'ff':(0.2, 0.1), 'fc':(0.12, 0.06), 'md':(0.06, 0.03),
                                         'mb':(0, 0.03), 'Mf':(64, 4), 'Q':(3, 1), 
                                         'avgAs':(95.2, 1.4)}
    >>> household_well_as = ['other_as_50m']
    >>> group_name = ['did_not_know']
    # TODO: add some minimal amount of relevant data
    >>> data = 
    >>> numbins = 15
    # TODO: add expected output given the data I choose
    """
    # get the correct subset of the data
    data_subset = make_subset(data, group_name)
    # run regressions
    distributed_results, household_results, data_subset = run_regressions(data_subset, group_name, household_well_as)
    # calculate parameter values
    distributed_params, household_params = calculate_parameters(distributed_results, household_results, parameters_with_uncertainties, group_name)
    # plot results
    make_plots(distributed_results, distributed_params, household_results, household_params, data_subset, group_name, numbins, household_well_as)
    # compare subsets
    compare_subsets(distributed_results, data)
    return data_subset, distributed_results, distributed_params, household_results, household_params

def run_many():
    """Run the two mass balance models for many sets input parameters. Saves one csv for each model,
    with as many columns of values as there are sets of parameters."""
    # parameters that may change across runs:
    # parameters that go into the mass balance equation and their uncertainties
    parameters_with_uncertainties = [{'ff':(0.2, 0.1), 'fc':(0.12, 0.06), 'md':(0.06, 0.03),
                                      'mb':(0, 0.03), 'Mf':(64, 4), 'Q':(3, 1), 
                                      'avgAs':(95.2, 1.4)}]
    parameters_with_uncertainties = [{k:UncertainVal(v[0], v[1]) for k, v in param_dict.items()}   
                                     for param_dict in parameters_with_uncertainties] 
    # which column to use for household well arsenic
    household_well_as = ['other_as_50m']
    # which subset of the data to look at
    group_name = ['did_not_know']

    # parameters that I don't expect to change across runs:
    # full dataset
    data = pd.read_csv('../araihazar-data/to_analyze/data_for_regressions.csv')
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
    all_distributed_params.to_csv('../araihazar-data/analysis_output/run_many_distributed_params.csv')
    # save all household params to another csv as adjacent columns
    all_household_params = pd.DataFrame(all_household_params)
    all_household_params = all_household_params.T
    all_household_params.to_csv('../araihazar-data/analysis_output/run_many_household_params.csv')
  
if __name__ == "__main__":
    import doctest
    doctest.testmod()
    run_many()


