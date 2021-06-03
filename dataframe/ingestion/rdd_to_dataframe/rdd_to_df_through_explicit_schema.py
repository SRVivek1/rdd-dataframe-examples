"""
This program demonstrates the how to validate the schema when creating DataFrame objects.
"""


from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import unix_timestamp
from pyspark.sql.types import StructType, StructField, IntegerType, FloatType, StringType, LongType, DoubleType

import constants.app_constants as app_constants


if __name__ == '__main__':
    sparkSession = SparkSession \
        .builder \
        .appName('rdd-to-df-schema-validation') \
        .getOrCreate()

    sparkContext = sparkSession.sparkContext
    sparkContext.setLogLevel('ERROR')

    txn_fct_rdd = sparkContext.textFile(app_constants.txn_fct_csv_file) \
        .filter(lambda rec: rec.find('txn_id')) \
        .map(lambda rec: rec.split("|")) \
        .map(lambda rec: Row(int(rec[0]), int(rec[1]), float(rec[2]), int(rec[3]), int(rec[4]), int(rec[5]), str(rec[6])))
        # RDD[Row(int, int, float, int, int, int, str)]

    print('\n*************** RDD sample data read from file')
    for row in txn_fct_rdd.take(5):
        print(row)

    # Define Schema
    txn_fct_rdd_schema = StructType([
        StructField('txn_id', LongType(), False),
        StructField('create_time', LongType(), False),
        StructField('amount', DoubleType(), True),
        StructField('cust_id', LongType(), True),
        StructField('status', IntegerType(), True),
        StructField('merchant_id', LongType(), True),
        StructField('create_time_ist', StringType(), True)
    ])

    # Create DataFrame
    print('\n**************** Rdd to DF using scheme - sparkSession.createDataFrame(txn_fct_rdd, txn_fct_rdd_schema)')
    txn_fct_df = sparkSession.createDataFrame(txn_fct_rdd, txn_fct_rdd_schema)

    print('\n**************** DF Schema - txn_fct_df.printSchema()')
    txn_fct_df.printSchema()

    print('\n**************** txn_fct_df.show(5) ')
    txn_fct_df.show(5)

    # Transformation on DataFrame using DSL
    txn_fct_df.withColumn('create_time_ist', unix_timestamp())

# Command
#   spark-submit --master 'local[*]' ./dataframe/ingestion/rdd_to_dataframe/rdd_to_df_through_explicit_schema.py

# Output
#