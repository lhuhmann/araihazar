#%% package imports
import os
import pandas as pd

from regressions import run_regressions
from plots import make_plots
from solve_mass_balance import calculate_parameters

#%% 
def run_all(data, group_name, household_well_as, numbins, parameters_with_uncertainties):
    data = make_subset(data, group_name)
    simple_results, two_slope_results, both_data = run_regressions(data, group_name, household_well_as)
    calculate_parameters(simple_results, two_slope_results, parameters_with_uncertainties, group_name)
    make_plots(simple_results, two_slope_results, both_data, group_name, numbins, household_well_as)

def make_subset(data, group_name):
    """Given a group name and the full data set, return the subset of the data that correspond to the group name."""
    if group_name == 'did_not_know':
        # keep only the rows where people did not know their well As when their urine As was measured
        data = data[data['knew_well_as'] == False]
    elif group_name == 'women':
        data = data[data['sex'] == 'female']
    elif group_name == 'women_did_not_know':
        data = data[data['knew_well_as'] == False]
        data = data[data['sex'] == 'female']
    elif group_name == 'men':
        data = data[data['sex'] == 'male']
    elif group_name == 'men_did_not_know':
        data = data[data['knew_well_as'] == False]
        data = data[data['sex'] == 'male']
    elif group_name == 'all':
        data = data
    else:
        assert(False)
    return data

if __name__ == "__main__":
    # parameters that go into the mass balance equation and their uncertainties
    parameters_with_uncertainties = {'ff':(0.2, 0.1), 'fc':(0.12,0.06), 'md':(0.06,0.03),
    'mb':(0,0), 'Mf':(96,6), 'Q':(3,1), 'avgAs':(95.2,1.4)}

    # pick which column to use for neighbor well arsenic
    household_well_as = "other_as_20m"
    # number of bins
    numbins = 15
    # data
    data = pd.read_csv(os.path.abspath("data_for_regressions.csv"))
    # group
    group_name = 'women_did_not_know'
    run_all(data, group_name, household_well_as, numbins, parameters_with_uncertainties)
