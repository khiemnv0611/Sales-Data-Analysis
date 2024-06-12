import pandas as pd
import config

def read_data_from_db(table_name):
    """
    Đọc dữ liệu từ bảng trong SQL Server.
    """
    engine = config.get_engine()
    query = f"SELECT * FROM {table_name}"
    data = pd.read_sql(query, con=engine)
    return data

def clean_data(df, table_name):
    """
    Làm sạch và chuẩn hóa dữ liệu.
    """
    # Bước 1: Loại bỏ các hàng có giá trị thiếu
    df.dropna(inplace=True)

    # Bước 2: Chuyển đổi định dạng ngày tháng nếu có cột date
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])

    # Bước 3: Loại bỏ các bản ghi không hợp lệ nếu có cột sales hoặc onpromotion
    if 'sales' in df.columns:
        df = df[df['sales'] >= 0]
    if 'onpromotion' in df.columns:
        df = df[df['onpromotion'] >= 0]

    # Bước 4: Chuẩn hóa tên cột
    df.columns = df.columns.str.lower().str.replace(' ', '_')

    return df

def save_cleaned_data_to_db(df, table_name):
    """
    Lưu dữ liệu đã làm sạch vào bảng trong SQL Server.
    """
    engine = config.get_engine()
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    print(f"Cleaned data saved to {table_name} table.")

def main():
    """
    Đọc dữ liệu từ các bảng, làm sạch và lưu lại vào bảng mới.
    """
    tables = ['holidays_events', 'oil', 'stores', 'transactions', 'train', 'test']
    for table in tables:
        print(f"Processing {table} table...")
        df = read_data_from_db(table)
        cleaned_df = clean_data(df, table)
        save_cleaned_data_to_db(cleaned_df, f"cleaned_{table}")

if __name__ == "__main__":
    main()
