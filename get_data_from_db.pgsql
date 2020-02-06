SELECT people.subject_id, 
       people.urine_as,
       people.knew_well_as, 
       people.sex,
       wells.well_id, 
       wells.arsenic_ugl, 
       wells.other_as_50m,
	wells.other_as_hyp_beyond_50,
       --if there were no wells within 30 m, use well arsenic from primary well
       COALESCE(wells.other_as_30m, wells.arsenic_ugL) AS other_as_30m,
       COALESCE(wells.other_as_20m, wells.arsenic_ugL) AS other_as_20m
FROM people, wells
WHERE people.well_id = wells.well_id