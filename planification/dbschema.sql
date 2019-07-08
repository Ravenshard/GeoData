--
-- PostgreSQL database dump
--

-- Dumped from database version 11.4
-- Dumped by pg_dump version 11.4

-- Started on 2019-07-05 10:57:46

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

DROP DATABASE IF EXISTS test;
--
-- TOC entry 2839 (class 1262 OID 16398)
-- Name: ecrains; Type: DATABASE; Schema: -; Owner: Jay
--

CREATE DATABASE test WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'English_Canada.1252' LC_CTYPE = 'English_Canada.1252';


ALTER DATABASE test OWNER TO "Jay";

\connect test

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

SET default_with_oids = false;

--
-- TOC entry 196 (class 1259 OID 21287)
-- Name: identite; Type: TABLE; Schema: public; Owner: Jay
--

DROP TABLE IF EXISTS public.identite;
CREATE TABLE public.identite (
    uid text NOT NULL,
    nom text,
    PRIMARY KEY (uid)
);


-- ALTER TABLE public.identite OWNER TO "Jay";


--
-- TOC entry 200 (class 1259 OID 22565)
-- Name: activites; Type: TABLE; Schema: public; Owner: Jay
--

DROP TABLE IF EXISTS public.activites;
CREATE TABLE public.activites (
    uid text REFERENCES identite(uid),
    randonnee text,
    alpinisme text,
    velo text,
    itineraires_dacces text,
    itineraires_associes text,
    ski_surf text,
    escalade text,
    parapente text,
    paralpinisme text,
    raquette text,
    peche text,
    cascade_de_glace text,
    FOREIGN KEY (uid) REFERENCES public.identite(uid)
);


-- ALTER TABLE public.activites OWNER TO "Jay";

--
-- TOC entry 198 (class 1259 OID 22523)
-- Name: geographie; Type: TABLE; Schema: public; Owner: Jay
--

CREATE TABLE public.geographie (
    uid text NOT NULL,
    type text,
    longitude text,
    latitude text,
    altitude text,
    massif text,
    secteur text,
    chaine text,
    region text,
    departement text,
    commune text,
    FOREIGN KEY (uid) REFERENCES public.identite (uid)
);


-- ALTER TABLE public.geographie OWNER TO "Jay";



--
-- TOC entry 199 (class 1259 OID 22559)
-- Name: media; Type: TABLE; Schema: public; Owner: Jay
--

CREATE TABLE public.media (
    uid text,
    website text,
    webite2 text,
    facebook text,
    carte_interactive text,
    FOREIGN KEY (uid) REFERENCES public.identite (uid)

);


-- ALTER TABLE public.media OWNER TO "Jay";

--
-- TOC entry 197 (class 1259 OID 21297)
-- Name: photos; Type: TABLE; Schema: public; Owner: Jay
--

CREATE TABLE public.photos (
    uid text NOT NULL,
    picid text NOT NULL,
    ext text,
    photo bytea,
    FOREIGN KEY (uid) REFERENCES public.identite (uid),
    PRIMARY KEY (uid,picid)
);


-- ALTER TABLE public.photos OWNER TO "Jay";

--
-- TOC entry 201 (class 1259 OID 22578)
-- Name: structure; Type: TABLE; Schema: public; Owner: Jay
--

CREATE TABLE public.structure (
    uid text NOT NULL,
    proprietaire text,
    gestionnaire text,
    gardien text,
    adresse text,
    telephone_1 text,
    telephone_2 text,
    mail text,
    reservation text,
    dates text,
    ouverture_et_fermeture text,
    tarifs text,
    paiement_par_cb text,
    paiement_par_cheque text,
    paiement_par_especes text,
    paiement_par_cheques_vacances text,
    FOREIGN KEY (uid) REFERENCES public.identite (uid)
);


-- ALTER TABLE public.structure OWNER TO "Jay";

--
-- TOC entry 2710 (class 2606 OID 21296)
-- Name: identite identite_pkey; Type: CONSTRAINT; Schema: public; Owner: Jay
--

-- ALTER TABLE ONLY public.identite
    -- ADD CONSTRAINT identite_pkey PRIMARY KEY (uid);


--
-- TOC entry 2712 (class 2606 OID 21304)
-- Name: photos photos_pkey; Type: CONSTRAINT; Schema: public; Owner: Jay
--

-- ALTER TABLE ONLY public.photos
    -- ADD CONSTRAINT photos_pkey PRIMARY KEY (uid, picid);


-- Completed on 2019-07-05 10:57:47

--
-- PostgreSQL database dump complete
--
