import os
import csv

import pandas as pd
import numpy as np
import scipy.stats as stats

from uncertain_val import UncertainVal
from solve_mass_balance import apply_formatting

# bring in data
data = pd.read_csv('../araihazar-data/to_analyze/data_for_regressions.csv')

# fraction of water from primary wells and other wells
fp = 0.4
fh = 0.20
fo = 0.07

# average As concentration of all wells in the area
mean_As_all_wells = 95.2
sem_As_all_wells = 1.4

# run for each of the four categories in Argos
categories = ['0.1-10', '10.1-50', '50.1-150', '150.1-864']
min_As = [0.1, 10.1, 50.1, 150.1]
max_As = [10, 50, 150, 864]
solutions = [['As range primary well', 'number of participants','mean As primary well', 'mean As all water consumed']]
for category, min_val, max_val in zip(categories, min_As, max_As):
    subset_data = data[(data['arsenic_ugl'] >= min_val) & (data['arsenic_ugl'] <= max_val)]
    num_subj = subset_data.shape[0]
    mean_As_primary_well = np.mean(subset_data['arsenic_ugl'])
    sem_As_primary_well = stats.sem(subset_data['arsenic_ugl'])
    mean_As_household_wells = np.mean(subset_data['other_as_20m'])
    sem_As_household_wells = stats.sem(subset_data['other_as_20m'])
    mean_As_water_consumed = (fp*mean_As_primary_well + fh*mean_As_household_wells + fo*mean_As_all_wells)/(fp+fh+fo)
    sem_As_water_consumed = (fp*sem_As_primary_well + fh*sem_As_household_wells + fo*sem_As_all_wells)/(fp+fh+fo)
    solutions.append([
        category,
        len(subset_data),
        UncertainVal(mean_As_primary_well, sem_As_primary_well),
        UncertainVal(mean_As_water_consumed, sem_As_water_consumed), 
    ])
with open(os.path.abspath(f'../araihazar-data/analysis_output/argos_table_fp={fp}_fh={fh}_fo={fo}.csv'), "w") as savefile:
    writer = csv.writer(savefile)
    for row in apply_formatting(solutions):
        writer.writerow(row)
