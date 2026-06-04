import os
import logging
import pandas as pd
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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


def list_tables():
    """List all tables in the database and their record counts."""
    try:
        engine = get_db_engine()
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        if not tables:
            logger.warning("No tables found in the database")
            return
        
        logger.info(f"Found {len(tables)} tables in database:\n")
        
        # Get row count for each table
        with engine.connect() as connection:
            for table in tables:
                result = connection.execute(text(f"SELECT COUNT(*) FROM {table}"))
                row_count = result.scalar()
                logger.info(f"  • {table}: {row_count} records")
        
        return tables
        
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        return None


def view_table_data(table_name, limit=5):
    """Display sample data from a specific table."""
    try:
        engine = get_db_engine()
        
        logger.info(f"\n{'='*60}")
        logger.info(f"Sample data from '{table_name}' table (first {limit} rows):")
        logger.info(f"{'='*60}\n")
        
        df = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT {limit}", engine)
        
        if df.empty:
            logger.info("No data in this table")
        else:
            logger.info(df.to_string())
            logger.info(f"\nColumns: {list(df.columns)}")
            logger.info(f"Data types:\n{df.dtypes}")
        
        return df
        
    except SQLAlchemyError as e:
        logger.error(f"Database error querying {table_name}: {e}")
        return None


def get_table_schema(table_name):
    """Display detailed schema information for a table."""
    try:
        engine = get_db_engine()
        inspector = inspect(engine)
        
        columns = inspector.get_columns(table_name)
        
        logger.info(f"\n{'='*60}")
        logger.info(f"Schema for '{table_name}' table:")
        logger.info(f"{'='*60}\n")
        
        for col in columns:
            nullable = "NULL" if col['nullable'] else "NOT NULL"
            logger.info(f"  • {col['name']:<20} {str(col['type']):<15} {nullable}")
        
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")


if __name__ == "__main__":
    logger.info("Connecting to PostgreSQL database...\n")
    
    # List all tables and record counts
    tables = list_tables()
    
    if tables:
        # Show schema and sample data for each table
        for table in tables:
            get_table_schema(table)
            view_table_data(table, limit=3)
            print()  # Add spacing between tables
