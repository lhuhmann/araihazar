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
  knew_well_as boolean
);

COPY people ( subject_id, sex, age, well_id, urine_as, urine_creatinine, urine_as_gmcr, knew_well_as )
    FROM 'C:/Users/Britt/GitHub/araihazar/ingest/data/people.csv'
    WITH 
          DELIMITER AS ','
          CSV HEADER ;