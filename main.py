#Python 3.7.2rc1
import configparser
from datetime import datetime, timedelta
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format
import pandas as pd
import glob
#pip install pyarrow
import pyarrow.parquet as pq
import boto3
from botocore.exceptions import NoCredentialsError
from pyspark.sql import SparkSession
import json



config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['AWS_SECRET_ACCESS_KEY']


########### use spark to read the data and partionate into multable files
spark = SparkSession.builder.\
config("spark.jars.packages","saurfang:spark-sas7bdat:2.0.0-s_2.11")\
.enableHiveSupport().getOrCreate()
df_spark =spark.read.format('com.github.saurfang.sas.spark').load('../../data/18-83510-I94-Data-2016/i94_apr16_sub.sas7bdat')
#write to parquet
df_spark.write.parquet("sas_data3")
df_spark=spark.read.parquet("sas_data3")



################ Move the original data to S3 buckeet
 

# this method take file local location and bucket name and file name to be stored in the s3 bucket
def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

# upload the orginal us-cities-demographics.csv file to s3 bucket
uploaded = upload_to_aws('/home/workspace/us-cities-demographics.csv', 'mybucket-akiau2-original' ,'us-cities-demographics.csv' )


parquetfiles = []
for file in glob.glob("/home/workspace/sas_data/*.parquet"):
    parquetfiles.append(file)

for x in range(len(parquetfiles)): 
	filenme = parquetfiles[x]
	uploaded = upload_to_aws(parquetfiles[x], 'mybucket-akiau2-original' ,filenme[filenme.rfind('/')+1:] )


################ data cleaning 

# Compine all files data in one DataFrame
filesNames = glob.glob("/home/workspace/sas_data/*.parquet")
df4 = pd.DataFrame()
for x in range(len(filesNames)): 
    print (filesNames[x])
    df2 = pd.read_parquet(filesNames[x], engine='pyarrow')
    df4 = df4.append(df2)

count_row = df4.shape[0]
count_row
dfObj = pd.DataFrame(df4, columns=['cicid'])
#print(df4.dtypes)
duplicateRowsDF = dfObj[dfObj.duplicated()]
duplicateRowsDF = duplicateRowsDF.sort_values(by=['cicid'])
duplicateRowsDF

# check for null columns 
for col in df4.columns: 
    print(col)
    print( df4[col].isnull().sum() / len(df4)*100)

# drop column with more that 40% nulls and unwanted columns 

to_drop =['entdepa', 'count', 'insnum' , 'admnum' ,'occup']
df4.drop(to_drop, inplace=True, axis=1)

# check original types
df4.dtypes


# convert to json then upload to s3 bucket 
df4 = df4.to_json(orient='records')
with open('immigration3.json', 'w') as json_file:
    json.dump(df4, json_file)

uploaded = upload_to_aws("/home/workspace/immigration3.json", 'mybucket-akiau' ,'immigration3.json' )

########## clean the demographic data

# impoer the data
df7 = pd.read_csv('/home/workspace/us-cities-demographics.csv' , delimiter=';') 

#check for dublicate data
dfObj = pd.DataFrame(df7, columns=['City','State','Race'])
duplicateRowsDF = dfObj[dfObj.duplicated()]
duplicateRowsDF = duplicateRowsDF.sort_values(by=['City'])
duplicateRowsDF

# change the column names so it's easy to work with in the sql
df7.rename(columns = {'City': 'city','State':'state','Median Age':'median_age','Male Population':'male_population','Female Population':'female_population','Total Population':'total_population', 'Number of Veterans':'number_of_veterans' ,'Average Household Size':'average_household_size','State Code':'state_code','Race':'race','Foreign-born':'Foreign_born'}, inplace = True) 

#drop unwanted column
df7.drop('Count', inplace=True, axis=1)

#convert to json then upload to s3 bucket 
df7 = df7.to_json(orient='records')
with open('us-cities-demographics.json', 'w') as json_file:
    json.dump(df7, json_file)
uploaded = upload_to_aws('/home/workspace/us-cities-demographics.json', 'mybucket-akiau2' ,'us-cities-demographics.json' )