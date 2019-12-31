DROP TABLE IF EXISTS wells;

CREATE TABLE wells
(
  well_id integer PRIMARY KEY,
  union_name character varying(50),
  village character varying(50),
  owner_name character varying(50),
  arsenic_ugL float,
  latitude float,
  longitude float,
  depth float,
  year integer
);

COPY wells ( well_id, union_name, village, owner_name, arsenic_ugl, latitude, longitude, depth, year )
    FROM 'C:/Users/Britt/GitHub/araihazar/ingest/data/wells.csv'
    WITH 
          DELIMITER AS ','
          CSV HEADER ;

--37202 is SRID, 2 is for dimensional data
SELECT AddGeometryColumn('public', 'wells', 'geom', 37202, 'POINT', 2);

UPDATE wells SET geom = ST_SetSRID(ST_MakePoint(latitude, longitude),37202);

-- Create a spatial index for faster querying
CREATE INDEX wells_geom ON wells USING GIST ( geom );