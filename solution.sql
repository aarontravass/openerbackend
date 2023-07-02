
-- a. Write SQL to retrieve all Test Plans that a particular user has approved a Phase on. Return only data for Test Plans. Ensure there are no duplicate rows in the results.
SELECT test_plan.id, plan_name FROM test_plan INNER JOIN test_plan_phases 
ON test_plan.id = test_plan_phases.test_plan_id
WHERE test_plan_phases.manager_user_id=3
GROUP BY test_plan.id;

-- b. Write SQL to find all the Test Plans that are still pending (i.e., have an unapproved Phase).Return only data for Test Plans. Ensure there are no duplicate rows in the results.
SELECT test_plan.id, plan_name FROM test_plan INNER JOIN test_plan_phases
ON test_plan.id = test_plan_phases.test_plan_id
WHERE test_plan_phases.approved_on IS null
GROUP BY test_plan.id;

-- c. Write SQL to add an additional Phase to a particular Test Plan.

INSERT INTO public.test_plan_phases VALUES(DEFAULT, 3, NULL, NULL, 'moderate', DEFAULT, DEFAULT);