import pandas as pd
from config import get_engine
import os

def read_data_from_db(table_name):
    """
    Đọc dữ liệu từ bảng trong SQL Server.
    """
    engine = get_engine()
    query = f"SELECT * FROM {table_name}"
    data = pd.read_sql(query, con=engine)
    return data

def analyze_data(df, table_name):
    """
    Phân tích dữ liệu và trả về kết quả.
    """
    analysis_result = {'table_name': table_name}
    
    # Các phân tích cho bảng train
    if table_name == 'cleaned_train':
        # Tính tổng số lượng sales
        if 'sales' in df.columns:
            total_sales = df['sales'].sum()
            analysis_result['total_sales'] = total_sales
        
        # Tính số lượng giao dịch trung bình
        if 'transactions' in df.columns:
            avg_transactions = df['transactions'].mean()
            analysis_result['avg_transactions'] = avg_transactions
    
    # Các phân tích cho bảng transactions
    if table_name == 'cleaned_transactions':
        # Tính tổng số lượng giao dịch
        if 'transactions' in df.columns:
            total_transactions = df['transactions'].sum()
            analysis_result['total_transactions'] = total_transactions

    # Các phân tích cho bảng oil
    if table_name == 'cleaned_oil':
        # Tính giá trị trung bình của giá dầu
        if 'dcoilwtico' in df.columns:
            avg_oil_price = df['dcoilwtico'].mean()
            analysis_result['avg_oil_price'] = avg_oil_price

    # Các phân tích cho bảng holidays_events
    if table_name == 'cleaned_holidays_events':
        # Tính số lượng từng loại ngày lễ
        if 'type' in df.columns:
            holiday_types = df['type'].value_counts().to_dict()
            analysis_result['holiday_types'] = holiday_types

    # Các phân tích cho bảng stores
    if table_name == 'cleaned_stores':
        # Đếm số lượng cửa hàng theo từng thành phố
        if 'city' in df.columns:
            store_counts_by_city = df['city'].value_counts().to_dict()
            analysis_result['store_counts_by_city'] = store_counts_by_city

        # Đếm số lượng cửa hàng theo từng loại (type)
        if 'type' in df.columns:
            store_counts_by_type = df['type'].value_counts().to_dict()
            analysis_result['store_counts_by_type'] = store_counts_by_type

    # Các phân tích cho bảng test
    if table_name == 'cleaned_test':
        # Đếm số lượng bản ghi theo từng ngày (date)
        if 'date' in df.columns:
            record_counts_by_date = df['date'].value_counts().to_dict()
            analysis_result['record_counts_by_date'] = record_counts_by_date

    return analysis_result

def save_analysis_result(result):
    """
    Lưu kết quả phân tích vào tệp analysis_report.txt.
    """
    results_dir = 'results'
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    file_path = os.path.join(results_dir, "analysis_report.txt")
    with open(file_path, 'a') as f:
        f.write(f"Analysis result for {result['table_name']}:\n")
        for key, value in result.items():
            if key != 'table_name':
                f.write(f"  {key}: {value}\n")
        f.write("\n")
    print(f"Analysis result saved to {file_path}")

def main():
    # Đọc dữ liệu từ các bảng đã làm sạch
    tables = ['cleaned_holidays_events', 'cleaned_oil', 'cleaned_stores', 'cleaned_transactions', 'cleaned_train', 'cleaned_test']
    for table in tables:
        print(f"Analyzing {table} table...")
        df = read_data_from_db(table)
        analysis_result = analyze_data(df, table)
        print(f"Analysis result for {table}: {analysis_result}")
        save_analysis_result(analysis_result)

if __name__ == "__main__":
    main()
