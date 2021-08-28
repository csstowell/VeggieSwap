--
-- PostgreSQL database dump
--

-- Dumped from database version 13.3 (Ubuntu 13.3-1.pgdg20.04+1)
-- Dumped by pg_dump version 13.3 (Ubuntu 13.3-1.pgdg20.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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
-- Name: exchange_produce; Type: TABLE; Schema: public; Owner: hackbright
--

CREATE TABLE public.exchange_produce (
    id integer NOT NULL,
    userproduce_id integer,
    consumer_id integer,
    amount integer NOT NULL,
    comment character varying(150),
    date date,
    state character varying(100)
);


ALTER TABLE public.exchange_produce OWNER TO hackbright;

--
-- Name: exchange_produce_exchange_id_seq; Type: SEQUENCE; Schema: public; Owner: hackbright
--

CREATE SEQUENCE public.exchange_produce_exchange_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.exchange_produce_exchange_id_seq OWNER TO hackbright;

--
-- Name: exchange_produce_exchange_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hackbright
--

ALTER SEQUENCE public.exchange_produce_exchange_id_seq OWNED BY public.exchange_produce.id;


--
-- Name: produce; Type: TABLE; Schema: public; Owner: hackbright
--

CREATE TABLE public.produce (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    handpick character varying(200),
    store character varying(200),
    variety character varying(200),
    nutrient text,
    img_url text
);


ALTER TABLE public.produce OWNER TO hackbright;

--
-- Name: produce_id_seq; Type: SEQUENCE; Schema: public; Owner: hackbright
--

CREATE SEQUENCE public.produce_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.produce_id_seq OWNER TO hackbright;

--
-- Name: produce_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hackbright
--

ALTER SEQUENCE public.produce_id_seq OWNED BY public.produce.id;


--
-- Name: user_produce; Type: TABLE; Schema: public; Owner: hackbright
--

CREATE TABLE public.user_produce (
    id integer NOT NULL,
    user_id integer,
    produce_id integer,
    quantity integer NOT NULL,
    condition text NOT NULL
);


ALTER TABLE public.user_produce OWNER TO hackbright;

--
-- Name: user_produce_id_seq; Type: SEQUENCE; Schema: public; Owner: hackbright
--

CREATE SEQUENCE public.user_produce_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_produce_id_seq OWNER TO hackbright;

--
-- Name: user_produce_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hackbright
--

ALTER SEQUENCE public.user_produce_id_seq OWNED BY public.user_produce.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: hackbright
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(30) NOT NULL,
    email character varying(30) NOT NULL,
    password character varying(30) NOT NULL,
    zipcode integer NOT NULL,
    phone character varying(20),
    address character varying,
    city character varying
);


ALTER TABLE public.users OWNER TO hackbright;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: hackbright
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO hackbright;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hackbright
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: exchange_produce id; Type: DEFAULT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.exchange_produce ALTER COLUMN id SET DEFAULT nextval('public.exchange_produce_exchange_id_seq'::regclass);


--
-- Name: produce id; Type: DEFAULT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.produce ALTER COLUMN id SET DEFAULT nextval('public.produce_id_seq'::regclass);


