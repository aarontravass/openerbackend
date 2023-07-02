-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
DROP TABLE IF EXISTS PUBLIC.users CASCADE;
CREATE TABLE IF NOT EXISTS public.users(
  id SERIAL,
  first_name VARCHAR(50),
  last_name VARCHAR(50),
  created_at timestamptz  NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamptz  NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT users_id_pkey PRIMARY KEY(id)
);
DROP TABLE IF EXISTS PUBLIC.user_relation CASCADE;
CREATE TABLE IF NOT EXISTS public.user_relation(
  id SERIAL,
  user_id INT NOT NULL,
  manager_user_id INT NOT NULL,
  created_at timestamptz  NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamptz  NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT users_relation_id_pkey PRIMARY KEY(id),
  CONSTRAINT users_relation_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
CONSTRAINT users_relation_manager_user_id_fkey FOREIGN KEY (manager_user_id)
        REFERENCES public.users (id)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

CREATE TYPE risk_statua_enum as ENUM (
'low', 'moderate', 'high'
);
DROP TABLE IF EXISTS PUBLIC.test_plan CASCADE;
CREATE TABLE IF NOT EXISTS public.test_plan(
  id SERIAL,
  user_id INT NOT NULL,
  plan_name VARCHAR(50),
  approved_on timestamptz  NULL,
  created_at timestamptz  NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamptz  NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT test_plan_id_pkey PRIMARY KEY(id),
  CONSTRAINT test_plan_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);



DROP TABLE IF EXISTS PUBLIC.test_plan_phases CASCADE;
CREATE TABLE IF NOT EXISTS public.test_plan_phases(
  id SERIAL,
  test_plan_id INT NOT NULL,
  approved_on timestamptz,
  manager_user_id INT NULL,
  risk risk_statua_enum NOT NULL,
  created_at timestamptz  NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamptz  NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT test_plan_phase_id_pkey PRIMARY KEY(id),
  CONSTRAINT test_plan_phases_test_plan_id_fkey FOREIGN KEY (test_plan_id)
        REFERENCES public.test_plan (id)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
  CONSTRAINT test_plan_phases_manager_user_id_fkey FOREIGN KEY (manager_user_id)
        REFERENCES public.users (id)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);


INSERT INTO PUBLIC.users VALUES(DEFAULT, 'a','a', DEFAULT, DEFAULT);
INSERT INTO PUBLIC.users VALUES(DEFAULT, 'b','b', DEFAULT, DEFAULT);
INSERT INTO PUBLIC.users VALUES(DEFAULT, 'x','x', DEFAULT, DEFAULT);
INSERT INTO PUBLIC.users VALUES(DEFAULT, 'y','y', DEFAULT, DEFAULT);
INSERT INTO PUBLIC.users VALUES(DEFAULT, 'z','z', DEFAULT, DEFAULT);

-- a has manager x and y
INSERT INTO PUBLIC.user_relation VALUES(DEFAULT, 1, 3, DEFAULT, DEFAULT);
INSERT INTO PUBLIC.user_relation VALUES(DEFAULT, 1, 4, DEFAULT, DEFAULT);


-- b has manager x and z
INSERT INTO PUBLIC.user_relation VALUES(DEFAULT, 2, 3, DEFAULT, DEFAULT);
INSERT INTO PUBLIC.user_relation VALUES(DEFAULT, 2, 5, DEFAULT, DEFAULT);


-- x has manager z
INSERT INTO PUBLIC.user_relation VALUES(DEFAULT, 3, 5, DEFAULT, DEFAULT);

INSERT INTO public.test_plan VALUES (DEFAULT, 1,'plan 1', CURRENT_TIMESTAMP, DEFAULT, DEFAULT);
INSERT INTO public.test_plan_phases VALUES(DEFAULT, 1, CURRENT_TIMESTAMP, 1, 'low', DEFAULT, DEFAULT);
INSERT INTO public.test_plan_phases VALUES(DEFAULT, 1, CURRENT_TIMESTAMP, 3, 'moderate', DEFAULT, DEFAULT);
INSERT INTO public.test_plan_phases VALUES(DEFAULT, 1, CURRENT_TIMESTAMP, 3, 'moderate', DEFAULT, DEFAULT);



INSERT INTO public.test_plan VALUES (DEFAULT, 2,'plan 2', NULL, DEFAULT, DEFAULT);
INSERT INTO public.test_plan_phases VALUES(DEFAULT, 2, NULL, NULL, 'moderate', DEFAULT, DEFAULT);


INSERT INTO public.test_plan VALUES (DEFAULT, 2,'plan 3', NULL, DEFAULT, DEFAULT);
INSERT INTO public.test_plan_phases VALUES(DEFAULT, 3, CURRENT_TIMESTAMP, 3, 'moderate', DEFAULT, DEFAULT);
INSERT INTO public.test_plan_phases VALUES(DEFAULT, 3, NULL, NULL, 'high', DEFAULT, DEFAULT);
