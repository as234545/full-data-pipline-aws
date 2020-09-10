# full data pipline AWS






## project Scope 
The porpose if the project is to understand the US immigration and ansower some question we have like:
1-	What majore world event did most effect immigration travile in the last 5 years?
2-	What top 5 nationality travila to US?
And to ansowers these quation we need to manage multible data 
-	I94 Immigration Data Here 
-	U.S. City Demographic Data


## Used Tchnologes 
- python script, to first upload the original data to s3 bucket just, then to get to know and view that data first then apply data cleaning by removeing unwanted columns, dublicat or ones that has too many null values and upload the cleaced data to another s3 buckt to use later in processing.  

- aws dataLake was used because it stores relational and non-relational data. The structure of the data or schema is not defined when data is captured. This means you can store all of your data without careful design.

- apache airflow, was used to schedule and monitor workflows to orchestrate the pipline from transeefing the data from s3 storage to redshift data werehouse. it's easy to use and learn 

## Table Schema 
There is one Fact table called 'immigration' and the other tables are dimation table.  

## explanation of some files in the repository    
`aws.cfg` configuration and settings file to place aws access key id and aws secret access key.      
`data-dictionary.xlsx` has all the description on the table columns


### If the data was increased by 100x.
Amazon Redshift had the ability with elastic resize and concurrency scaling. Elastic resize meaning to quickly increase or decrease the number of compute nodes, doubling or halving the original cluster’s node count, or even change the node type.

### If the pipelines were run on a daily basis by 7am.
add hook that send notification on faliure, to quilcy debug the issue, or add emila Sla


### If the database needed to be accessed by 100+ people.
assigne roles to morintore change  

