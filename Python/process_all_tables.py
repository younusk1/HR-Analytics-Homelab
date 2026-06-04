import logging
from input_data import process_csv

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define table configurations
tables = [
    {"csv": "employees.csv", "table": "employees"},
    {"csv": "managers.csv", "table": "managers"},
    {"csv": "performance_reviews.csv", "table": "performance_reviews"},
    {"csv": "training_records.csv", "table": "training_records"},
    {"csv": "turnover.csv", "table": "turnover"},
]


def process_all_tables():
    """Process all CSV files and load them into corresponding PostgreSQL tables."""
    logger.info(f"Starting ETL process for {len(tables)} tables...")
    
    results = []
    success_count = 0
    
    for config in tables:
        logger.info(f"\n--- Processing {config['csv']} ---")
        result = process_csv(config["csv"], config["table"])
        results.append(result)
        
        if result["success"]:
            success_count += 1
    
    # Summary
    logger.info(f"\n{'='*50}")
    logger.info(f"ETL SUMMARY: {success_count}/{len(tables)} tables processed successfully")
    logger.info(f"{'='*50}")
    
    for result in results:
        if result["success"]:
            logger.info(f"✓ {result['table_name']}: {result['records_count']} records imported")
        else:
            logger.error(f"✗ {result['csv_file']}: {result['error']}")
    
    return results


if __name__ == "__main__":
    process_all_tables()
