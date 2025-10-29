# Databricks notebook source
# MAGIC %md
# MAGIC #### DATA READING

# COMMAND ----------


df = spark.read.format("parquet")\
               .option("inferSchema", "true")\
               .load("abfss://bronze@carshujatdatalake.dfs.core.windows.net/rawdata/")

# COMMAND ----------

display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC #### DATA TRANSFORMATION

# COMMAND ----------


from pyspark.sql.functions import *
from pyspark.sql.types import*

# COMMAND ----------


df = df.withColumn('Model_Category',split(col('Model_ID'), '-')[0])
display(df)

# COMMAND ----------

df = df.withColumn("RevenuePerUnit", col('Revenue')/col('Units_Sold'))
df.display()

# COMMAND ----------

display(df.groupBy('Year','BranchName').agg(sum('Units_Sold').alias('Total_Sales')).sort('Year','Total_Sales',ascending=[1,0]))
     

# COMMAND ----------

# MAGIC %md
# MAGIC #### DATA WRITING

# COMMAND ----------



df.write.format('parquet').mode('overwrite').option("path","abfss://silver@carshujatdatalake.dfs.core.windows.net/carsales/").save()
     

# COMMAND ----------

# MAGIC
# MAGIC
# MAGIC %sql
# MAGIC SELECT * FROM parquet.`abfss://silver@carshujatdatalake.dfs.core.windows.net/carsales/`

# COMMAND ----------

