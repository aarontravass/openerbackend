CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS public.users{
  id uuid NOT NULL DEFAULT public.uuid_generate_v4(),
  first_name VARCHAR(50),
  last_name VARCHAR(50),
  phone_number VARCHAR(50),
  created_at TIMESTAMPZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT users_id_pkey PRIMARY KEY(id)
};

CREATE TABLE IF NOT EXISTS public.user_relation{
  id SERIAL,
  user_id uuid NOT NULL,
  manager_user_id uuid NOT NULL ,
  created_at TIMESTAMPZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT users_relation_id_pkey PRIMARY KEY(id),
  CONSTRAINT users_relation_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
CONSTRAINT users_relation_manager_user_id_fkey FOREIGN KEY (manager_user_id)
        REFERENCES public.users (id)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
};

CREATE TABLE IF NOT EXISTS public.test_plan{
  id uuid NOT NULL DEFAULT public.uuid_generate_v4(),
  user_id uuid NOT NULL,
  approved_on TIMESTAMPZ NULL,
  created_at TIMESTAMPZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT test_plan_id_pkey PRIMARY KEY(id),
  CONSTRAINT test_plan_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
};

CREATE TYPE public.risk_statua_enum AS ENUM
    ('low', 'moderate', 'high');


CREATE TABLE IF NOT EXISTS public.test_plan_phases{
  id uuid NOT NULL DEFAULT public.uuid_generate_v4(),
  test_plan_id uuid NOT NULL,
  approved_on TIMESTAMPZ,
  manager_user_id uuid NOT NULL,
  created_at TIMESTAMPZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT test_plan_phase_id_pkey PRIMARY KEY(id),
  CONSTRAINT test_plan_phases_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
  CONSTRAINT test_plan_phases_manager_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
};
