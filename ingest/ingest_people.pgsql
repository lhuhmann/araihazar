DROP TABLE IF EXISTS people;

CREATE TABLE people
(
  subject_id integer PRIMARY KEY,
  sex character varying(6),
  age integer,
  well_id integer REFERENCES wells(well_id),
  urine_as float,
  urine_creatinine float,
  urine_as_gmcr float,
  interview_date date,
  knew_well_as boolean
);

COPY people ( subject_id, sex, age, well_id, urine_as, urine_creatinine, urine_as_gmcr, interview_date, knew_well_as )
    FROM 'C:/Users/Britt/GitHub/araihazar-data/to_ingest/people.csv'
    WITH 
          DELIMITER AS ','
          CSV HEADER ;