# Data Quality Audit - Task 24

**Internship Task:** Data Quality Audit  
**Track:** Data Analytics  
**Intern:** Archana  
**Organization:** vedatechnology.in

## Overview

This project implements a comprehensive data quality audit tool using Python and Pandas. The tool audits datasets for missing values, duplicate records, range violations, and consistency issues, then generates detailed reports and cleaned sample data.

## Project Deliverables

- ✅ **Audit Report** (JSON & TXT format) - Comprehensive quality metrics
- ✅ **Issue Log** (CSV format) - Detailed log of all data quality issues
- ✅ **Cleaned Sample** - Dataset with quality issues resolved
- ✅ **Repeatable Quality Checklist** - Reusable audit framework

## Dataset Used

**Sample Superstore Dataset** - A retail sales dataset containing:
- Order information (Order ID, Order Date, Ship Date)
- Customer details (Customer ID, Customer Name, Segment)
- Product information (Category, Sub-Category, Product Name)
- Sales metrics (Sales, Quantity, Discount, Profit)
- Geographic data (City, State, Region)

The sample dataset intentionally includes data quality issues to demonstrate the audit capabilities.

## Approach

### 1. Missing Value Analysis
- Identifies columns with missing data
- Calculates missing percentage per column
- Quantifies overall missing rate
- Categorizes severity based on impact

### 2. Duplicate Detection
- Identifies completely duplicate rows
- Checks for duplicates in key columns
- Quantifies duplicate percentage
- Recommends removal strategies

### 3. Range Validation
- Analyzes numeric columns for outliers using IQR method
- Checks for inappropriate negative values
- Provides statistical summaries (min, max, mean, std)
- Flags values outside expected ranges

### 4. Consistency Checks
- Detects case inconsistencies in categorical data
- Identifies whitespace issues
- Validates date ranges
- Checks for format inconsistencies

### 5. Quality Scoring
- Calculates overall data quality score (0-100)
- Categorizes issues by severity (High, Medium, Low)
- Provides actionable recommendations

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup

1. Clone or download this repository
2. Install required dependencies:
```bash
pip install -r requirements.txt
```

Required packages:
- pandas==2.1.4
- numpy==1.26.2
- openpyxl==3.1.2

## Usage

### Running the Audit

1. Place your dataset (CSV or Excel) in the project directory
2. Run the audit script:
```bash
python data_quality_audit.py
```

3. When prompted, enter the path to your dataset:
```
Enter path to dataset (CSV or Excel): sample_superstore.csv
```

### Using the Sample Dataset

The project includes a sample Superstore dataset with intentional quality issues:
```bash
python data_quality_audit.py
# Enter: sample_superstore.csv
```

## Output Files

The audit generates the following files (timestamped):

### 1. `audit_report_YYYYMMDD_HHMMSS.json`
Detailed JSON report containing:
- Missing value analysis
- Duplicate detection results
- Range validation statistics
- Consistency check findings
- Overall quality score

### 2. `issue_log_YYYYMMDD_HHMMSS.csv`
CSV file with columns:
- Issue Type
- Column
- Severity
- Description
- Recommendation

### 3. `audit_report_YYYYMMDD_HHMMSS.txt`
Human-readable text report with:
- Executive summary
- Detailed issue descriptions
- Recommendations for each issue

### 4. `cleaned_sample_YYYYMMDD_HHMMSS.csv` (or .xlsx)
Cleaned version of the dataset with:
- Duplicate rows removed
- Missing values imputed (median for numeric, mode for categorical)
- Whitespace trimmed from string columns
- Data type consistency ensured

## Data Quality Rules Implemented

### Validation Rules

1. **Missing Value Threshold**
   - High Severity: >20% missing
   - Medium Severity: 5-20% missing
   - Low Severity: <5% missing

2. **Duplicate Threshold**
   - High Severity: >5% duplicate rows
   - Medium Severity: 1-5% duplicate rows
   - Low Severity: <1% duplicate rows

3. **Outlier Detection**
   - Uses IQR method (Interquartile Range)
   - Values outside Q1-1.5*IQR or Q3+1.5*IQR flagged
   - Percentage-based severity classification

4. **Consistency Rules**
   - Case sensitivity in categorical fields
   - Leading/trailing whitespace
   - Date range validation

## Quality Score Calculation

The overall quality score is calculated as:
```
Base Score: 100
- (High Severity Issues × 10)
- (Medium Severity Issues × 5)
- (Low Severity Issues × 2)
= Final Quality Score (minimum 0)
```

## Issue Prioritization

Issues are prioritized based on:

1. **High Priority**
   - >20% missing values in critical columns
   - >5% duplicate records
   - Extreme outliers affecting analysis
   - Invalid data types

2. **Medium Priority**
   - 5-20% missing values
   - 1-5% duplicates
   - Moderate outliers
   - Negative values in inappropriate fields

3. **Low Priority**
   - <5% missing values
   - <1% duplicates
   - Minor consistency issues
   - Whitespace problems

## Interview Question Answers

### Q1: What makes a quality rule useful?

A quality rule is useful when it:
- **Addresses Business Impact**: Rules should focus on issues that affect decision-making
- **Is Measurable**: Can be quantified with clear thresholds
- **Is Actionable**: Provides clear remediation steps
- **Is Repeatable**: Can be consistently applied across datasets
- **Is Context-Aware**: Considers domain-specific requirements
- **Has Sufficient Granularity**: Identifies specific issues rather than general problems

### Q2: How do you prioritize issues?

Issues are prioritized based on:
1. **Impact on Analysis**: How significantly the issue affects insights
2. **Data Volume**: Percentage of records affected
3. **Business Criticality**: Importance of the affected field
4. **Ease of Resolution**: Complexity of fixing the issue
5. **Downstream Effects**: Impact on dependent processes

High-severity issues that affect large portions of critical data fields are addressed first.

## Project Structure

```
day 24/
├── data_quality_audit.py      # Main audit script
├── requirements.txt            # Python dependencies
├── sample_superstore.csv       # Sample dataset with issues
├── README.md                   # This file
├── audit_report_*.json         # Generated audit report
├── issue_log_*.csv             # Generated issue log
├── audit_report_*.txt          # Human-readable report
└── cleaned_sample_*.csv        # Cleaned dataset
```

## Key Features

- **Comprehensive Analysis**: Covers 4 major quality dimensions
- **Automated Reporting**: Generates multiple output formats
- **Severity Classification**: Categorizes issues by impact
- **Actionable Recommendations**: Provides specific fix suggestions
- **Data Cleaning**: Automatically generates cleaned sample
- **Reusable Framework**: Can be applied to any dataset

## Limitations

- Domain-specific rules may need customization
- Outlier detection uses statistical methods (may not suit all contexts)
- Missing value imputation uses simple strategies (median/mode)
- Date validation assumes reasonable time ranges

## Future Enhancements

- Add domain-specific validation rules
- Implement advanced imputation methods
- Add data profiling visualizations
- Support for additional file formats (Parquet, JSON)
- Integration with data pipelines
- Automated alerting for quality thresholds


---


