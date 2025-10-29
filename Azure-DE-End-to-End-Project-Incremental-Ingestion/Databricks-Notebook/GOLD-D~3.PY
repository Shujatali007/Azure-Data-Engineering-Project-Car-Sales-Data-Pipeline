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

df_src = spark.sql('''select distinct (Dealer_ID) as Dealer_ID, DealerName
         from parquet.`abfss://silver@carshujatdatalake.dfs.core.windows.net/carsales/`
         ''')

# COMMAND ----------

display(df_src)

# COMMAND ----------

# MAGIC %md
# MAGIC ##  dim dealer-sink Initial and incremental(Just bring the schema if table not exists)

# COMMAND ----------

if  spark.catalog.tableExists('carsdatabricks.gold.dim_dealer'):
  df_sink = spark.sql('''select  dim_dealer_key,Dealer_ID, DealerName 
                    from carsdatabricks.gold.dim_dealer
                    ''')
else:
  df_sink = spark.sql('''select 1 as dim_dealer_key,Dealer_ID,DealerName 
                    from  parquet.`abfss://silver@carshujatdatalake.dfs.core.windows.net/carsales/` 
                    where 1= 0''')

# COMMAND ----------

df_filter = df_src.join(df_sink, df_src.Dealer_ID == df_sink.Dealer_ID, 'left').select(df_src.Dealer_ID,df_src.DealerName,df_sink.dim_dealer_key)

# COMMAND ----------

df_filter.display()

# COMMAND ----------

# MAGIC %md
# MAGIC **df_filter_old**

# COMMAND ----------

df_filter_old = df_filter.filter(df_filter.dim_dealer_key.isNotNull())

# COMMAND ----------

# MAGIC %md
# MAGIC **df_filter_new**

# COMMAND ----------

df_filter_new = df_filter.filter(df_filter.dim_dealer_key.isNull()).select(df_src['Dealer_ID'],df_src['DealerName'])

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
   max_val_df = spark.sql("select max(dim_dealer_key) from carsdatabricks.gold.dim_dealer")
   max_value = max_val_df.collect()[0][0]+1  #0th element of 0th row,get value from the dataframe
print(max_value)

# COMMAND ----------

# MAGIC %md
# MAGIC ***create surrorgate key and add the max surrogate key***
# MAGIC

# COMMAND ----------

df_filter_new = df_filter_new.withColumn('dim_dealer_key', max_value + monotonically_increasing_id())

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

#source-df_Final,dest-dim_dealer

    #Incremental run
src = df_final

if spark.catalog.tableExists('carsdatabricks.gold.dim_dealer'):
    delta_tbl = DeltaTable.forPath(spark,'abfss://gold@carshujatdatalake.dfs.core.windows.net/dim_dealer')    #creating DeltaTable object on top of dim_dealer
    delta_tbl.alias('trg').merge (df_final.alias('src'), "trg.dim_dealer_key == src.dim_dealer_key")\
        .whenMatchedUpdateAll()\
        .whenNotMatchedInsertAll()\
        .execute()
   #initial run
else:
    df_final.write.format('delta')\
        .mode('overwrite')\
        .option('path','abfss://gold@carshujatdatalake.dfs.core.windows.net/dim_dealer')\
        .saveAsTable('carsdatabricks.gold.dim_dealer')

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from carsdatabricks.gold.dim_dealer