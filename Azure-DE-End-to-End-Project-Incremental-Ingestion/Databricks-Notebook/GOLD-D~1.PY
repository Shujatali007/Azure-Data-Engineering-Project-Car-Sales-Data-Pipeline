# Databricks notebook source
from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

# MAGIC %md
# MAGIC ## CREATE FLAG PARAMETER

# COMMAND ----------

dbutils.widgets.text('incremental_flag','0')

# COMMAND ----------

incremental_flag = dbutils.widgets.get('incremental_flag')
print(type('incremental_flag'))

# COMMAND ----------

# MAGIC %md
# MAGIC ## CREATING DIMENSION

# COMMAND ----------

# MAGIC %md
# MAGIC ## fetch relative columns

# COMMAND ----------

df_src = spark.sql('''select distinct (Branch_ID) as Branch_ID, BranchName
         from parquet.`abfss://silver@carshujatdatalake.dfs.core.windows.net/carsales/`
         ''')

# COMMAND ----------

display(df_src)

# COMMAND ----------

# MAGIC %md
# MAGIC ##  dim Branch-sink Initial and incremental(Just bring the schema if table not exists)

# COMMAND ----------

if  spark.catalog.tableExists('carsdatabricks.gold.dim_branch'):
  df_sink = spark.sql('''select  dim_branch_key,Branch_ID, BranchName 
                    from  carsdatabricks.gold.dim_branch
                    ''')
else:
  df_sink = spark.sql('''select 1 as dim_branch_key,Branch_ID,BranchName 
                    from  parquet.`abfss://silver@carshujatdatalake.dfs.core.windows.net/carsales/` 
                    where 1= 0''')

# COMMAND ----------

df_filter = df_src.join(df_sink, df_src.Branch_ID == df_sink.Branch_ID, 'left').select(df_src.Branch_ID,df_src.BranchName,df_sink.dim_branch_key)

# COMMAND ----------

df_filter.display()

# COMMAND ----------

# MAGIC %md
# MAGIC **df_filter_old**

# COMMAND ----------

df_filter_old = df_filter.filter(df_filter.dim_branch_key.isNotNull())

# COMMAND ----------

df_filter_old.display()

# COMMAND ----------

# MAGIC %md
# MAGIC **df_filter_new**

# COMMAND ----------

df_filter_new = df_filter.filter(df_filter.dim_branch_key.isNull()).select(df_src['Branch_ID'],df_src['BranchName'])

# COMMAND ----------

df_filter_new.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Create Surrogate key

# COMMAND ----------

# MAGIC %md
# MAGIC **fetch the max surrogate key***

# COMMAND ----------

if (incremental_flag == '0') :
    max_value = 1
else:
   max_val_df = spark.sql("select max(dim_branch_key) from carsdatabricks.gold.dim_branch")
   max_value = (max_val_df.collect()[0][0]) +1
print(max_value)

# COMMAND ----------

# MAGIC %md
# MAGIC ***create surrorgate key and add the max surrogate key***
# MAGIC

# COMMAND ----------

df_filter_new = df_filter_new.withColumn('dim_branch_key', max_value + monotonically_increasing_id())

# COMMAND ----------

df_filter_new.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ## create final_df = df_filter_old + df_filter_new

# COMMAND ----------

df_final = df_filter_old.union(df_filter_new)
df_final.display()


# COMMAND ----------

# MAGIC %md
# MAGIC # SCD TYPE 1(UPSERT)

# COMMAND ----------

from delta.tables import DeltaTable

# COMMAND ----------

#source-df_Final,dest-dim_branch

    #Incremental run
src = df_final

if spark.catalog.tableExists('carsdatabricks.gold.dim_branch'):
    delta_tbl = DeltaTable.forPath(spark,'abfss://gold@carshujatdatalake.dfs.core.windows.net/dim_branch')    #creating DeltaTable object on top of dim_branch
    delta_tbl.alias('trg').merge (df_final.alias('src'), "trg.dim_branch_key == src.dim_branch_key")\
        .whenMatchedUpdateAll()\
        .whenNotMatchedInsertAll()\
        .execute()
   #initial run
else:
    df_final.write.format('delta')\
        .mode('overwrite')\
        .option('path','abfss://gold@carshujatdatalake.dfs.core.windows.net/dim_branch')\
        .saveAsTable('carsdatabricks.gold.dim_branch')