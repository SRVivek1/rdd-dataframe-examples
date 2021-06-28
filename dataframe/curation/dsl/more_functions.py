"""
This program demonstrates other functions from spark APIs.
"""


from pyspark.sql import SparkSession
from pyspark.sql.functions import first, last, trim, lower, col, initcap, ltrim, corr
from model.Person import Person


if __name__ == '__main__':
    """
    Driver program.
    """

    sparkSession = SparkSession\
        .builder\
        .appName('spark-api-functions-demo')\
        .getOrCreate()
    sparkSession.sparkContext.setLogLevel('ERROR')

    print('\n**************************** SPARK pyspark.sql.functions method demo ****************************\n')
    # Create dataframe from person list.
    people_df = sparkSession.createDataFrame([
        Person("Sidhartha", "Ray", 32, None, "Programmer"),
        Person("Pratik", "Solanki", 22, 176.7, None),
        Person("Ashok ", "Pradhan", 62, None, None),
        Person(" ashok", "Pradhan", 42, 125.3, "Chemical Engineer"),
        Person("Pratik", "Solanki", 22, 222.2, "Teacher")
    ])

    print('\n**************** people_df.printSchema()')
    people_df.printSchema()

    print('\n**************** people_df.show(truncate=False)')
    people_df.show(truncate=False)

    # first(...) method.
    print('\n**************** people_df.groupBy(\'firstName\').agg(first(\'weightInLbs\')).show(truncate=False)')
    people_df\
        .groupBy('firstName')\
        .agg(first('weightInLbs'))\
        .show(truncate=False)

    # last(...) method
    print('\n**************** people_df.groupBy(\'firstName\').agg(last(\'weightInLbs\')).show(truncate=False)')
    people_df\
        .groupBy('firstName')\
        .agg(last('weightInLbs'))\
        .show(truncate=False)

    # lower(...) & trim(...) methods
    print("\n***************** people_df"
          ".groupBy(trim(lower(col('firstName')))).agg(first('weightInLbs')).show(truncate=False)")
    people_df\
        .groupBy(trim(lower(col('firstName'))))\
        .agg(first('weightInLbs'))\
        .show(truncate=False)

    # lower(...) & trim(...) methods
    print("\n***************** people_df"
          ".groupBy(trim(lower(col('firstName')))).agg(last('weightInLbs')).show(truncate=False)")
    people_df\
        .groupBy(trim(lower(col('firstName'))))\
        .agg(last('weightInLbs'))\
        .show(truncate=False)

    # last(...) ignore nulls
    print("\n***************** people_df"
          ".groupBy(trim(lower(col('firstName')))).agg(last('weightInLbs', True)).show(truncate=False)")
    people_df\
        .groupBy(trim(lower(col('firstName'))))\
        .agg(last('weightInLbs', True))\
        .show(truncate=False)

    # Sort weightInLbs column in desc order then find records
    print("\n************* people_df.sort(col('weightInLbs').desc())"
          ".groupBy(trim(lower(col('firstName')))).agg(first('weightInLbs', True)).show(truncate=False)")
    people_df\
        .sort(col('weightInLbs').desc())\
        .groupBy(trim(lower(col('firstName'))))\
        .agg(first('weightInLbs', True))\
        .show(truncate=False)

    # Sort weightInLbs column in asc order where null appear in last
    print("\n************** people_df.sort(col('weighInLbs').asc_nulls_last())"
          ".groupBy(trim(lower(col('firstName')))).agg(first(col('weightInLbs'))).show(truncate=False)")
    people_df.sort(col('weightInLbs').asc_nulls_last())\
        .groupBy(trim(lower(col('firstName'))))\
        .agg(first(col('weightInLbs')))\
        .show(truncate=False)

    # Data cleaning / correction - using withColumn(...), initcap(..), ltrim(...) & trim(...)
    print('\n************ Data cleaning / correction - using withColumn(...), initcap(..), ltrim(...) & trim(...)')

    corrected_people_df = people_df.withColumn('firstName', initcap('firstName'))
    print("\n************ corrected_people_df = people_df.withColumn('firstName', initcap('firstName'))")
    corrected_people_df.show(truncate=False)

    corrected_people_df = corrected_people_df.withColumn('firstName', ltrim(initcap('firstName')))
    print("\n************ corrected_people_df = corrected_people_df.withColumn('firstName', ltrim(initcap('firstName')))")
    corrected_people_df.show(truncate=False)

    corrected_people_df = corrected_people_df.withColumn('firstName', trim(initcap('firstName')))
    print("\n************ corrected_people_df = corrected_people_df.withColumn('firstName', trim(initcap('firstName')))")
    corrected_people_df.show(truncate=False)
