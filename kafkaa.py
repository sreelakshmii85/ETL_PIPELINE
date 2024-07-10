from pyspark.sql import SparkSession
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# MongoDB connection URI
mongo_uri = os.getenv("mongodb_url")

# Initialize Spark session
spark = SparkSession.builder \
    .appName("YourAppName") \
    .config("spark.jars.packages",
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
    .config("spark.jars.repositories", "https://repo.maven.apache.org/maven2") \
    .config("spark.mongodb.input.uri", mongo_uri) \
    .config("spark.mongodb.output.uri", mongo_uri)\
    .getOrCreate()

# Kafka parameters
kafka_bootstrap_servers = "localhost:9092"
kafka_topic = "my_topic"

# Read from Kafka
df = spark.read \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", kafka_topic) \
    .load()

# Process the data from Kafka
processed_df = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

# Show the processed data
processed_df.show()

# Write processed data to MongoDB
processed_df.write \
    .format("com.mongodb.spark.sql.DefaultSource") \
    .mode("append") \
    .option("uri", mongo_uri) \
    .option("database", "test") \
    .option("collection", "demo") \
    .save()

# Stop the Spark session
spark.stop()

