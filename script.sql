CREATE TABLE IF NOT EXISTS public.users
(
    hash_id int NOT NULL,
    user_id bigint NOT NULL,
    username character varying(40) COLLATE pg_catalog."default",
    sens_level real DEFAULT 0.50,
    data_folder character varying COLLATE pg_catalog."default" NOT NULL,
    result_folder character varying COLLATE pg_catalog."default" NOT NULL,
    show_labels boolean DEFAULT true,
    num_of_requests bigint DEFAULT 0,
    CONSTRAINT hash_pkey PRIMARY KEY (hash_id),
    CONSTRAINT users_id_unique UNIQUE (user_id),
    CONSTRAINT users_username_key UNIQUE (username)
)