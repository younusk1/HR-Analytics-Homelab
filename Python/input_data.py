import os
import logging
from pathlib import Path
from datetime import datetime

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Project root
project_root = Path(__file__).resolve().parent.parent

# Output directory
output_dir = project_root / "Data" / "Processed"
output_dir.mkdir(parents=True, exist_ok=True)

# PostgreSQL connection - set environment variables
os.environ.setdefault("DB_USER", "admin")
os.environ.setdefault("DB_PASSWORD", "password")
os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5432")
os.environ.setdefault("DB_NAME", "hr_analytics")


def get_db_engine():
    """Create and return SQLAlchemy engine for PostgreSQL."""
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    
    connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    return create_engine(connection_string)


def process_csv(csv_filename, table_name):
    """
    Process a CSV file and load it into PostgreSQL.
    
    Args:
        csv_filename (str): Name of the CSV file in Data/Raw/
        table_name (str): Target table name in PostgreSQL
    
    Returns:
        dict: Status dict with 'success', 'records_count', and 'output_file'
    """
    try:
        # Input file path
        input_file = project_root / "Data" / "Raw" / csv_filename
        
        # Validate input file exists
        if not input_file.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        logger.info(f"Loading data from: {input_file}")
        
        # Load data
        df = pd.read_csv(input_file)
        
        if df.empty:
            raise ValueError("Input file is empty")
        
        logger.info(f"Loaded {len(df)} records from {csv_filename}")
        
        # Data validation - check for null values
        null_count = df.isnull().sum().sum()
        if null_count > 0:
            logger.warning(f"Found {null_count} null values in {csv_filename}")
        
        # Transform: lowercase and strip column names
        df.columns = df.columns.str.lower().str.strip()
        
        # Generate timestamp for processed file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = output_dir / f"{table_name}_processed_{timestamp}.csv"
        
        # Save processed file
        df.to_csv(output_file, index=False)
        logger.info(f"Processed file saved to: {output_file}")
        
        # Load into database
        engine = get_db_engine()
        logger.info(f"Importing {len(df)} records into {table_name} table...")
        
        df.to_sql(
            table_name,
            engine,
            if_exists="append",  # Use 'append' for incremental loads, 'replace' to truncate
            index=False
        )
        
        logger.info(f"Successfully imported {len(df)} records into {table_name} table.")
        
        return {
            "success": True,
            "records_count": len(df),
            "output_file": str(output_file),
            "table_name": table_name
        }
        
    except FileNotFoundError as e:
        logger.error(f"File error processing {csv_filename}: {e}")
        return {"success": False, "error": str(e), "csv_file": csv_filename}
    except ValueError as e:
        logger.error(f"Data validation error in {csv_filename}: {e}")
        return {"success": False, "error": str(e), "csv_file": csv_filename}
    except pd.errors.EmptyDataError as e:
        logger.error(f"CSV parsing error in {csv_filename}: {e}")
        return {"success": False, "error": str(e), "csv_file": csv_filename}
    except SQLAlchemyError as e:
        logger.error(f"Database error loading {csv_filename} into {table_name}: {e}")
        return {"success": False, "error": str(e), "csv_file": csv_filename, "table_name": table_name}
    except Exception as e:
        logger.error(f"Unexpected error processing {csv_filename}: {e}")
        return {"success": False, "error": str(e), "csv_file": csv_filename}


if __name__ == "__main__":
    # Example: process single file
    process_csv("employees.csv", "employees")