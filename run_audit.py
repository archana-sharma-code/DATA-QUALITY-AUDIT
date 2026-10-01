"""
Quick script to run audit on the sample dataset without user input
"""

from data_quality_audit import DataQualityAuditor

# Run audit on sample dataset
auditor = DataQualityAuditor('sample_superstore.csv')
auditor.run_full_audit()
