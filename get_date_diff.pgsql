select avg((SELECT MAX(interview_date)FROM PEOPLE)::date - interview_date::date)
from people
where knew_well_as = true

select avg((SELECT MAX(interview_date)FROM PEOPLE)::date - interview_date::date)
from people
where knew_well_as = false