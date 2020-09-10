from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id = "",
                 data_quality_check = "",
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.data_quality_check = data_quality_check
    def execute(self, context):
        redshift_hook = PostgresHook("redshift")
        
        for check in data_quality_check:
            sql = check["check_sql"]
            exp = check["expected_result"]
            records = redshift_hook.get_records(sql)
            num_records = records[0][0]
            if num_records != exp:
                raise ValueError(f"Data quality check failed. Expected: {exp} | Got: {num_records}")
            else:
                self.log.info(f"Data quality on SQL {sql} check passed with {records[0][0]} records")