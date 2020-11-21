# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: nomarker
#       format_version: '1.0'
#       jupytext_version: 1.4.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# [Q1] first we initiate a SparkSession with the spark-master

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("pyspark-notebook").\
        master("spark://spark-master:7077").\
        config("spark.executor.memory", "1024m").\
        getOrCreate()

spark

# [Q2a] load CSV into spark dataframe
# and [Q2b] check schema
wrong_schema = spark.read.csv(path='../data/covid19.csv',header=True)
# by default the type of each column is apparently assumed to be String.
print(wrong_schema.printSchema())

# if you ask explicitly, spark will try to infer the schema automatically
infer_schema = spark.read.csv(path='../data/covid19.csv',header=True,inferSchema=True)
infer_schema.printSchema()
# in this case it gets the integers right, but just treats the date as a string

# or you can specify the schema explicitly

from pyspark.sql.types import (StructField, 
                               StringType, 
                               IntegerType,
                               DateType,
                               StructType)

data_schema = [StructField('continent',StringType(),True),
              StructField('location',StringType(),True),
              StructField('date',DateType(),True),
              StructField('total_cases',IntegerType(),True),
              StructField('new_cases',IntegerType(),True),
              StructField('total_deaths',IntegerType(),True),
              StructField('new_deaths',IntegerType(),True)]

correct_struc = StructType(fields=data_schema)

dataframe = spark.read.csv(path='../data/covid19.csv', header=True, schema=correct_struc)

# and we can confirm that this time the types are correct
print(dataframe.printSchema())

# if we wanted to convert to the older-style RDD we easily could
rdd = dataframe.rdd
print(f'Created `rdd` {type(rdd)} from `dataframe` {type(dataframe)}.')
# ... and vice versa
new_dataframe = rdd.toDF()
print(f'Created `new_dataframe` {type(new_dataframe)} from `rdd` {type(rdd)}.')

# the simplest way to drop null values from a spark 2.0 dataframe 
# ...is like this
drop_na = dataframe.dropna()

# [Q2c] but we can use the `.filter()` method if we like
filtered_df = dataframe.filter(
        ' and '.join([f'{x} is not null' for x in dataframe.columns])
        )

print(f'Before filtering we had {dataframe.count()} rows...')
print(f'Using `.dropna()` leaves us {drop_na.count()} rows.')
print(f'Using `.filter()` leaves us {filtered_df.count()} rows.')
if drop_na.count() == filtered_df.count():
    print('Good, those numbers are the same!')
else:
    print('Not good -- those numbers should be the same...')

# [Q3] use aggregate and groupBy functions to see highest `total_deaths` in each country
hi_total_deaths = filtered_df.groupBy('location').agg({'total_deaths':'max'})

hi_total_deaths.show()

# the assignment suggests that the number of total_deaths for Sweden should be 986
# however it is actually 5918
hi_total_deaths.filter(hi_total_deaths.location=='Sweden').show()

# however, we would get the result 986 if we hadn't explicitly made sure to load the CSV with the correct schema
wrong_schema.groupBy('location').agg({'total_deaths':'max'}).filter(wrong_schema.location=='Sweden').show()

# [Q4] use max and min functions to see which country 
# has highest and lowest `total_cases`
# NB: 'total_cases' are given for every date, 
# so for country with lowest can't simply find min(total_cases)
# as we'll get an earlier date with a lower figure
# rather than the country with the lowest final total_cases
# -- however, this is obviously not an issue for the maximum figure
import pyspark.sql.functions as F

filtered_df.select(F.max('total_cases')).show()
filtered_df.groupBy('location').max('total_cases').select(F.min('max(total_cases)')).show()

# to see a list of the countries with the highest and lowest total_cases count...
total_cases = filtered_df.groupBy('location').max('total_cases')
print('Countries with Highest Total Number of Cases')
total_cases.orderBy('max(total_cases)',ascending=False).show()
print('Countries with Lowest Total Number of Cases')
total_cases.orderBy('max(total_cases)',ascending=True).show()
