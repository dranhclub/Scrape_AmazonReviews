import warnings
from pyspark.sql import SparkSession
warnings.filterwarnings('ignore')
# Create Spark session
spark = SparkSession.builder \
    .appName('Amazon Review Analytic') \
    .master('local') \
    .getOrCreate()

data = spark.read.json("./data/All_Beauty_5.json")
asin = data.select('asin').distinct()
asin.coalesce(1).write.save("asin.txt", "text")

