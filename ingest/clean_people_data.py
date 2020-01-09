#%% package imports
import pandas as pd
import os

#%% file imports
# bring in tables
age = pd.read_csv(os.path.abspath("ingest/data_cleaning/age.csv"))
urine_as = pd.read_csv(os.path.abspath("ingest/data_cleaning/baseline_urine_as.csv"))
sex = pd.read_csv(os.path.abspath("ingest/data_cleaning/sex.csv"))
well = pd.read_csv(os.path.abspath("ingest/data_cleaning/subject_well_mapping.csv"))
all_wells = pd.read_csv(os.path.abspath("ingest/data/wells.csv"))

#%% 

# keep only people from original cohort
well = well[well['cohort'] == 'OrigCohort']

# how many people from orig cohort have wells without a known well As? 
# It looks like about 10 people and 5 wells. 
# Those people should be filtered out since we can't use them in our analysis
# So do an inner join of the person-well mapping ('well' table) with the well data ('all_wells' table)
well = pd.merge(left=well, right=all_wells, left_on='Index well', right_on='Well ID', how='inner')

# inner join urine_as and well tables 
# (inner join because we can only do a useful analysis on people with known primary well and known urine As)
people = pd.merge(left=urine_as, right=well, left_on='SubjectID', right_on='subject ID', how='inner')
people = people.drop('subject ID', axis=1)
# left join that table with age table
people = pd.merge(left=people, right=age, left_on='SubjectID', right_on='Subject', how='left')
people = people.drop(['Subject'], axis=1)
# left join with sex table
people = pd.merge(left=people, right=sex, on='SubjectID', how='left')

# replace sex markers with something more meaningful
people['Sex'] = people['Sex'].map({1: 'male', 2: 'female'})
#make well id int type
people = people.astype({'Index well': int})
#reorder columns
people = people[['SubjectID', 'Sex', 'Age','Index well', 'UrineAs', 'UrineCreat', 'UrAsgmCr']]
print(people.head(5))

people.to_csv(os.path.abspath("ingest/data/people.csv"), index=False)