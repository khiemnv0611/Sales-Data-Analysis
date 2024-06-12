import pyodbc
from sqlalchemy import create_engine

# Thông tin kết nối đến SQL Server
server_name = 'KHIEMNV'
database_name = 'sales_data'
# username = 'your_username'
# password = 'your_password'

connection_string_master = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server_name};DATABASE=master;Trusted_Connection=yes;'
connection_string_db = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server_name};DATABASE={database_name};Trusted_Connection=yes;'
# connection_string_master = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server_name};DATABASE=master;UID={username};PWD={password};'
# connection_string_db = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server_name};DATABASE={database_name};UID={username};PWD={password};'

def get_engine(database='sales_data'):
    """
    Trả về đối tượng engine của SQLAlchemy để kết nối tới SQL Server.
    """
    if database == 'master':
        return create_engine(f'mssql+pyodbc://@{server_name}/master?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes')
        # return create_engine(f'mssql+pyodbc://{username}:{password}@{server_name}/master?driver=ODBC+Driver+17+for+SQL+Server')
    else:
        return create_engine(f'mssql+pyodbc://@{server_name}/{database}?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes')
        # return create_engine(f'mssql+pyodbc://{username}:{password}@{server_name}/{database}?driver=ODBC+Driver+17+for+SQL+Server')

def get_connection_string(database='sales_data'):
    """
    Trả về chuỗi kết nối cho pyodbc.
    """
    if database == 'master':
        return connection_string_master
    else:
        return connection_string_db
