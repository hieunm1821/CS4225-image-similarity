from pyspark import SQLContext
from pyspark.sql import Row
from pyspark.sql import SparkSession
from util import *
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import BucketedRandomProjectionLSH
spark = SparkSession.builder\
        .master("local")\
        .appName("Colab")\
        .config('spark.ui.port', '4050')\
        .getOrCreate()

sqlContext = SQLContext(spark)

df = spark.read.option("header", True).csv("./vector.csv")

def string_to_Vectors(row):
    row_dict = row.asDict()
    string = row_dict["vector"]
    string = list(map(float, string.split(",")))
    vector = Vectors.dense(string)
    row_dict["vector"] = vector
    newrow = Row(**row_dict)
    return newrow
    
df2_rdd = df.rdd.map(lambda x: string_to_Vectors(x))
df2 = sqlContext.createDataFrame(data = df2_rdd)

brp = BucketedRandomProjectionLSH()
brp.setInputCol("vector")
brp.setOutputCol("hashes")
brp.setSeed(12345)
brp.setBucketLength(500)
model = brp.fit(df2)

new_image_path = "./sample.jpg"

list_vec_sample = encode(new_image_path)
vector_sample = Vectors.dense(list_vec_sample)

model.approxNearestNeighbors(df2, vector_sample, 1).show()

