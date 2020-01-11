SELECT people.subject_id, people.urine_as, 
       wells.well_id, wells.arsenic_ugl, wells.other_as_20m,
	   wells.other_as_hyp_beyond_20
FROM people, wells
WHERE people.well_id = wells.well_id