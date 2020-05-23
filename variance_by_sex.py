import pandas as pd
import numpy as np
from scipy import stats

from compare_subsets import make_subset, make_histograms

# get subsets by sex
subset_pairs = [['women', 'men'], ['women_did_not_know', 'men_did_not_know'], ['women_may_have_known', 'men_may_have_known']]
data = pd.read_csv('../araihazar-data/to_analyze/data_for_regressions.csv')

for subset_pair in subset_pairs:
    data_pair = {}
    count = {}
    well_as = {}
    well_as_variances = {}
    urine_as = {}
    urine_as_variances = {}
    for subset in subset_pair:
        # get subset of data
        data_pair[subset] = make_subset(data, subset)
        count[subset] = len(data_pair[subset].index)
        # get well As variance
        well_as[subset] = data_pair[subset].arsenic_ugl
        well_as_variances[subset] = np.var(data_pair[subset].arsenic_ugl)

        # get urine As variance
        urine_as[subset] = data_pair[subset].urine_as
        urine_as_variances[subset] = np.var(data_pair[subset].urine_as)
    # compare variances
    well_as_W, well_as_p = stats.levene(well_as[subset_pair[0]], well_as[subset_pair[1]], center='median')
    ur_as_W, ur_as_p = stats.levene(urine_as[subset_pair[0]], urine_as[subset_pair[1]], center='median')
    # make histograms
    print(well_as[subset_pair[0]])
    make_histograms(data_pair[subset_pair[0]], subset_pair[0], data_pair[subset_pair[1]], subset_pair[1],  0, 5000, 'arsenic_ugl')
    make_histograms(data_pair[subset_pair[0]], subset_pair[0], data_pair[subset_pair[1]], subset_pair[1], 0, 5000, 'urine_as')
    # save data to table
    index = [subset_pair[0], subset_pair[1], 'W', 'p']
    columns = ['primary well As variance', 'urinary As variance', 'n']
    out_data = pd.DataFrame(index=index, columns=columns)
    out_data.loc[subset_pair[0]] = [well_as_variances[subset_pair[0]], urine_as_variances[subset_pair[0]], count[subset_pair[0]]]
    out_data.loc[subset_pair[1]] = [well_as_variances[subset_pair[1]], urine_as_variances[subset_pair[1]], count[subset_pair[1]]]
    out_data.loc['W'] = [well_as_W, ur_as_W, np.nan]
    out_data.loc['p'] = [well_as_p, ur_as_p, np.nan]
    out_data.to_csv(f'../araihazar-data/analysis_output/variances_{subset_pair[0]}_{subset_pair[1]}.csv')

