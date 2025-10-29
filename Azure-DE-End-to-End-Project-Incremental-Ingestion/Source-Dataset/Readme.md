# Source Dataset - Car Sales Data

This folder contains the sample datasets used in the Azure Data Engineering pipeline to demonstrate incremental data loading and transformation processes.

## 📊 Dataset Overview

### `SalesData.csv`
**Primary/Historical Sales Dataset**
- **Purpose**: Contains the initial bulk load of historical car sales data
- **Size**: 1,851 records
- **Time Period**: 2017 sales data
- **Usage**: Used for initial data pipeline setup and Bronze layer population

### `IncrementalSales.csv`
**Incremental Sales Dataset**
- **Purpose**: Contains new sales records to demonstrate incremental loading capabilities
- **Size**: 4 records
- **Time Period**: 2020 sales data (newer than historical data)
- **Usage**: Used to test and demonstrate incremental data processing in the pipeline

## 📋 Data Schema

Both datasets share the same schema structure:

| Column Name | Data Type | Description | Example |
|------------|-----------|-------------|---------|
| `Branch_ID` | String | Unique identifier for sales branch | BR0001 |
| `Dealer_ID` | String | Unique identifier for dealer | DLR0001 |
| `Model_ID` | String | Car model identifier with brand prefix | BMW-M1 |
| `Revenue` | Integer | Sales revenue for the transaction | 13363978 |
| `Units_Sold` | Integer | Number of units sold | 2 |
| `Date_ID` | String | Date identifier for the transaction | DT00001 |
| `Day` | Integer | Day of the month (1-31) | 1 |
| `Month` | Integer | Month of the year (1-12) | 1 |
| `Year` | Integer | Year of the transaction | 2017 |
| `BranchName` | String | Name of the sales branch | AC Cars Motors |
| `DealerName` | String | Name of the dealer | AC Cars Motors |
| `Product_Name` | String | Brand name of the car | BMW |

## 🔍 Data Analysis & Insights

### Sample Data Characteristics

#### SalesData.csv (Historical Data)
- **Date Range**: 2017 sales transactions
- **Branch Coverage**: Multiple branches (BR0001 to BR9999+ range)
- **Dealer Network**: Extensive dealer network (DLR0001 to DLR0999+ range)
- **Car Brands**: Multi-brand coverage (BMW, Honda, Tata, Hyundai, Renault, etc.)
- **Revenue Range**: Variable revenue amounts from thousands to millions

#### IncrementalSales.csv (New Data)
- **Date Range**: 2020 sales transactions (3 years after historical data)
- **New Entries**: Contains both existing and new branch/dealer combinations
- **Test Data**: Includes a test record (`XYZ9726`, `XYZ0063`) for validation
- **Pattern**: Consistent schema with historical data

### Key Data Patterns

#### Model ID Structure
- **Format**: `[Brand]-M[Number]` (e.g., BMW-M1, Hon-M218)
- **Brands Included**: BMW, Honda (Hon), Tata (Tat), Hyundai (Hyu), Renault (Ren), Cadillac (Cad), Mercedes-Benz (Mer), Volkswagen (Vol), Jeep (Jee)
- **Usage**: Model_Category is extracted from this field in Silver layer transformation

#### Date Structure
- **Date_ID**: Unique identifier for each date (DT00001, DT00002, etc.)
- **Components**: Separate day, month, year fields for analysis
- **Usage**: Forms the basis for the date dimension table

#### Business Hierarchy
- **Branch → Dealer → Sales**: Clear business hierarchy structure
- **Geographic Distribution**: Multiple branches across different locations
- **Dealer Relationships**: Some dealers serve multiple branches

## 🚀 Pipeline Integration

### Data Ingestion Flow
```
Source-Dataset/
├── SalesData.csv ────────► Azure SQL Database ──► Bronze Layer
└── IncrementalSales.csv ──► Azure SQL Database ──► Bronze Layer
```

