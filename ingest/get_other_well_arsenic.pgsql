ALTER TABLE wells
ADD COLUMN other_as_50m float,
ADD COLUMN other_as_40m float,
ADD COLUMN other_as_30m float,
--ADD COLUMN other_as_hyp_beyond_20 float,
--ADD COLUMN other_as_exp float,
--ADD COLUMN other_as_exp_dist_round float
ADD COLUMN other_as_exp_beyond_50 float,
ADD COLUMN other_as_exp_beyond_40 float,
ADD COLUMN other_as_exp_beyond_30 float;

--assume person drinks equally from all wells within 50 m
WITH other_as_table (well1_id, other_as) AS (
    SELECT well1_id, (AVG(well2_arsenic_ugl))
    FROM well_distances
    WHERE distance_m <= 50
    GROUP BY well1_id
)
UPDATE wells
SET other_as_50m = other_as_table.other_as
FROM other_as_table
WHERE wells.well_id = other_as_table.well1_id


--assume person drinks from all other wells in proportion to 1/distance to each well,
--for wells beyond 20 m
WITH other_as_table (well1_id, other_as) AS (
    SELECT well1_id, SUM(well2_arsenic_ugl*(1/distance_m))/SUM(1/distance_m)
    FROM well_distances
    WHERE distance_m > 50
    GROUP BY well1_id
)
UPDATE wells
SET other_as_hyp_beyond_50 = other_as_table.other_as
FROM other_as_table
WHERE wells.well_id = other_as_table.well1_id

--assume person drinks from all other wells in an amount that decreases exponentially with distance
WITH other_as_table (well1_id, other_as) AS (
    SELECT well1_id, SUM(well2_arsenic_ugl*exp(-distance_m))/SUM(exp(-distance_m))
    FROM well_distances
    --exclude wells greater than 1000 m away, since their contribution to the sum will be tiny
    WHERE distance_m < 500
    GROUP BY well1_id
)
UPDATE wells
SET other_as_exp = other_as_table.other_as
FROM other_as_table
WHERE wells.well_id = other_as_table.well1_id

--assume person drinks from all other wells in an amount that decreases exponentially with distance
--version where all distances below 5 m are rounded up to 5 m
WITH other_as_table (well1_id, other_as) AS (
    SELECT well1_id, 
           SUM(
               CASE WHEN distance_m < 5 THEN well2_arsenic_ugl*exp(-5)
                ELSE well2_arsenic_ugl*exp(-distance_m)
                END)/
            SUM(
                CASE WHEN distance_m < 5 THEN exp(-5)
                ELSE exp(-distance_m)
                END)
    FROM well_distances
    --exclude wells greater than 1000 m away, since their contribution to the sum will be tiny
    WHERE distance_m < 500
    GROUP BY well1_id
)
UPDATE wells
SET other_as_exp_dist_round = other_as_table.other_as
FROM other_as_table
WHERE wells.well_id = other_as_table.well1_id

--assume person drinks from all other wells in an amount that decreases exponentially with distance
--only for wells beyond 30 m from primary well
WITH other_as_table (well1_id, other_as) AS (
    SELECT well1_id, SUM(well2_arsenic_ugl*exp(-distance_m))/SUM(exp(-distance_m))
    FROM well_distances
    --exclude wells greater than 1000 m away, since their contribution to the sum will be tiny
    WHERE distance_m < 500
    AND distance_m > 30
    GROUP BY well1_id
)
UPDATE wells
SET other_as_exp_beyond_30 = other_as_table.other_as
FROM other_as_table
WHERE wells.well_id = other_as_table.well1_id