DROP TABLE IF EXISTS well_distances;

CREATE TABLE well_distances(
  well1_id integer REFERENCES wells(well_id),
  well2_id integer REFERENCES wells(well_id),
  distance_m float,
  CONSTRAINT well1_well2 PRIMARY KEY (well1_id, well2_id)
);

INSERT INTO well_distances
SELECT
    w1.well_id AS well1, 
    w2.well_id AS well2,
    ST_DISTANCESPHEROID(w1.geom, 
						w2.geom,
						'SPHEROID["WGS 84",6378137,298.257223563]') 
						AS distance
FROM wells w1
     JOIN wells w2
     ON w1.well_id < w2.well_id;
     