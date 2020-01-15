SELECT people.subject_id, 
       people.urine_as,
       people.did_not_know, 
       wells.well_id, 
       wells.arsenic_ugl, 
       wells.other_as_50m,
	   wells.other_as_hyp_beyond_50
FROM people, wells
WHERE people.well_id = wells.well_id