--
-- Name: user_produce id; Type: DEFAULT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.user_produce ALTER COLUMN id SET DEFAULT nextval('public.user_produce_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: exchange_produce; Type: TABLE DATA; Schema: public; Owner: hackbright
--

COPY public.exchange_produce (id, userproduce_id, consumer_id, amount, comment, date, state) FROM stdin;
1	2	1	5	Delicious veggies	2021-08-25	Active
\.


--
-- Data for Name: produce; Type: TABLE DATA; Schema: public; Owner: hackbright
--

COPY public.produce (id, name, handpick, store, variety, nutrient, img_url) FROM stdin;
1	Asparagus	Asparagus is available fresh, frozen and canned for good nutrition and convenience. If selecting fresh, choose odorless asparagus stalks with dry, tight tips. Avoid limp or wilted stalks.	Refrigerate asparagus for up to four days by wrapping ends of stalks in wet paper towel and placing in plastic bag.	Purple Asparagus, White Asparagus	Fat free, Saturated fat free, Cholesterol free, Sodium free, Low in calories, Good source of vitamin C	https://freepngimg.com/thumb/eggplant/7-2-eggplant-png-hd-thumb.png
2	Eggplant	Choose eggplants that are heavy for their size and without cracks or discolorations.	Store eggplants in the refrigerator crisper drawer. Use within 5-7 days.	Chinese Eggplant	Low calorie, Fat free, Saturated fat free, Cholesterol free, Sodium free, Good source of copper	https://freepngimg.com/thumb/categories/1016.png
3	Kale	Kale is available fresh and frozen for good nutrition and convenience. If selecting fresh, choose dark colored kale bunches. Avoid brown or yellow leaves.	Store kale in a plastic bag in the coldest part of the fridge for 3-5 days.	N/A	Low fat, Saturated fat free, Cholesterol free, Low sodium, High in vitamin A, High in vitamin C, Good source of calcium, Good source of potassium	https://p.kindpng.com/picc/s/137-1371619_transparent-kale-leaf-hd-png-download.png
4	Beets	Choose beets with firm, smooth skins and non-wilted leaves if still attached. Smaller ones are more tender.	Remove leaves, leaving about an inch of the stems. Use leaves as greens- raw or cooked. Store roots in a plastic bag in refrigerator for up to 3 weeks. Wash before cooking.	NA	Fat free, saturated fat free, cholesterol free, low sodium, excellent source of folate.	https://spng.pngfind.com/pngs/s/213-2133811_purple-radish-common-beet-hd-png.png
\.


--
-- Data for Name: user_produce; Type: TABLE DATA; Schema: public; Owner: hackbright
--

COPY public.user_produce (id, user_id, produce_id, quantity, condition) FROM stdin;
2	2	2	3	Average
49	3	4	1	Good
50	3	2	1	Good
51	3	3	1	Good
52	3	4	1	Good
53	3	2	1	Good
54	3	2	1	Good
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: hackbright
--

COPY public.users (id, username, email, password, zipcode, phone, address, city) FROM stdin;
1	Liz_biz	lizzy@aol.com	apples66	94114	2817894563	\N	\N
2	wayne_j	wayne_johnson@gmail.com	concepts	67941	7139328567	\N	\N
3	Katie	kate_cat@aim.com	pineapple	94114	\N	\N	\N
4	mel	melverine@yahoo.com	pie	82289	\N	\N	\N
\.


--
-- Name: exchange_produce_exchange_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hackbright
--

SELECT pg_catalog.setval('public.exchange_produce_exchange_id_seq', 1, true);


--
-- Name: produce_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hackbright
--

SELECT pg_catalog.setval('public.produce_id_seq', 4, true);


--
-- Name: user_produce_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hackbright
--

SELECT pg_catalog.setval('public.user_produce_id_seq', 54, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hackbright
--

SELECT pg_catalog.setval('public.users_id_seq', 4, true);


--
-- Name: exchange_produce exchange_produce_pkey; Type: CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.exchange_produce
    ADD CONSTRAINT exchange_produce_pkey PRIMARY KEY (id);


--
-- Name: produce produce_pkey; Type: CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.produce
    ADD CONSTRAINT produce_pkey PRIMARY KEY (id);


--
-- Name: user_produce user_produce_pkey; Type: CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.user_produce
    ADD CONSTRAINT user_produce_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: exchange_produce exchange_produce_buyer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.exchange_produce
    ADD CONSTRAINT exchange_produce_buyer_id_fkey FOREIGN KEY (consumer_id) REFERENCES public.users(id);


--
-- Name: exchange_produce exchange_produce_seller_produce_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.exchange_produce
    ADD CONSTRAINT exchange_produce_seller_produce_id_fkey FOREIGN KEY (userproduce_id) REFERENCES public.user_produce(id);


--
-- Name: user_produce user_produce_produce_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.user_produce
    ADD CONSTRAINT user_produce_produce_id_fkey FOREIGN KEY (produce_id) REFERENCES public.produce(id);


--
-- Name: user_produce user_produce_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hackbright
--

ALTER TABLE ONLY public.user_produce
    ADD CONSTRAINT user_produce_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

