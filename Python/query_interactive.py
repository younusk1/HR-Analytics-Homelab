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


def get_all_tables():
    """Get list of all tables in the database."""
    try:
        engine = get_db_engine()
        inspector = inspect(engine)
        return inspector.get_table_names()
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        return []


def list_tables_with_counts():
    """List all tables and their record counts."""
    try:
        engine = get_db_engine()
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        if not tables:
            print("\n❌ No tables found in the database\n")
            return
        
        print(f"\n📊 Tables in database ({len(tables)} total):\n")
        
        with engine.connect() as connection:
            for i, table in enumerate(tables, 1):
                result = connection.execute(text(f"SELECT COUNT(*) FROM {table}"))
                row_count = result.scalar()
                print(f"  {i}. {table:<25} ({row_count} records)")
        
        print()
        
    except SQLAlchemyError as e:
        print(f"\n❌ Database error: {e}\n")


def view_table_data(table_name, limit=5):
    """Display data from a specific table."""
    try:
        engine = get_db_engine()
        
        print(f"\n{'='*80}")
        print(f"📋 Data from '{table_name}' (first {limit} rows)")
        print(f"{'='*80}\n")
        
        df = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT {limit}", engine)
        
        if df.empty:
            print("❌ No data in this table\n")
        else:
            print(df.to_string(index=False))
            print(f"\nColumns ({len(df.columns)}): {', '.join(df.columns)}")
            print(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns\n")
        
    except SQLAlchemyError as e:
        print(f"\n❌ Database error: {e}\n")


def get_table_schema(table_name):
    """Display schema information for a table."""
    try:
        engine = get_db_engine()
        inspector = inspect(engine)
        
        columns = inspector.get_columns(table_name)
        
        print(f"\n{'='*80}")
        print(f"🔍 Schema for '{table_name}'")
        print(f"{'='*80}\n")
        
        for i, col in enumerate(columns, 1):
            nullable = "✓ NULL" if col['nullable'] else "✗ NOT NULL"
            print(f"  {i}. {col['name']:<25} {str(col['type']):<20} {nullable}")
        
        print()
        
    except SQLAlchemyError as e:
        print(f"\n❌ Database error: {e}\n")


def run_custom_query(query):
    """Execute a custom SQL query."""
    try:
        engine = get_db_engine()
        
        print(f"\n{'='*80}")
        print(f"🔧 Query Result")
        print(f"{'='*80}\n")
        
        df = pd.read_sql_query(query, engine)
        
        if df.empty:
            print("✓ Query executed successfully but returned no results\n")
        else:
            print(df.to_string(index=False))
            print(f"\nResult: {df.shape[0]} rows × {df.shape[1]} columns\n")
        
    except Exception as e:
        print(f"\n❌ Error executing query: {e}\n")


def display_menu():
    """Display the main menu."""
    print("\n" + "="*80)
    print("📊 HR Analytics Database Query Tool")
    print("="*80)
    print("\nOptions:")
    print("  1. List all tables with record counts")
    print("  2. View table schema")
    print("  3. View table data")
    print("  4. Run custom SQL query")
    print("  5. Exit")
    print()


def interactive_prompt():
    """Run interactive prompt for database queries."""
    print("\n✓ Connected to PostgreSQL database successfully!")
    
    while True:
        display_menu()
        choice = input("Choose an option (1-5): ").strip()
        
        if choice == "1":
            list_tables_with_counts()
        
        elif choice == "2":
            tables = get_all_tables()
            if tables:
                print("\nAvailable tables:")
                for i, table in enumerate(tables, 1):
                    print(f"  {i}. {table}")
                
                table_choice = input("\nEnter table name (or number): ").strip()
                
                # Handle numeric input
                if table_choice.isdigit() and 1 <= int(table_choice) <= len(tables):
                    table_name = tables[int(table_choice) - 1]
                else:
                    table_name = table_choice
                
                if table_name in tables:
                    get_table_schema(table_name)
                else:
                    print(f"\n❌ Table '{table_name}' not found\n")
        
        elif choice == "3":
            tables = get_all_tables()
            if tables:
                print("\nAvailable tables:")
                for i, table in enumerate(tables, 1):
                    print(f"  {i}. {table}")
                
                table_choice = input("\nEnter table name (or number): ").strip()
                
                # Handle numeric input
                if table_choice.isdigit() and 1 <= int(table_choice) <= len(tables):
                    table_name = tables[int(table_choice) - 1]
                else:
                    table_name = table_choice
                
                if table_name in tables:
                    try:
                        limit = input("Number of rows to display (default 5): ").strip()
                        limit = int(limit) if limit.isdigit() else 5
                        view_table_data(table_name, limit=limit)
                    except ValueError:
                        print("\n❌ Invalid number entered\n")
                else:
                    print(f"\n❌ Table '{table_name}' not found\n")
        
        elif choice == "4":
            print("\nEnter your SQL query (e.g., SELECT * FROM employees WHERE salary > 50000)")
            query = input("SQL Query: ").strip()
            
            if query:
                run_custom_query(query)
            else:
                print("\n❌ No query entered\n")
        
        elif choice == "5":
            print("\n👋 Goodbye!\n")
            break
        
        else:
            print("\n❌ Invalid option. Please choose 1-5.\n")


if __name__ == "__main__":
    try:
        interactive_prompt()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!\n")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}\n")
