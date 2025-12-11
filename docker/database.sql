--
-- PostgreSQL database dump
--

\restrict 6Jh7qHv2XLMomU7HGzb3iMPC0GFlF8XLy5ekqR6zMqViqRJFlQKAkSCkQ2RmchY

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.permissions (
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    "create" boolean NOT NULL,
    read boolean NOT NULL,
    update boolean NOT NULL,
    delete boolean NOT NULL,
    business_entity character varying(255) NOT NULL
);


ALTER TABLE public.permissions OWNER TO postgres;

--
-- Name: revoked_tokens; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.revoked_tokens (
    jti uuid NOT NULL
);


ALTER TABLE public.revoked_tokens OWNER TO postgres;

--
-- Name: user_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_permissions (
    user_id uuid NOT NULL,
    permission_id uuid NOT NULL
);


ALTER TABLE public.user_permissions OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    surname character varying(255) NOT NULL,
    patronymic character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    password character varying(255) NOT NULL,
    is_active boolean NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Data for Name: permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.permissions (id, name, description, "create", read, update, delete, business_entity) FROM stdin;
936ef793-ccee-430c-a541-68fc49934175	Права администратора на Пользователь	\N	t	t	t	t	Пользователь
e1b6d154-bfad-4a54-b020-5bbab8529cb9	Права администратора на Право доступа	\N	t	t	t	t	Право доступа
dc6b69b3-9ee8-4817-a01e-1d28fdc98c1a	Права администратора на Товар	\N	t	t	t	t	Товар
b39d9f32-72b5-4632-9348-55b56c5f6ed2	test	test	t	t	t	t	Пользователь
e41e9280-49e5-484a-9b7c-cb8375bec1ac	test2	test2	t	t	t	t	Право доступа
e0c9b84f-e773-4a49-8a60-60dfbf812f42	test3	test3	t	t	t	t	Товар
\.


--
-- Data for Name: revoked_tokens; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.revoked_tokens (jti) FROM stdin;
cff612c7-ae6c-4660-9590-c63205137475
c522cd39-92dd-4c45-a05f-bbc530608f3b
d665cd83-2ad3-41d6-8a93-6096e252bdbc
86a59deb-0e80-47ed-b506-b8a15b65eb97
9a5ee60a-10e8-4859-a14a-c64598ec16fa
a1a031d7-d364-4448-890b-c3876c203bc7
08dd89dd-da1b-49bc-8092-0d2d20d32e39
\.


--
-- Data for Name: user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_permissions (user_id, permission_id) FROM stdin;
f2f0ccc3-316e-4939-9378-dedc307fd0c0	e1b6d154-bfad-4a54-b020-5bbab8529cb9
f2f0ccc3-316e-4939-9378-dedc307fd0c0	936ef793-ccee-430c-a541-68fc49934175
f2f0ccc3-316e-4939-9378-dedc307fd0c0	dc6b69b3-9ee8-4817-a01e-1d28fdc98c1a
0b05f6fe-4a6b-45bb-8058-2b6947bf6c38	b39d9f32-72b5-4632-9348-55b56c5f6ed2
0b05f6fe-4a6b-45bb-8058-2b6947bf6c38	e41e9280-49e5-484a-9b7c-cb8375bec1ac
0b05f6fe-4a6b-45bb-8058-2b6947bf6c38	e0c9b84f-e773-4a49-8a60-60dfbf812f42
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, name, surname, patronymic, email, password, is_active) FROM stdin;
f2f0ccc3-316e-4939-9378-dedc307fd0c0	admin	admin	admin	admin@admin.ru	8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918	t
0b05f6fe-4a6b-45bb-8058-2b6947bf6c38	test	test	test	test@test.ru	9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08	t
\.


--
-- Name: permissions permissions_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_name_key UNIQUE (name);


--
-- Name: permissions permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_pkey PRIMARY KEY (id);


--
-- Name: revoked_tokens revoked_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.revoked_tokens
    ADD CONSTRAINT revoked_tokens_pkey PRIMARY KEY (jti);


--
-- Name: user_permissions user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_permissions
    ADD CONSTRAINT user_permissions_pkey PRIMARY KEY (user_id, permission_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: user_permissions user_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_permissions
    ADD CONSTRAINT user_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES public.permissions(id);


--
-- Name: user_permissions user_permissions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_permissions
    ADD CONSTRAINT user_permissions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

\unrestrict 6Jh7qHv2XLMomU7HGzb3iMPC0GFlF8XLy5ekqR6zMqViqRJFlQKAkSCkQ2RmchY

