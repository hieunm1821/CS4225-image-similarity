from pyspark import SQLContext
from pyspark.sql import SparkSession
from util import *
spark = SparkSession.builder\
        .master("local")\
        .appName("Colab")\
        .config('spark.ui.port', '4050')\
        .getOrCreate()

sqlContext = SQLContext(spark)

df = spark.read.option("header", True).csv("./data_10.csv")
 
df_rdd = df.rdd

df2_rdd = df_rdd.map(lambda row: encode_row(row))
df2 = sqlContext.createDataFrame(data = df2_rdd)
# df2.write.csv("output.csv")
df2.repartition(1).write.format('com.databricks.spark.csv').save("output", header = 'true')
