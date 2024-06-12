import pandas as pd
import config

# Đường dẫn đến các tệp CSV
data_files = {
    'holidays_events': './data/holidays_events.csv',
    'oil': './data/oil.csv',
    'stores': './data/stores.csv',
    'transactions': './data/transactions.csv',
    'train': './data/train.csv',
    'test': './data/test.csv'
}

def create_database():
    """
    Tạo database nếu chưa tồn tại.
    """
    with config.pyodbc.connect(config.get_connection_string('master'), autocommit=True) as conn:
        cursor = conn.cursor()
        cursor.execute(f"IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'{config.database_name}') CREATE DATABASE [{config.database_name}]")
        cursor.close()
    print(f"Database '{config.database_name}' is ready.")

def load_data(file_path, table_name):
    """
    Hàm để tải dữ liệu từ CSV vào SQL Server.
    """
    engine = config.get_engine()
    data = pd.read_csv(file_path)
    data.to_sql(table_name, con=engine, if_exists='replace', index=False)
    print(f'Data from {file_path} loaded into {table_name} table.')

def main():
    # Tạo database nếu chưa tồn tại
    create_database()
    
    # Lặp qua các tệp dữ liệu và tải chúng vào SQL Server
    for table_name, file_path in data_files.items():
        load_data(file_path, table_name)

if __name__ == "__main__":
    main()
