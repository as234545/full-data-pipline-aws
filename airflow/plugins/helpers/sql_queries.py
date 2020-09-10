class SqlQueries:
    immigration_table_insert = ("""
        SELECT
    cicid,
    i94yr,
    i94mon,
    i94cit,
    i94res,
    i94port,
    arrdate,
    i94mode,
    i94addr,
    depdate,
    dtadfile,
    entdepu,
    matflag,
    dtaddto,
        FROM immigration_staging

    """)

    us_cities_demographics_table_insert = ("""
        SELECT distinct     
    city,
    state,
    median_age ,
    male_population,
    female_population ,
    total_population,
    number_of_veterans,
    Foreign_born ,
    average_household_size,
    state_code,
    race 
        FROM us_demographic_staging
    """)

    immigration_table_insert = ("""
        SELECT distinct 
            cicid   NOT NULL,
    i94yr ,
    i94mon ,
    i94cit ,
    i94res ,
    i94port ,
    arrdate ,
    i94mode ,
    i94addr ,
    depdate  ,
    dtadfile ,
    entdepu ,
    matflag ,
    dtaddto ,
        FROM immigration_staging
    """)

    immigration_traviler_table_insert = ("""
        SELECT distinct     cicid   NOT NULL,
    gender ,
    biryear ,
    i94bir ,
    status ,
        FROM immigration_staging
    """)

    immigration_visa_table_insert = ("""
        SELECT distinct   
          cicid   NOT NULL,
    visapost ,
    visatype ,
    i94visa ,
        FROM immigration_staging
    """)

    immigration_loc_table_insert = ("""
        SELECT distinct
    cicid   NOT NULL,
    airline ,
    fltno ,
        FROM immigration_staging
    """)
