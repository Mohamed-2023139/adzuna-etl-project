import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import (
    explode, col, split, trim,
    regexp_replace, when,
    year, month, size
)

sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

s3_source_path = "s3://adzuna-etl/raw_data/to_process/"
s3_output_path = "s3://adzuna-etl/transformed_data/"

# Read JSON
source_dyf = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    format="json",
    connection_options={"paths": [s3_source_path]}
)

df = source_dyf.toDF()

# Safety check
if "items" not in df.columns:
    raise ValueError("Column 'items' not found in source data")

# Explode items
df = df.withColumn("items", explode(col("items")))

# Select & clean main fields
jobs_df = df.select(
    col("items.id").alias("job_id"),
    col("items.title").alias("job_title"),
    col("items.company.display_name").alias("job_company"),
    col("items.category.label").alias("job_category"),
    col("items.redirect_url").alias("job_url"),
    col("items.created").cast("timestamp").alias("job_created"),
    col("items.location.display_name").alias("job_location")
).dropDuplicates(["job_id"])

# Clean category (remove job / jobs case insensitive)
jobs_df = jobs_df.withColumn(
    "job_category",
    trim(regexp_replace(col("job_category"), "(?i)job[s]?", ""))
)

# Split location into city and region safely
jobs_df = jobs_df.withColumn(
    "location_parts",
    split(col("job_location"), ",")
).withColumn(
    "job_city",
    when(size(col("location_parts")) >= 1, trim(col("location_parts").getItem(0)))
).withColumn(
    "job_region",
    when(size(col("location_parts")) >= 2, trim(col("location_parts").getItem(1)))
).withColumn(
    "job_region",
    when(col("job_region") == "", None).otherwise(col("job_region"))
)

# Drop helper column
jobs_df = jobs_df.drop("job_location", "location_parts")

# Add partition columns
jobs_df = jobs_df.withColumn("year", year(col("job_created"))) \
                 .withColumn("month", month(col("job_created")))

# Write partitioned parquet
jobs_df.write \
    .mode("append") \
    .partitionBy("year", "month") \
    .parquet(s3_output_path)

job.commit()
