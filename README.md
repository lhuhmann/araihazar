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
This code only needs to be run when the underlying data for the data analysis are changed.
* Save the well data in the desired form for the SQL database at 'ingest\data\wells.csv'.
* Save the individual sources of the people data (age.csv, baseline_urine_as.csv, interview_dates.csv, sex.csv, subject_well_mapping.csv) at 'ingest\data_cleaning'.
* Run \ingest\clean_people_data.py to clean and combine the data for the 'people' table in the SQL database.
** This saves the people data at 'ingest\data\people.csv'.
* Ingest well data to SQL database by running '\ingest\ingest_well.pgsql'.
* Ingest people data to SQL database by running '\ingest\ingest_people.pgsql'.
* Create a database table with distances between pairs of wells by running '\ingest\get_well_dist.pgsql'.
* Calculate arsenic from selected combinations of neighboring wells using selected queries from '\ingest\get_other_well_arsenic.pgsql'.
* Extract from the database the data for the data analysis stage by running '\ingest\get_data_from_db.pgsql'.

# Data analysis
## Code structure
* The functions in 'run_all.py' set up the input parameters, load the data, and run the analysis.
* The functions in 'regressions.py' run linear regressions on the input data for two different mass-balance models of water and arsenic consumption and excretion.
* The functions in 'solve_mass_balance.py' use the input parameters and the parameters from the linear regressions to solve for the estimated fractions of water consumed from different sources and the uncertainties on these fractions, saving the results to csv files.
* The functions in 'plots.py' make scatter plots of the original data compared with the model predictions.

## Running the code
The code can be run with 'python3 run_all.py'.

