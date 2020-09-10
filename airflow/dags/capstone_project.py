from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageToRedshiftOperator, LoadTableOperator,
                                 DataQualityOperator)
from helpers import SqlQueries
default_args = {
    'owner': 'Halah',
    'start_date': datetime(2019, 1, 12),
    'retries':0,
    'catchup':False,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('s3_to_redshift_dag',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval='0 * * * *'
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

stage_immigration_to_redshift = StageToRedshiftOperator(
    task_id='Stage_immigration',
    dag=dag,
    table= "public.immigration_data",
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_bucket="mybucket-akiau",
    s3_key="immigration3.json",
    json="auto"
)

stage_demographics_to_redshift = StageToRedshiftOperator(
    task_id='Stage_demographics',
    dag=dag,
    table= "public.us_demographic_staging",
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_bucket="mybucket-akiau2",
    s3_key="us-cities-demographics.json", 
    json="auto"
)


load_immigration_table = LoadTableOperator( 
    task_id='Load_simmigration__table',
    dag=dag,
    redshift_conn_id="redshift",
    table="public.immigration",
    truncate_table=True,
    query=SqlQueries.immigration_table_insert
)

load_demographics_table = LoadTableOperator( 
    task_id='Load_demographics__table',
    dag=dag,
    redshift_conn_id="redshift",
    table="public.us_cities_demographics",
    truncate_table=True,
    query=SqlQueries.us_cities_demographics_table_insert
)

load_immigration_traviler_table = LoadTableOperator( 
    task_id='Load_immigration_traviler__table',
    dag=dag,
    redshift_conn_id="redshift",
    table="public.immigration_traviler",
    truncate_table=True,
    query=SqlQueries.immigration_traviler_table_insert
)

load_immigration_visa_table = LoadTableOperator( 
    task_id='Load_immigration_visa__table',
    dag=dag,
    redshift_conn_id="redshift",
    table="public.immigration_visa",
    truncate_table=True,
    query=SqlQueries.immigration_visa_table_insert
)

load_immigration_loc_table = LoadTableOperator( 
    task_id='Load_immigration_loc__table',
    dag=dag,
    redshift_conn_id="redshift",
    table="public.immigration_loc",
    truncate_table=True,
    query=SqlQueries.immigration_loc_table_insert
)


run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag,
    redshift_conn_id="redshift",
    data_quality_check=[{'check_sql': "SELECT COUNT(*) FROM immigration WHERE cicid is null", 'expected_result': 0},
                        {'check_sql': "SELECT COUNT(*) FROM us_cities_demographics WHERE table_id is null", 'expected_result': 0}]
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)



start_operator >> [stage_immigration_to_redshift, stage_demographics_to_redshift] >> \
load_songplays_table>>[ load_immigration_table,
                       load_demographics_table,
                       load_immigration_traviler_table,
                       load_immigration_visa_table,
                       load_immigration_loc_table] \
>> run_quality_checks >> end_operator