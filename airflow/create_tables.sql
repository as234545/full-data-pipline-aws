CREATE TABLE public.immigration_staging (
	cicid varchar(256),
	i94yr varchar(256),
	i94mon varchar(256),
	i94cit varchar(256),
	i94res varchar(256),
	i94port varchar(256),
	arrdate numeric(18,0),
	i94mode varchar(256),
	i94addr varchar(256),
	depdate  varchar(256),
	i94bir varchar(256),
	i94visa varchar(256),
	dtadfile varchar(256),
	visapost varchar(256),
	status varchar(256),
	entdepu varchar(256),
	matflag varchar(256),
	biryear varchar(256),
	dtaddto varchar(256),
	gender varchar(256),
	airline varchar(256),
	fltno varchar(256),
	visatype varchar(256)

);

CREATE TABLE public.us_demographic_staging  (
	city	varchar(256),
	state	varchar(256),
	median_age	varchar(256),
	male_population	varchar(256),
	female_population	varchar(256),
	total_population varchar(256),
	number_of_veterans varchar(256),
	Foreign_born	varchar(256),
	average_household_size varchar(256),
	state_code varchar(256),
	race varchar(256)

);


CREATE TABLE public.immigration (
	cicid  varchar(256) NOT NULL,
	i94yr varchar(256),
	i94mon varchar(256),
	i94cit varchar(256),
	i94res varchar(256),
	i94port varchar(256),
	arrdate varchar(256),
	i94mode varchar(256),
	i94addr varchar(256),
	depdate  varchar(256),
	dtadfile varchar(256),
	entdepu varchar(256),
	matflag varchar(256),
	dtaddto varchar(256),
	CONSTRAINT immigration_pkey PRIMARY KEY (cicid)
);


CREATE TABLE public.immigration_traviler(
	cicid  varchar(256) NOT NULL,
	gender varchar(256),
	biryear varchar(256),
	i94bir  numeric(18,0),
	status varchar(256),
	CONSTRAINT immigration_traviler_pkey PRIMARY KEY (cicid)
);

CREATE TABLE public.immigration_visa(
	cicid  varchar(256) NOT NULL,
	visapost varchar(256),
	visatype varchar(256),
	i94visa varchar(256),
	CONSTRAINT simmigration_visa_pkey PRIMARY KEY (cicid)
);

CREATE TABLE public.immigration_loc(
	cicid  varchar(256) NOT NULL,
	airline varchar(256),
	fltno  numeric(18,0),
	CONSTRAINT immigration_loc_pkey PRIMARY KEY (cicid)
);

CREATE TABLE public.us_cities_demographics(
	table_id int NOT NULL AUTO_INCREMENT
	city varchar(256),
	State varchar(256),
	median_age numeric(18,2),
	male_population numeric(18,2),
	female_population numeric(18,2),
	total_population numeric(18,0),
	number_of_veterans numeric(18,0),
	foreign_born varchar(256),
	average_household_size numeric(18,3),
	state_code  varchar(256),
	race varchar(256),
	CONSTRAINT us_cities_demographics_pkey PRIMARY KEY (table_id)
);
