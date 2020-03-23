import os

import pandas as pd
import numpy as np
import scipy.stats as stats

from uncertain_val import UncertainVal
from solve_mass_balance import apply_formatting

# bring in data
data = pd.read_csv(os.path.abspath("data_for_regressions.csv"))

# fraction of water from primary wells and other wells
fp = 0.5
fo = 0.18

# average As concentration of all wells in the area
mean_As_all_wells = UncertainVal(95.2, 1.4)

# run for each of the categories in Ahsan
categories = ['0.1-8.0', '8.1-40.0', '40.1-91.0', '91.1-175.0', '175.1-864.0']
min_As = [0.1, 8.1, 40.1, 91.1, 175.1]
max_As = [8, 40, 91, 175, 864]

# add column to data for estimate of As in all water consumed (primary wells and other wells)
data['arsenic_ugl_water_consumed'] = (fp*data['arsenic_ugl'] + fo*mean_As_all_wells.value)/(fp+fo)

solutions_dict = {}
for category, min_val, max_val in zip(categories, min_As, max_As):
    subset_data = data[(data['arsenic_ugl'] >= min_val) & (data['arsenic_ugl'] <= max_val)]
    num_subj = subset_data.shape[0]
    mean_As_primary_well = UncertainVal(np.mean(subset_data['arsenic_ugl']),
                                        stats.sem(subset_data['arsenic_ugl']))
    mean_As_water_consumed = UncertainVal(np.mean(subset_data['arsenic_ugl_water_consumed']),
                                          stats.sem(subset_data['arsenic_ugl_water_consumed']))
    median_As_primary_well = np.median(subset_data['arsenic_ugl'])
    median_As_water_consumed = np.median(subset_data['arsenic_ugl_water_consumed'])
    min_As_water_consumed = min(subset_data['arsenic_ugl_water_consumed'])
    max_As_water_consumed = max(subset_data['arsenic_ugl_water_consumed'])
    solutions_dict.update({category: {'mean primary well As (ug/L)': mean_As_primary_well,
                                      'mean all water As (ug/L)': mean_As_water_consumed,
                                      'median primary well As (ug/L)': median_As_primary_well,
                                      'median all water As (ug/L)': median_As_water_consumed,
                                      'min all water As (ug/L)': min_As_water_consumed,
                                      'max all water As (ug/L)': max_As_water_consumed,
                                      'number of participants': num_subj}})

solutions_dataframe = pd.concat({k: pd.DataFrame.from_dict(v, 'index')
                                 for k, v in solutions_dict.items()}, axis=1)
solutions_dataframe.apply(apply_formatting)
solutions_dataframe.to_csv('output_data/ahsan_table.csv')
