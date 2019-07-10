--
-- PostgreSQL database dump
--


-- Il faut qu'on utilse ce dossier pour créer la base de données
-- voici les instructions:
-- En utilisant le "command line":
--  psql -U postgres -f GeoData\programmes\dbschema.sql
--  il faut qu'on change le "cd (current directory)" trouver le dossier psql.exe
--  Pour moi (John), c'est comme ceci:
--  c:\Program Files\PostgreSQL\11\bin> psql -U postgres -f d:\UoA\Grenoble\INRIA\data\GeoData\programmes\dbschema.sql
--  Puis, il est necessaire qu'on mette le mot de passe de postgres,
--  C'est le même mot de passe qu'on utilise pour installer postgreSQL


-- Dumped from database version 11.4
-- Dumped by pg_dump version 11.4

-- Started on 2019-07-09 15:57:30

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
-- IL FAUT QU'ON CHANGE LE NOM DE BASE DE DONNÉES ICI
DROP DATABASE IF EXISTS test;
--
-- TOC entry 4311 (class 1262 OID 28176)
-- Name: test; Type: DATABASE; Schema: -; Owner: postgres
--
-- IL FAUT QU'ON CHANGE LE NOM DE BASE DE DONNÉES ICI
CREATE DATABASE test WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'English_Canada.utf8' LC_CTYPE = 'English_Canada.utf8';

-- IL FAUT QU'ON CHANGE LE NOM DE BASE DE DONNÉES ICI
ALTER DATABASE test OWNER TO postgres;
-- IL FAUT QU'ON CHANGE LE NOM DE BASE DE DONNÉES ICI
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

--
-- TOC entry 2 (class 3079 OID 28247)
-- Name: postgis; Type: EXTENSION; Schema: -; Owner:
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- TOC entry 4312 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry, geography, and raster spatial types and functions';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 198 (class 1259 OID 28185)
-- Name: activites; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.activites (
    uid smallint NOT NULL,
    randonnee boolean,
    alpinisme boolean,
    velo boolean,
    itineraires_dacces boolean,
    itineraires_associes boolean,
    ski_surf boolean,
    escalade boolean,
    parapente boolean,
    paralpinisme boolean,
    raquette boolean,
    peche boolean,
    cascade_de_glace boolean
);


ALTER TABLE public.activites OWNER TO postgres;

--
-- TOC entry 199 (class 1259 OID 28193)
-- Name: geographie; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.geographie (
    uid smallint NOT NULL,
    type text,
    "position" point,
    altitude real,
    massif text,
    secteur text,
    chaine text,
    region text,
    departement text,
    commune text
);


ALTER TABLE public.geographie OWNER TO postgres;

--
-- TOC entry 202 (class 1259 OID 28228)
-- Name: gestion; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.gestion (
    uid smallint NOT NULL,
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
    paiement_par_cb boolean,
    paiement_par_cheque boolean,
    paiement_par_especes boolean,
    paiement_par_cheques_vacances boolean
);


ALTER TABLE public.gestion OWNER TO postgres;

--
-- TOC entry 197 (class 1259 OID 28177)
-- Name: identite; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.identite (
    uid smallint NOT NULL,
    nom text NOT NULL
);


ALTER TABLE public.identite OWNER TO postgres;

--
-- TOC entry 200 (class 1259 OID 28204)
-- Name: media; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.media (
    uid smallint NOT NULL,
    website text,
    webite2 text,
    facebook text,
    carte_interactive text
);


ALTER TABLE public.media OWNER TO postgres;

--
-- TOC entry 201 (class 1259 OID 28215)
-- Name: photos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.photos (
    uid smallint NOT NULL,
    picid text NOT NULL,
    ext text,
    photo bytea
);


ALTER TABLE public.photos OWNER TO postgres;

--
-- TOC entry 203 (class 1259 OID 28239)
-- Name: structure; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.structure (
    uid smallint NOT NULL,
    date_de_construction smallint,
    nb_de_places smallint,
    couettes boolean,
    couvertures boolean,
    location_de_draps boolean,
    lavabos boolean,
    douches boolean,
    eau_courante boolean,
    vaisselle boolean,
    equipement_cuisson boolean,
    chauffage boolean,
    wifi boolean,
    salle_de_reunion boolean,
    restauration boolean,
    prises_electriques boolean,
    salle_hors_sac_independante boolean,
    wc_interieurs boolean
);


ALTER TABLE public.structure OWNER TO postgres;

--
-- TOC entry 4167 (class 2606 OID 28184)
-- Name: identite identite_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.identite
    ADD CONSTRAINT identite_pkey PRIMARY KEY (uid);


--
-- TOC entry 4169 (class 2606 OID 28222)
-- Name: photos photos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.photos
    ADD CONSTRAINT photos_pkey PRIMARY KEY (uid, picid);


--
-- TOC entry 4172 (class 2606 OID 28188)
-- Name: activites activites_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.activites
    ADD CONSTRAINT activites_uid_fkey FOREIGN KEY (uid) REFERENCES public.identite(uid);


--
-- TOC entry 4173 (class 2606 OID 28199)
-- Name: geographie geographie_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.geographie
    ADD CONSTRAINT geographie_uid_fkey FOREIGN KEY (uid) REFERENCES public.identite(uid);


--
-- TOC entry 4176 (class 2606 OID 28234)
-- Name: gestion gestion_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gestion
    ADD CONSTRAINT gestion_uid_fkey FOREIGN KEY (uid) REFERENCES public.identite(uid);


--
-- TOC entry 4174 (class 2606 OID 28210)
-- Name: media media_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.media
    ADD CONSTRAINT media_uid_fkey FOREIGN KEY (uid) REFERENCES public.identite(uid);


--
-- TOC entry 4175 (class 2606 OID 28223)
-- Name: photos photos_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.photos
    ADD CONSTRAINT photos_uid_fkey FOREIGN KEY (uid) REFERENCES public.identite(uid);


--
-- TOC entry 4177 (class 2606 OID 28242)
-- Name: structure structure_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.structure
    ADD CONSTRAINT structure_uid_fkey FOREIGN KEY (uid) REFERENCES public.identite(uid);


-- Completed on 2019-07-09 15:57:32

--
-- PostgreSQL database dump complete
--
