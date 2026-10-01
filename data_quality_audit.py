"""
Data Quality Audit Script
Task 24: Data Quality Audit for Internship at vedatechnology.in

This script performs a comprehensive data quality audit including:
- Missing value analysis
- Duplicate detection
- Range validation
- Consistency checks
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json
import os
import sys


class DataQualityAuditor:
    """Comprehensive data quality auditing tool"""
    
    def __init__(self, filepath):
        """Initialize auditor with dataset"""
        self.filepath = filepath
        self.df = None
        self.audit_results = {}
        self.issue_log = []
        
    def load_data(self):
        """Load dataset based on file extension"""
        try:
            if self.filepath.endswith('.csv'):
                self.df = pd.read_csv(self.filepath)
            elif self.filepath.endswith('.xlsx') or self.filepath.endswith('.xls'):
                self.df = pd.read_excel(self.filepath)
            else:
                raise ValueError("Unsupported file format. Use CSV or Excel.")
            
            print(f"✓ Successfully loaded dataset: {self.df.shape[0]} rows, {self.df.shape[1]} columns")
            return True
        except Exception as e:
            print(f"✗ Error loading data: {e}")
            return False
    
    def check_missing_values(self):
        """Audit for missing values"""
        print("\n" + "="*60)
        print("1. MISSING VALUE ANALYSIS")
        print("="*60)
        
        missing_counts = self.df.isnull().sum()
        missing_percentages = (self.df.isnull().sum() / len(self.df)) * 100
        
        missing_report = pd.DataFrame({
            'Column': self.df.columns,
            'Missing Count': missing_counts.values,
            'Missing Percentage': missing_percentages.values
        })
        
        missing_report = missing_report[missing_report['Missing Count'] > 0].sort_values(
            'Missing Count', ascending=False
        )
        
        total_missing = self.df.isnull().sum().sum()
        total_cells = self.df.shape[0] * self.df.shape[1]
        overall_missing_rate = (total_missing / total_cells) * 100
        
        print(f"Total missing values: {total_missing}")
        print(f"Overall missing rate: {overall_missing_rate:.2f}%")
        print("\nColumns with missing values:")
        print(missing_report.to_string(index=False))
        
        # Log issues
        for _, row in missing_report.iterrows():
            self.issue_log.append({
                'Issue Type': 'Missing Value',
                'Column': row['Column'],
                'Severity': 'High' if row['Missing Percentage'] > 20 else 'Medium' if row['Missing Percentage'] > 5 else 'Low',
                'Description': f"{row['Missing Count']} missing values ({row['Missing Percentage']:.2f}%)",
                'Recommendation': 'Impute or remove missing values based on business context'
            })
        
        self.audit_results['missing_values'] = {
            'total_missing': int(total_missing),
            'overall_missing_rate': float(overall_missing_rate),
            'columns_with_missing': len(missing_report),
            'details': missing_report.to_dict('records')
        }
        
        return missing_report
    
    def check_duplicates(self):
        """Audit for duplicate records"""
        print("\n" + "="*60)
        print("2. DUPLICATE RECORD ANALYSIS")
        print("="*60)
        
        # Check for completely duplicate rows
        duplicate_rows = self.df.duplicated().sum()
        duplicate_percentage = (duplicate_rows / len(self.df)) * 100
        
        print(f"Completely duplicate rows: {duplicate_rows} ({duplicate_percentage:.2f}%)")
        
        # Check for duplicates in key columns (if they exist)
        key_columns = self.df.select_dtypes(include=['object']).columns.tolist()
        key_column_duplicates = {}
        
        for col in key_columns[:5]:  # Check first 5 categorical columns
            duplicates = self.df[col].duplicated().sum()
            if duplicates > 0:
                key_column_duplicates[col] = {
                    'count': int(duplicates),
                    'percentage': float((duplicates / len(self.df)) * 100)
                }
        
        print(f"\nDuplicates in key columns:")
        for col, stats in key_column_duplicates.items():
            print(f"  {col}: {stats['count']} duplicates ({stats['percentage']:.2f}%)")
        
        # Log issues
        if duplicate_rows > 0:
            self.issue_log.append({
                'Issue Type': 'Duplicate Records',
                'Column': 'All Columns',
                'Severity': 'High' if duplicate_percentage > 5 else 'Medium',
                'Description': f"{duplicate_rows} completely duplicate rows ({duplicate_percentage:.2f}%)",
                'Recommendation': 'Remove duplicate rows, keeping first occurrence'
            })
        
        for col, stats in key_column_duplicates.items():
            self.issue_log.append({
                'Issue Type': 'Duplicate Values',
                'Column': col,
                'Severity': 'Low',
                'Description': f"{stats['count']} duplicate values in {col} ({stats['percentage']:.2f}%)",
                'Recommendation': 'Review if duplicates are expected for this field'
            })
        
        self.audit_results['duplicates'] = {
            'total_duplicate_rows': int(duplicate_rows),
            'duplicate_percentage': float(duplicate_percentage),
            'key_column_duplicates': key_column_duplicates
        }
        
        return duplicate_rows
    
    def check_range_validation(self):
        """Audit for data range issues"""
        print("\n" + "="*60)
        print("3. RANGE VALIDATION")
        print("="*60)
        
        numeric_columns = self.df.select_dtypes(include=[np.number]).columns
        range_issues = []
        
        for col in numeric_columns:
            col_data = self.df[col].dropna()
            
            # Basic statistics
            min_val = col_data.min()
            max_val = col_data.max()
            mean_val = col_data.mean()
            std_val = col_data.std()
            
            # Check for outliers using IQR method
            Q1 = col_data.quantile(0.25)
            Q3 = col_data.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = col_data[(col_data < lower_bound) | (col_data > upper_bound)]
            outlier_count = len(outliers)
            outlier_percentage = (outlier_count / len(col_data)) * 100
            
            # Check for negative values where they might not make sense
            negative_count = (col_data < 0).sum()
            
            range_info = {
                'column': col,
                'min': float(min_val),
                'max': float(max_val),
                'mean': float(mean_val),
                'std': float(std_val),
                'outlier_count': int(outlier_count),
                'outlier_percentage': float(outlier_percentage),
                'negative_count': int(negative_count)
            }
            
            print(f"\n{col}:")
            print(f"  Range: [{min_val:.2f}, {max_val:.2f}]")
            print(f"  Mean: {mean_val:.2f}, Std: {std_val:.2f}")
            print(f"  Outliers: {outlier_count} ({outlier_percentage:.2f}%)")
            if negative_count > 0:
                print(f"  Negative values: {negative_count}")
            
            if outlier_count > 0:
                range_issues.append(range_info)
                self.issue_log.append({
                    'Issue Type': 'Outlier',
                    'Column': col,
                    'Severity': 'Medium' if outlier_percentage > 5 else 'Low',
                    'Description': f"{outlier_count} outliers detected ({outlier_percentage:.2f}%)",
                    'Recommendation': 'Review outliers for data entry errors or legitimate extreme values'
                })
            
            if negative_count > 0 and col not in ['discount', 'profit', 'loss']:
                self.issue_log.append({
                    'Issue Type': 'Negative Value',
                    'Column': col,
                    'Severity': 'Medium',
                    'Description': f"{negative_count} negative values in {col}",
                    'Recommendation': 'Verify if negative values are valid for this metric'
                })
        
        self.audit_results['range_validation'] = {
            'numeric_columns_analyzed': len(numeric_columns),
            'columns_with_outliers': len(range_issues),
            'details': range_issues
        }
        
        return range_issues
    
    def check_consistency(self):
        """Audit for data consistency issues"""
        print("\n" + "="*60)
        print("4. CONSISTENCY CHECKS")
        print("="*60)
        
        consistency_issues = []
        
        # Check for inconsistent string formats in categorical columns
        categorical_columns = self.df.select_dtypes(include=['object']).columns
        
        for col in categorical_columns:
            unique_values = self.df[col].dropna().unique()
            
            # Check for case inconsistencies
            if len(unique_values) > 1 and len(unique_values) < 50:
                lower_unique = set(str(v).lower() for v in unique_values)
                if len(lower_unique) < len(unique_values):
                    case_issues = len(unique_values) - len(lower_unique)
                    print(f"\n{col}: {case_issues} case inconsistencies detected")
                    print(f"  Sample values: {list(unique_values[:5])}")
                    
                    consistency_issues.append({
                        'column': col,
                        'issue_type': 'case_inconsistency',
                        'count': case_issues
                    })
                    
                    self.issue_log.append({
                        'Issue Type': 'Case Inconsistency',
                        'Column': col,
                        'Severity': 'Low',
                        'Description': f"{case_issues} case inconsistencies in {col}",
                        'Recommendation': 'Standardize to lowercase or title case'
                    })
            
            # Check for whitespace issues
            whitespace_issues = self.df[col].apply(
                lambda x: isinstance(x, str) and (x != x.strip())
            ).sum()
            
            if whitespace_issues > 0:
                print(f"\n{col}: {whitespace_issues} values with leading/trailing whitespace")
                consistency_issues.append({
                    'column': col,
                    'issue_type': 'whitespace',
                    'count': int(whitespace_issues)
                })
                
                self.issue_log.append({
                    'Issue Type': 'Whitespace',
                    'Column': col,
                    'Severity': 'Low',
                    'Description': f"{whitespace_issues} values with extra whitespace in {col}",
                    'Recommendation': 'Strip leading/trailing whitespace'
                })
        
        # Check date columns for consistency
        date_columns = self.df.select_dtypes(include=['datetime64']).columns
        for col in date_columns:
            date_range = self.df[col].max() - self.df[col].min()
            print(f"\n{col}: Date range spans {date_range.days} days")
            
            if date_range.days > 365 * 10:  # More than 10 years
                self.issue_log.append({
                    'Issue Type': 'Date Range',
                    'Column': col,
                    'Severity': 'Medium',
                    'Description': f"Date range spans {date_range.days} days ({date_range.days/365:.1f} years)",
                    'Recommendation': 'Verify if this date range is expected'
                })
        
        self.audit_results['consistency'] = {
            'categorical_columns_analyzed': len(categorical_columns),
            'issues_found': len(consistency_issues),
            'details': consistency_issues
        }
        
        return consistency_issues
    
    def generate_audit_report(self):
        """Generate comprehensive audit report"""
        print("\n" + "="*60)
        print("5. AUDIT SUMMARY")
        print("="*60)
        
        # Overall quality score
        total_issues = len(self.issue_log)
        high_severity = sum(1 for issue in self.issue_log if issue['Severity'] == 'High')
        medium_severity = sum(1 for issue in self.issue_log if issue['Severity'] == 'Medium')
        low_severity = sum(1 for issue in self.issue_log if issue['Severity'] == 'Low')
        
        print(f"\nTotal Issues Found: {total_issues}")
        print(f"  - High Severity: {high_severity}")
        print(f"  - Medium Severity: {medium_severity}")
        print(f"  - Low Severity: {low_severity}")
        
        # Calculate quality score (0-100)
        quality_score = max(0, 100 - (high_severity * 10) - (medium_severity * 5) - (low_severity * 2))
        print(f"\nData Quality Score: {quality_score}/100")
        
        self.audit_results['summary'] = {
            'total_issues': total_issues,
            'high_severity': high_severity,
            'medium_severity': medium_severity,
            'low_severity': low_severity,
            'quality_score': quality_score
        }
        
        return self.audit_results
    
    def save_reports(self):
        """Save audit report and issue log to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save audit report as JSON
        with open(f'audit_report_{timestamp}.json', 'w') as f:
            json.dump(self.audit_results, f, indent=2, default=str)
        print(f"\n✓ Audit report saved: audit_report_{timestamp}.json")
        
        # Save issue log as CSV
        issue_df = pd.DataFrame(self.issue_log)
        issue_df.to_csv(f'issue_log_{timestamp}.csv', index=False)
        print(f"✓ Issue log saved: issue_log_{timestamp}.csv")
        
        # Save detailed text report
        with open(f'audit_report_{timestamp}.txt', 'w') as f:
            f.write("="*70 + "\n")
            f.write("DATA QUALITY AUDIT REPORT\n")
            f.write("="*70 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Dataset: {self.filepath}\n")
            f.write(f"Rows: {self.df.shape[0]}, Columns: {self.df.shape[1]}\n\n")
            
            f.write("="*70 + "\n")
            f.write("SUMMARY\n")
            f.write("="*70 + "\n")
            f.write(f"Total Issues: {len(self.issue_log)}\n")
            f.write(f"Quality Score: {self.audit_results['summary']['quality_score']}/100\n\n")
            
            f.write("="*70 + "\n")
            f.write("ISSUE LOG\n")
            f.write("="*70 + "\n")
            for i, issue in enumerate(self.issue_log, 1):
                f.write(f"\n{i}. {issue['Issue Type']} - {issue['Column']}\n")
                f.write(f"   Severity: {issue['Severity']}\n")
                f.write(f"   Description: {issue['Description']}\n")
                f.write(f"   Recommendation: {issue['Recommendation']}\n")
        
        print(f"✓ Text report saved: audit_report_{timestamp}.txt")
        
        return timestamp
    
    def clean_data(self):
        """Generate cleaned sample dataset"""
        print("\n" + "="*60)
        print("6. GENERATING CLEANED SAMPLE")
        print("="*60)
        
        df_cleaned = self.df.copy()
        
        # Remove completely duplicate rows
        before_duplicates = df_cleaned.duplicated().sum()
        df_cleaned = df_cleaned.drop_duplicates()
        after_duplicates = df_cleaned.duplicated().sum()
        print(f"Removed {before_duplicates - after_duplicates} duplicate rows")
        
        # Handle missing values based on data type
        for col in df_cleaned.columns:
            missing_count = df_cleaned[col].isnull().sum()
            if missing_count > 0:
                if df_cleaned[col].dtype in ['int64', 'float64']:
                    # Fill numeric with median
                    df_cleaned[col].fillna(df_cleaned[col].median(), inplace=True)
                    print(f"Filled {missing_count} missing values in {col} with median")
                else:
                    # Fill categorical with mode or 'Unknown'
                    if df_cleaned[col].mode().empty:
                        df_cleaned[col].fillna('Unknown', inplace=True)
                    else:
                        df_cleaned[col].fillna(df_cleaned[col].mode()[0], inplace=True)
                    print(f"Filled {missing_count} missing values in {col}")
        
        # Strip whitespace from string columns
        string_columns = df_cleaned.select_dtypes(include=['object']).columns
        for col in string_columns:
            df_cleaned[col] = df_cleaned[col].astype(str).str.strip()
        
        print(f"\n✓ Cleaned dataset created: {df_cleaned.shape[0]} rows, {df_cleaned.shape[1]} columns")
        
        return df_cleaned
    
    def run_full_audit(self):
        """Run complete data quality audit"""
        print("="*60)
        print("DATA QUALITY AUDIT")
        print("="*60)
        
        if not self.load_data():
            return False
        
        # Run all checks
        self.check_missing_values()
        self.check_duplicates()
        self.check_range_validation()
        self.check_consistency()
        self.generate_audit_report()
        
        # Save reports
        timestamp = self.save_reports()
        
        # Generate cleaned sample
        df_cleaned = self.clean_data()
        
        # Save cleaned sample
        if self.filepath.endswith('.csv'):
            df_cleaned.to_csv(f'cleaned_sample_{timestamp}.csv', index=False)
        else:
            df_cleaned.to_excel(f'cleaned_sample_{timestamp}.xlsx', index=False)
        print(f"✓ Cleaned sample saved: cleaned_sample_{timestamp}.{'csv' if self.filepath.endswith('.csv') else 'xlsx'}")
        
        print("\n" + "="*60)
        print("AUDIT COMPLETE")
        print("="*60)
        
        return True


def main():
    """Main execution function"""
    print("Data Quality Audit Tool")
    print("Task 24: Data Quality Audit for Internship\n")
    
    # Check if file path provided as command-line argument
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        print(f"Using dataset from command line: {filepath}\n")
    else:
        # Ask for dataset path
        filepath = input("Enter path to dataset (CSV or Excel): ").strip()
    
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        return
    
    # Run audit
    auditor = DataQualityAuditor(filepath)
    auditor.run_full_audit()


if __name__ == "__main__":
    main()
