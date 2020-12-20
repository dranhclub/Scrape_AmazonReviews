import warnings
import os
from pyspark.sql import SparkSession

warnings.filterwarnings('ignore')

# Create Spark session
spark = SparkSession.builder \
    .appName('Amazon Review Analytic') \
    .master('local') \
    .getOrCreate()

dir_path = '../data/json/'
for filename in os.listdir(dir_path):
    data = spark.read.json(dir_path + filename)
    asin = data.select('asin').distinct()
    # asin.coalesce(1).write.save("asin.txt", "text")
    asin.toPandas().to_csv(f'../data/asin_list/{filename}.csv')