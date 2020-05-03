# Project overview
This project evaluates the sources of arsenic exposure for villagers in rural Bangladesh who consume arsenic-contaminated well water.  A mass balance approach paired with linear regressions is used to estimate the average fraction of a Bangladesh villager’s drinking water that comes from the individual's primary well, other wells within the individual's household compound, and other wells throughout the study area.

# Required packages
Install from Pipfile.

# Data sources
## HEALS data
| Source table on shared Dropbox                                                                  | Columns in source table used                                                 | Database table | Columns in SQL database                                                                 |
|-------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------|----------------|-----------------------------------------------------------------------------------------|
| WellWaterUrinaryArsenic/DataFromLex/6615_privatewells.xls | Well ID, Union, Village, Owner, As% (ug/l), Latitude, Longitude, Depth, Year | wells | well_id, union_name, village, owner_name, arsenic_ugl, latitude, longitude, depth, year |
| WellWaterUrinaryArsenic/DataFromLex/Age.xlsx | Subject, Age | people| subject_id, age|
| WellWaterUrinaryArsenic/DataFromLex/AllGender.xlsx| SubjectID, Sex | people| subject_id, sex |
| WellWaterUrinaryArsenic/DataFromLex/AllUrinaryAs_BrokenOutByYear.xlsx  (first tab only) | SubjectID, UrineAs, UrineCreat, UrAsgmCr |  people | subject_id, urine_as, urine_creatinine, urine_as_gmcr |
| WellWaterUrinaryArsenic/DataFromLex/UrineAndWaterDataOverTime (2).xls                           | subject ID, Index well                                                       | people         | subject_id, well_id                                                                     |
| WellWaterUrinaryArsenic/DataFromLex/ Covariate Dataset for Orig Cohort and FUs_Lex 10_2015a.xls | SubjectID, DateInt                                                           | people         | subject_id, interview_date                                                              |
## Mass balance parameters
| Variable | Description                                                    | Estimated Value | Reference              |
|----------|----------------------------------------------------------------|-----------------|------------------------|
|          | Fraction of water consumed via food                            | 0.2 ± 0.1       | Popkin et al. 2011     |
|          | Fraction of water produced from cellular respiration           | 0.12 ± 0.06     | Gomella and Haist 2007 |
|          | mass fraction of arsenic loss via defecation                   | 0.06 ± 0.03     | Pomroy et al. 1980     |
|          | Mass fraction of arsenic lost to deep compartments in the body | 0               |                        |
|          | Mass of arsenic consumed via food                              | 64 ± 4 mg/d     | El-masri et al. 2018   |
|          |                                                                | 96 ± 6 mg/d     | local estimate         |
|          | Volume of water consumed                                       | 3 ± 1 L/d       | El-masri et al. 2018   |
|          | Average As of all wells in the study area                      | 95.2 ± 1.4 µg/L | local estimate         |

# Data wrangling
This code only needs to be run when the underlying data for the data analysis are changed.
* The araihazar-data repo should be saved in the same directory as the araihazar repo.
* Save the well data in the desired form for the SQL database in the araihazar-data repo at 'to_ingest/wells.csv'.
* Save the individual sources of the people data (age.csv, baseline_urine_as.csv, interview_dates.csv, sex.csv, subject_well_mapping.csv) in the araihazar-data repo in the 'to_clean' directory.
* Run ingest/clean_people_data.py to clean and combine the data for the 'people' table in the SQL database.
** This saves the people data in the araihazar-data repo at 'to_ingest/people.csv'.
* Ingest well data to SQL database by running 'ingest/ingest_wells.pgsql' on the database, updating the path to point to the correct data location.
* Ingest people data to SQL database by running 'ingest/ingest_people.pgsql' on the database, updating the path to point to the correct data location.
* Create a database table with distances between pairs of wells by running 'ingest/get_well_dist.pgsql' on the database.
* Calculate arsenic from selected combinations of neighboring wells using selected queries from 'ingest/get_other_well_arsenic.pgsql'.
* Extract from the database the data for the analysis stage by running 'get_data_from_db.pgsql' on the database. Save data to the araihazar-data repo in the 'to_analyze' directory.

# Data analysis
## Regression Based on Mass Balance
This code runs linear regressions (based on the mass balance equations) on the observed data from Araihazar, Bangladesh. It then uses the parameters derived from the linear regressions along with other parameters from the scientific literature to solve the mass balance equations for f<sub>p</sub>, the average fraction of water an individual consumes from their primary well, and f<sub>u</sub>, the average fraction of water an individual loses via urine, along with their uncertainties.
* The functions in 'run_all.py' set up the input parameters, load the data, and run the analysis.
* The functions in 'regressions.py' run linear regressions on the input data for two different mass-balance models of water and arsenic consumption and excretion.
* The functions in 'solve_mass_balance.py' use the input parameters and the parameters from the linear regressions to solve for the estimated fractions of water consumed from different sources and the uncertainties on these fractions, saving the results to csv files.
* uncertain_val.py provides a class, UncertainVal, used for dealing with values with uncertainties. 
* The functions in 'plots.py' make scatter plots of the original data compared with the model predictions.
* The functions in 'compare_subsets.py' compare how urinary arsenic varies as a function of well arsenic for two different subsets of the population.
### More details on subset comparison
Some study participants were informed of the arsenic concentrations in their primary drinking water wells before their urinary arsenic was tested. We hypothesize that learning their primary well arsenic concentrations may have caused them to alter their behavior. Specifically, we hypothesize that participants with the highest- and lowest-arsenic primary wells who had been informed of their primary well arsenic concentrations will have lower urinary arsenic concentrations than participants who had not been informed. This code tests that hypothesis. 
### Running the code
Before running the code, parameters for the mass balance can be updated in The code can be run with 'python3 run_all.py'.
## Exploring the effects of different mass balance parameters
Alongside the observed relationship between primary well arsenic and urinary arsenic, we plot some relationships predicted by the distributed wells model, changing one parameter at a time in the mass balance equation.
### Running the code
The code can be run with 'python3 explore_parameter_effects.py'.
## Comparison with Argos et al. (2010)
Uses the estimated fraction of water an individual consumes from their primary well and from other wells to estimate the average amount of arsenic in *all* water consumed by an individual. The output table maps each of the primary well arsenic categories from Argos et al. (first column) to the estimated mean arsenic in all water consumed for an individual with the mean primary well arsenic for that category (second column). 
### Running the code
The code can be run with 'python3 argos_comparison.py'.
## Comparison with Ahsan et al. (2006)
Uses the estimated fraction of water an individual consumes from their primary well and from other wells to estimate the average amount of arsenic in *all* water consumed by an individual. Compares the min, max, mean, and median arsenic concentrations in primary well water versus all well water for individuals in four primary well arsenic categories. These four categories are based on the categories in Ahsan et al. I was asked to calculate these values, but I don't believe this is a useful comparison, since Ahsan et al. already incorporate self-reports of water consumption from both primary wells versus other wells into their arsenic exposure estimates.
### Running the code
The code can be run with 'python3 ahsan_comparison.py'.
