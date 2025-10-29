# Project Diagrams & Screenshots

This folder contains all architectural diagrams, pipeline visualizations, and screenshots that document the Azure Data Engineering pipeline for car sales data.

## 📊 Diagram Overview

### `architecture.png`
**Overall Solution Architecture**
- **Purpose**: High-level view of the complete Azure data engineering solution
- **Components Shown**:
  - Data sources and ingestion points
  - Azure services integration (ADF, Databricks, ADLS, SQL Database)
  - Data flow between different Azure services
  - Storage layers (Bronze, Silver, Gold)
- **Use Case**: Understanding the overall system design and service interactions
- **Referenced In**: Main README, project documentation, presentations

### `etl_pipeline.png`
**ETL Pipeline Visualization - Primary**
- **Purpose**: Detailed view of the ETL/ELT pipeline workflow
- **Components Shown**:
  - Data sources and extraction processes
  - Azure Data Factory pipeline activities
  - Transformation stages in Databricks
  - Loading processes to different storage layers
- **Use Case**: Technical documentation for pipeline implementation
- **Referenced In**: Pipeline documentation, development guides

### `etl2.png`
**ETL Pipeline Visualization - Secondary**
- **Purpose**: Alternative or complementary view of the ETL processes
- **Components Shown**:
  - Additional pipeline details not covered in primary diagram
  - Incremental loading processes
  - Error handling and monitoring components
  - Data validation checkpoints
- **Use Case**: Comprehensive pipeline documentation, troubleshooting guides
- **Referenced In**: Advanced technical documentation

### `star_schema.png`
**Data Warehouse Star Schema Design**
- **Purpose**: Visual representation of the dimensional model
- **Components Shown**:
  - **Fact Table**: `fact_sales` with measures (Revenue, Units_Sold, RevenuePerUnit)
  - **Dimension Tables**:
    - `dim_date` - Time dimension
    - `dim_branch` - Branch/location dimension
    - `dim_dealer` - Dealer information dimension
    - `dim_model` - Car model dimension
  - Foreign key relationships between fact and dimension tables
- **Use Case**: Database design documentation, data modeling reference
- **Referenced In**: Gold layer documentation, analytics guides

## 🎯 Usage Guidelines

### For Documentation
- **`architecture.png`**: Use in executive summaries and high-level project overviews
- **`etl_pipeline.png` & `etl2.png`**: Include in technical documentation and developer guides
- **`star_schema.png`**: Reference in data modeling and analytics documentation

### For Presentations
- **Executive Presentations**: Focus on `architecture.png` for business stakeholders
- **Technical Presentations**: Combine `etl_pipeline.png` and `star_schema.png` for technical audiences
- **Training Materials**: Use all diagrams to explain different aspects of the solution

### For Development
- **Pipeline Development**: Reference ETL diagrams during Azure Data Factory development
- **Database Design**: Use star schema diagram for Databricks Gold layer implementation
- **System Integration**: Refer to architecture diagram for service configuration

## 📐 Diagram Relationships

### Data Flow Visualization
```
[architecture.png]
       ↓
   High-level data flow
       ↓
[etl_pipeline.png] + [etl2.png]
       ↓
   Detailed ETL processes
       ↓
[star_schema.png]
       ↓
   Final data structure
```

### Technical Depth Levels
1. **Business Level**: `architecture.png` - Shows business value and ROI
2. **Implementation Level**: `etl_pipeline.png`, `etl2.png` - Shows technical implementation
3. **Data Level**: `star_schema.png` - Shows data structure and relationships

## 🔄 Maintenance & Updates

### When to Update Diagrams
- **Architecture Changes**: Update `architecture.png` when adding/removing Azure services
- **Pipeline Modifications**: Update ETL diagrams when changing data flow or processing logic
- **Schema Evolution**: Update `star_schema.png` when adding new dimensions or measures

### Version Control
- Keep previous versions of diagrams for reference
- Document changes made to each diagram
- Ensure consistency across all project documentation

### Tools Used
- Diagrams may have been created using:
  - Microsoft Visio
  - Lucidchart
  - Draw.io
  - Azure Architecture Center templates
  - Custom visualization tools

## 📋 Quality Checklist

### Diagram Standards
- [ ] Clear and readable labels
- [ ] Consistent color coding and symbols
- [ ] Proper flow direction indicators
- [ ] Legend/key when necessary
- [ ] Appropriate resolution for both digital and print use

### Content Accuracy
- [ ] All Azure services correctly represented
- [ ] Data flow directions are accurate
- [ ] Service connections properly shown
- [ ] Current with implemented architecture

## 🖼️ File Details

| File | Format | Recommended Use | Resolution |
|------|--------|----------------|------------|
| `architecture.png` | PNG | Documentation, presentations | High |
| `etl_pipeline.png` | PNG | Technical guides, wikis | High |
| `etl2.png` | PNG | Detailed technical docs | High |
| `star_schema.png` | PNG | Database documentation | High |

## 📖 Integration with Documentation

These diagrams are referenced throughout the project documentation:
- **Main README**: All diagrams linked for comprehensive overview
- **Databricks Notebooks README**: Star schema diagram for data model reference
- **Source Dataset README**: Architecture diagram for data flow context
- **Technical Specifications**: ETL diagrams for implementation details

## 🎨 Visual Design Notes

### Color Coding (if applicable)
- **Blue**: Azure services and components
- **Green**: Data flow and successful processes
- **Orange**: Transformation and processing stages
- **Red**: Error handling and validation points

### Symbols and Icons
- Standard Azure service icons used for consistency
- Arrow styles indicate different types of data flow
- Dotted lines may represent optional or conditional flows
- Bold lines indicate primary data paths