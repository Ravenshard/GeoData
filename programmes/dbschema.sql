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

CREATE DATABASE test WITH ENCODING = 'UTF8' LC_COLLATE = 'English_Canada.1252' LC_CTYPE = 'English_Canada.1252';

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

CREATE TABLE public.identite (
    uid smallint NOT NULL,
    nom text NOT NULL,
    PRIMARY KEY (uid)
);

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
    cascade_de_glace boolean,
    FOREIGN KEY (uid) REFERENCES public.identite (uid)
);

CREATE TABLE public.geographie (
    uid smallint NOT NULL,
    type text,
    position point,
    altitude real,
    massif text,
    secteur text,
    chaine text,
    region text,
    departement text,
    commune text,
    FOREIGN KEY (uid) REFERENCES public.identite (uid)
);

CREATE TABLE public.media (
    uid smallint NOT NULL,
    website text,
    webite2 text,
    facebook text,
    carte_interactive text,
    FOREIGN KEY (uid) REFERENCES public.identite (uid)
);

CREATE TABLE public.photos (
    uid smallint NOT NULL,
    picid text NOT NULL,
    ext text,
    photo bytea,
    FOREIGN KEY (uid) REFERENCES public.identite (uid),
    PRIMARY KEY (uid,picid)
);

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
    paiement_par_cheques_vacances boolean,
    FOREIGN KEY (uid) REFERENCES public.identite (uid)
);

CREATE TABLE public.structure (
    uid smallint NOT NULL,
    date_de_construction smallint,
    nb_de_places smallint,
    couettes boolean,
    couvertures boolean,
    location_de_Draps boolean,
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
    WC_interieurs boolean,
    FOREIGN KEY (uid) REFERENCES public.identite (uid)
);