### Processing Stages

#### 1. Initial Load (SalesData.csv)
- **Target**: Azure SQL Database
- **Method**: Full data load via Azure Data Factory
- **Destination**: Bronze layer in ADLS Gen2 (Parquet format)

#### 2. Incremental Load (IncrementalSales.csv)
- **Target**: Azure SQL Database (append/update)
- **Method**: Incremental processing via ADF
- **Destination**: Bronze layer (merged with existing data)

#### 3. Transformation Pipeline
- **Silver Layer**: Data cleansing and calculated fields
- **Gold Layer**: Dimensional modeling and star schema creation

## 🔧 Data Quality Considerations

### Data Completeness
- ✅ All required fields populated
- ✅ No missing critical business keys
- ✅ Consistent data types across datasets

### Data Consistency
- ✅ Schema alignment between historical and incremental data
- ✅ Consistent naming conventions
- ✅ Proper format for business identifiers

### Data Accuracy
- ✅ Revenue and units sold are logical
- ✅ Date components are valid
- ✅ Brand prefixes match product names

### Potential Issues
- ⚠️ Some dealer names are very long and may need truncation
- ⚠️ Revenue values vary significantly (may need normalization for analysis)
- ⚠️ Test data in incremental file should be filtered in production

## 📈 Business Use Cases

### Sales Analysis
- **Revenue Trends**: Year-over-year revenue comparison
- **Branch Performance**: Compare sales across different branches
- **Dealer Effectiveness**: Analyze dealer performance metrics
- **Product Mix**: Understand brand and model preferences

### Operational Insights
- **Inventory Planning**: Units sold patterns for forecasting
- **Territory Management**: Branch and dealer relationship analysis
- **Seasonal Trends**: Monthly and daily sales patterns
- **Market Share**: Brand performance across territories

## 🔄 Testing Scenarios

### Initial Load Testing
- Use `SalesData.csv` for full pipeline testing
- Validate Bronze → Silver → Gold transformations
- Verify star schema creation and relationships

### Incremental Load Testing
- Use `IncrementalSales.csv` to test incremental processing
- Validate SCD Type-1 implementation
- Test new vs. existing record handling

### Data Validation Tests
```sql
-- Sample validation queries
SELECT COUNT(*) FROM SalesData;  -- Should return 1,851
SELECT DISTINCT Year FROM SalesData;  -- Should return 2017
SELECT MIN(Revenue), MAX(Revenue) FROM SalesData;  -- Check revenue ranges
```

## 📝 Usage Instructions

### For Development
1. **Initial Setup**: Use `SalesData.csv` for pipeline development
2. **Testing**: Use `IncrementalSales.csv` for incremental load testing
3. **Validation**: Compare record counts and data integrity

### For Production
1. Replace sample files with actual production data
2. Maintain the same schema structure
3. Ensure proper data validation before processing
4. Implement appropriate error handling for data quality issues

## 📊 Sample Queries

### Data Exploration
```sql
-- Top 5 branches by revenue
SELECT TOP 5 BranchName, SUM(Revenue) as Total_Revenue
FROM SalesData
GROUP BY BranchName
ORDER BY Total_Revenue DESC;

-- Monthly sales trend
SELECT Month, SUM(Units_Sold) as Total_Units
FROM SalesData
GROUP BY Month
ORDER BY Month;

-- Brand performance
SELECT Product_Name, COUNT(*) as Transaction_Count, SUM(Revenue) as Total_Revenue
FROM SalesData
GROUP BY Product_Name
ORDER BY Total_Revenue DESC;
```

## 🔒 Data Security & Privacy

### Considerations
- Data appears to be synthetic/sample data for demonstration
- Contains business-sensitive information (revenue, dealer relationships)
- Should be treated as confidential in production environments

### Best Practices
- Implement proper access controls
- Use encryption for data at rest and in transit
- Maintain audit logs for data access
- Consider data masking for non-production environments
