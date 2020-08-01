import pandas as pd
from scipy import stats

women_data = pd.read_csv('../araihazar-data/to_analyze/women_didnotknow_matlab.csv')
men_data = pd.read_csv('../araihazar-data/to_analyze/men_didnotknow_matlab.csv')

# compare variances
print(women_data['As_ugL'].head())
print(men_data['As_ugL'].head())
print(women_data['As_ugL'].tail())
print(men_data['As_ugL'].tail())
well_as_W, well_as_p = stats.bartlett(women_data['As_ugL'], men_data['As_ugL'])
print(well_as_p)
ur_as_W, ur_as_p = stats.bartlett(women_data['UrineAs'], men_data['UrineAs'])
print(ur_as_p)

# save data to table
# index = ['arsenic_ugL', 'urine_as', 'W', 'p']
# columns = ['primary well As variance', 'urinary As variance', 'n']
# out_data = pd.DataFrame(index=index, columns=columns)
# out_data.loc[subset_pair[0]] = [well_as_variances[subset_pair[0]], urine_as_variances[subset_pair[0]], count[subset_pair[0]]]
# out_data.loc[subset_pair[1]] = [well_as_variances[subset_pair[1]], urine_as_variances[subset_pair[1]], count[subset_pair[1]]]
# out_data.loc['W'] = [well_as_W, ur_as_W, np.nan]
# out_data.loc['p'] = [well_as_p, ur_as_p, np.nan]
# out_data.to_csv(f'../araihazar-data/analysis_output/variances_{subset_pair[0]}_{subset_pair[1]}.csv')