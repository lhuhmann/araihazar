#%% package imports
import pandas as pd
import os
import statsmodels.api as sm


from statsmodels.sandbox.regression.predstd import wls_prediction_std

def run_regressions(data, group_name, household_well_as):
    """ Takes data and returns the regression parameters (R2, R2adj, slope(s), intercept)"""
    simple_data, simple_results = simple_regress(data, group_name)
    both_data, two_slope_results = two_slope_regress(data, group_name, household_well_as)
    return simple_results, two_slope_results, both_data

#%% base case
def simple_regress(data, group_name):
    """Run simple linear regression on input data. Return input data with added column for 
    regression predicted values and return regression results."""
    # need to add a column of ones to the x-data to get a constant term in the model
    x = sm.add_constant(data.arsenic_ugl)

    model = sm.OLS(data.urine_as, x)
    results = model.fit()
    # print(results.summary())

    urine_as_pred = results.params[1]*data.arsenic_ugl + results.params[0]
    data['urine_as_pred_simple'] = urine_as_pred
    return data, results

#%% add wells in family compound
def two_slope_regress(data, group_name, household_well_as):
    """Run multiple linear regression on input data. Return input data with added column for 
    regression predicted values and return regression results."""
    # need to add a column of ones to the x-data to get a constant term in the model
    x = sm.add_constant(pd.concat([data.arsenic_ugl, data[household_well_as]], axis=1))

    model = sm.OLS(data.urine_as, x)
    results = model.fit()
    # print(results.summary())

    urine_as_pred = results.params[1]*data.arsenic_ugl + \
                    results.params[2]*data[household_well_as] + \
                    results.params[0]
    data['urine_as_pred_multiple'] = urine_as_pred
    return data, results