# Databricks Notebooks - Car Sales Data Pipeline

This folder contains all the Azure Databricks notebooks and Python scripts used for data transformation in the Medallion architecture (Bronze → Silver → Gold layers).

## 📋 Execution Order

Execute the notebooks in the following sequence for proper data pipeline flow:

1. **`db_notebook.py`** - Schema Creation (One-time setup)
2. **`Silver_nb.ipynb`** - Bronze to Silver transformation
3. **Dimension Tables** (can be run in parallel):
   - `Gold-dim_branch.py`
   - `Gold-dim_date.py`
   - `Gold-dim_dealer.py`
   - `Gold-dim_model.py`
4. **`gold-fact-sales.py`** - Fact table creation (run after all dimensions)

## 📁 File Descriptions

### Initial Setup
- **`db_notebook.py`** 
  - Creates the required database schemas (`carsdatabricks.silver` and `carsdatabricks.gold`)
  - One-time execution required before running other notebooks

### Silver Layer Transformation
- **`Silver_nb.ipynb`** / **`Silver_nb.py`**
  - **Purpose**: Transforms raw Bronze layer data into cleaned Silver layer
  - **Input**: Parquet files from Bronze layer (`abfss://bronze@carshujatdatalake.dfs.core.windows.net/rawdata/`)
  - **Transformations**:
    - Extracts `Model_Category` from `Model_ID` using string split
    - Calculates `RevenuePerUnit` (Revenue ÷ Units_Sold)
    - Aggregates sales data by Year and Branch
  - **Output**: Cleaned data in Silver layer (`abfss://silver@carshujatdatalake.dfs.core.windows.net/carsales/`)

### Gold Layer - Dimension Tables

#### `Gold-dim_branch.py`
- **Purpose**: Creates and maintains Branch dimension table
- **Features**:
  - SCD Type-1 implementation with UPSERT operations
  - Incremental processing with configurable flags
  - Surrogate key generation using `monotonically_increasing_id()`
- **Parameters**: `incremental_flag` (0 for initial load, 1 for incremental)
- **Output**: `carsdatabricks.gold.dim_branch`

#### `Gold-dim_date.py`
- **Purpose**: Creates and maintains Date dimension table
- **Features**:
  - Extracts unique dates from Silver layer
  - Generates surrogate keys for new date records
  - Implements SCD Type-1 for date updates
- **Parameters**: `incremental_flag`
- **Output**: `carsdatabricks.gold.dim_date`

#### `Gold-dim_dealer.py`
- **Purpose**: Creates and maintains Dealer dimension table
- **Features**:
  - Processes dealer information from Silver layer
  - Handles new dealer additions incrementally
  - Maintains dealer hierarchy and attributes
- **Parameters**: `incremental_flag`
- **Output**: `carsdatabricks.gold.dim_dealer`

#### `Gold-dim_model.py`
- **Purpose**: Creates and maintains Model dimension table
- **Features**:
  - Manages car model information and categorization
  - Includes model metadata and classifications
  - Supports incremental updates for new models
- **Parameters**: `incremental_flag`
- **Output**: `carsdatabricks.gold.dim_model`

### Gold Layer - Fact Table

#### `gold-fact-sales.py`
- **Purpose**: Creates the central fact table for the star schema
- **Features**:
  - Joins Silver layer data with all dimension tables
  - Retrieves foreign keys from dimension tables
  - Implements MERGE operations for incremental updates
  - Maintains referential integrity
- **Input**: Silver layer data + all dimension tables
- **Output**: `carsdatabricks.gold.factsales`
- **Key Metrics**: Revenue, Units_Sold, RevenuePerUnit

## 🔧 Technical Implementation Details

### SCD Type-1 Implementation
All dimension tables implement Slowly Changing Dimension Type-1:
```python
# Pattern used across dimension tables
if spark.catalog.tableExists('table_name'):
    delta_tbl = DeltaTable.forPath(spark, 'path_to_table')
    delta_tbl.alias('trg').merge(df_final.alias('src'), "join_condition")
        .whenMatchedUpdateAll()
        .whenNotMatchedInsertAll()
        .execute()
else:
    # Initial load
    df_final.write.format('delta').mode('overwrite').saveAsTable('table_name')
```

### Incremental Processing
- **Initial Load**: Set `incremental_flag = '0'`
- **Incremental Load**: Set `incremental_flag = '1'`
- Surrogate key generation handles both scenarios automatically

### Data Storage Format
- **Bronze Layer**: Parquet format for efficient storage and querying
- **Silver Layer**: Parquet format with cleaned and transformed data
- **Gold Layer**: Delta Lake format for ACID transactions and versioning

## 🏗️ Star Schema Architecture

```
                    ┌─────────────────┐
                    │   dim_date      │
                    │ - dim_date_key  │
                    │ - Date_ID       │
                    └─────────────────┘
                            │
                            │
    ┌─────────────────┐     │     ┌─────────────────┐
    │   dim_branch    │     │     │   dim_dealer    │
    │ - dim_branch_key│     │     │ - dim_dealer_key│
    │ - Branch_ID     │     │     │ - Dealer_ID     │
    │ - BranchName    │     │     │ - DealerName    │
    └─────────────────┘     │     └─────────────────┘
            │               │               │
            └───────────────┼───────────────┘
                            │
                    ┌─────────────────┐
                    │   fact_sales    │
                    │ - Revenue       │
                    │ - Units_Sold    │
                    │ - RevenuePerUnit│
                    │ - dim_date_key  │
                    │ - dim_branch_key│
                    │ - dim_dealer_key│
                    │ - dim_model_key │
                    └─────────────────┘
                            │
                    ┌─────────────────┐
                    │   dim_model     │
                    │ - dim_model_key │
                    │ - Model_ID      │
                    │ - Model_Category│
                    └─────────────────┘
```

## 🚀 Prerequisites & Setup

### Prerequisites
- Azure Databricks workspace configured
- Access to Azure Data Lake Storage Gen2
- Proper permissions for reading/writing to storage containers
- PySpark and Delta Lake libraries available

### Environment Setup
1. Ensure Bronze layer data is available
2. Configure storage account connection strings
3. Set up database schemas using `db_notebook.py`
4. Configure notebook parameters as needed

### Parameters Configuration
Most notebooks accept the following parameter:
- `incremental_flag`: Set to '0' for initial load, '1' for incremental processing

## 📊 Monitoring & Validation

### Data Quality Checks
- Verify record counts between layers
- Check for duplicate surrogate keys
- Validate referential integrity in fact table
- Monitor processing time and performance metrics

### Troubleshooting
- Check storage account access permissions
- Verify schema exists before running Gold layer notebooks
- Ensure proper execution order (dimensions before fact table)
- Monitor Spark UI for performance bottlenecks

## 🔄 Maintenance

### Regular Tasks
- Monitor incremental processing performance
- Review and optimize Spark configurations
- Update storage connection strings as needed
- Archive old log files and temporary data

### Scaling Considerations
- Adjust cluster size based on data volume
- Implement partitioning strategies for large datasets
- Consider auto-scaling policies for cost optimization
