# Project overview
This project evaluates the sources of arsenic exposure for villagers in rural Bangladesh who consume arsenic-contaminated well water.  A mass balance approach paired with linear regressions is used to estimate the average fraction of a Bangladesh villager’s drinking water that comes from the individual's primary well, other wells within the individual's household compound, and other wells throughout the study area.

# Required packages
Install from Pipfile.

# Data sources
| Source table on shared Dropbox                                                                  | Columns in source table used                                                 | Database table | Columns in SQL database                                                                 |
|-------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------|----------------|-----------------------------------------------------------------------------------------|
| WellWaterUrinaryArsenic\DataFromLex\6615_privatewells.xls | Well ID, Union, Village, Owner, As% (ug/l), Latitude, Longitude, Depth, Year | wells | well_id, union_name, village, owner_name, arsenic_ugl, latitude, longitude, depth, year |
| WellWaterUrinaryArsenic\DataFromLex\Age.xlsx | Subject, Age | people| subject_id, age|
| WellWaterUrinaryArsenic\DataFromLex\AllGender.xlsx| SubjectID, Sex | people| subject_id, sex |
| WellWaterUrinaryArsenic\DataFromLex\AllUrinaryAs_BrokenOutByYear.xlsx  (first tab only) | SubjectID, UrineAs, UrineCreat, UrAsgmCr |  people | subject_id, urine_as, urine_creatinine, urine_as_gmcr |
| WellWaterUrinaryArsenic\DataFromLex\UrineAndWaterDataOverTime (2).xls                           | subject ID, Index well                                                       | people         | subject_id, well_id                                                                     |
| WellWaterUrinaryArsenic\DataFromLex\ Covariate Dataset for Orig Cohort and FUs_Lex 10_2015a.xls | SubjectID, DateInt                                                           | people         | subject_id, interview_date                                                              |
# Data wrangling
* 
# Data analysis
## Code structure
* The functions in 'run_all.py' set up the input parameters, load the data, and run the analysis.
* The functions in 'regressions.py' run linear regressions on the input data for two different mass-balance models of water and arsenic consumption and excretion.
* The functions in 'solve_mass_balance.py' use the input parameters and the parameters from the linear regressions to solve for the estimated fractions of water consumed from different sources and the uncertainties on these fractions, saving the results to csv files.
* The functions in 'plots.py' make scatter plots of the original data compared with the model predictions.

## Running the code
The code can be run with 'python3 run_all.py'.

