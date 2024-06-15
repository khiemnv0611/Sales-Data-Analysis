import pandas as pd
import config
import matplotlib.pyplot as plt
import seaborn as sns
import os

def read_data_from_db(table_name):
    """
    Đọc dữ liệu từ bảng trong SQL Server.
    """
    engine = config.get_engine()
    query = f"SELECT * FROM {table_name}"
    data = pd.read_sql(query, con=engine)
    return data

def analyze_data(df, table_name):
    """
    Phân tích dữ liệu và trực quan hóa dữ liệu.
    """
    analysis_result = {"table_name": table_name}
    
    # Chuyển đổi cột 'date' sang kiểu datetime nếu cột này tồn tại trong DataFrame
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])  # Chuyển đổi cột 'date' về định dạng datetime

    # Phân tích bảng cleaned_holidays_events
    if table_name == 'cleaned_holidays_events':
        # Đếm số lượng từng loại ngày nghỉ và lưu vào kết quả phân tích
        holiday_types = df['type'].value_counts().to_dict()  # Đếm số lượng các loại ngày nghỉ và chuyển thành từ điển
        analysis_result['holiday_types'] = holiday_types  # Lưu số lượng các loại ngày nghỉ vào analysis_result
        
        # Vẽ biểu đồ phân phối các loại ngày nghỉ
        plt.figure(figsize=(12, 6))  # Tạo khung vẽ với kích thước 12x6 inch
        sns.countplot(data=df, x='type')  # Vẽ biểu đồ cột đếm số lượng các loại ngày nghỉ
        plt.title('Holiday Types Distribution')  # Đặt tiêu đề cho biểu đồ
        plt.xlabel('Holiday Type')  # Đặt nhãn cho trục x là 'Holiday Type'
        plt.ylabel('Count')  # Đặt nhãn cho trục y là 'Count'
        plt.grid(True)  # Bật lưới để dễ nhìn biểu đồ hơn
        plt.savefig(f'results/{table_name}_holiday_types.png')  # Lưu biểu đồ dưới dạng tệp PNG trong thư mục 'results'
        plt.close()  # Đóng biểu đồ để giải phóng bộ nhớ
        
    # Phân tích bảng cleaned_oil
    if table_name == 'cleaned_oil':
        # Tính giá trung bình của dầu và lưu vào kết quả phân tích
        avg_oil_price = df['dcoilwtico'].mean()  # Tính giá dầu trung bình
        analysis_result['avg_oil_price'] = avg_oil_price  # Lưu giá dầu trung bình vào analysis_result
        
        # Vẽ biểu đồ giá dầu hàng ngày theo thời gian
        plt.figure(figsize=(12, 6))  # Tạo khung vẽ với kích thước 12x6 inch
        sns.lineplot(data=df, x='date', y='dcoilwtico')  # Vẽ biểu đồ đường với trục x là 'date' và trục y là 'dcoilwtico'
        plt.title('Daily Oil Price Over Time')  # Đặt tiêu đề cho biểu đồ
        plt.xlabel('Date')  # Đặt nhãn cho trục x là 'Date'
        plt.ylabel('Oil Price')  # Đặt nhãn cho trục y là 'Oil Price'
        plt.grid(True)  # Bật lưới để dễ nhìn biểu đồ hơn
        plt.savefig(f'results/{table_name}_oil_price.png')  # Lưu biểu đồ dưới dạng tệp PNG trong thư mục 'results'
        plt.close()  # Đóng biểu đồ để giải phóng bộ nhớ
        
    # Phân tích bảng cleaned_stores
    if table_name == 'cleaned_stores':
        # Đếm số lượng cửa hàng theo thành phố và lưu vào kết quả phân tích
        store_counts_by_city = df['city'].value_counts().to_dict()  # Đếm số lượng cửa hàng theo thành phố và chuyển thành từ điển
        analysis_result['store_counts_by_city'] = store_counts_by_city  # Lưu số lượng cửa hàng theo thành phố vào analysis_result
        
        # Vẽ biểu đồ số lượng cửa hàng theo thành phố
        plt.figure(figsize=(12, 6))  # Tạo khung vẽ với kích thước 12x6 inch
        sns.countplot(data=df, x='city')  # Vẽ biểu đồ cột đếm số lượng cửa hàng theo thành phố
        plt.title('Store Counts by City')  # Đặt tiêu đề cho biểu đồ
        plt.xlabel('City')  # Đặt nhãn cho trục x là 'City'
        plt.ylabel('Count')  # Đặt nhãn cho trục y là 'Count'
        plt.grid(True)  # Bật lưới để dễ nhìn biểu đồ hơn
        plt.savefig(f'results/{table_name}_store_counts_by_city.png')  # Lưu biểu đồ dưới dạng tệp PNG trong thư mục 'results'
        plt.close()  # Đóng biểu đồ để giải phóng bộ nhớ
        
    # Phân tích bảng cleaned_transactions
    if table_name == 'cleaned_transactions':
        # Tính tổng số giao dịch hàng ngày và lưu vào kết quả phân tích
        daily_transactions = df.groupby('date')['transactions'].sum().reset_index()  # Nhóm dữ liệu theo ngày và tính tổng số lượng giao dịch hàng ngày
        analysis_result['total_transactions'] = daily_transactions['transactions'].sum()  # Tính tổng số lượng giao dịch và lưu vào analysis_result
        
        # Vẽ biểu đồ số giao dịch hàng ngày theo thời gian
        plt.figure(figsize=(12, 6))  # Tạo khung vẽ với kích thước 12x6 inch
        sns.lineplot(data=daily_transactions, x='date', y='transactions')  # Vẽ biểu đồ đường với trục x là 'date' và trục y là 'transactions'
        plt.title('Daily Transactions Over Time')  # Đặt tiêu đề cho biểu đồ
        plt.xlabel('Date')  # Đặt nhãn cho trục x là 'Date'
        plt.ylabel('Number of Transactions')  # Đặt nhãn cho trục y là 'Number of Transactions'
        plt.grid(True)  # Bật lưới để dễ nhìn biểu đồ hơn
        plt.savefig(f'results/{table_name}_daily_transactions.png')  # Lưu biểu đồ dưới dạng tệp PNG trong thư mục 'results'
        plt.close()  # Đóng biểu đồ để giải phóng bộ nhớ
        
    # Phân tích bảng cleaned_train
    if table_name == 'cleaned_train':
        # Tính tổng số doanh thu và lưu vào kết quả phân tích
        total_sales = df['sales'].sum()  # Tính tổng doanh thu
        analysis_result['total_sales'] = total_sales  # Lưu tổng doanh thu vào analysis_result

        # Vẽ biểu đồ tổng doanh thu theo thời gian
        plt.figure(figsize=(12, 6))  # Tạo khung vẽ với kích thước 12x6 inch
        sns.lineplot(data=df, x='date', y='sales')  # Vẽ biểu đồ đường với trục x là 'date' và trục y là 'sales'
        plt.title('Total Sales Over Time')  # Đặt tiêu đề cho biểu đồ
        plt.xlabel('Date')  # Đặt nhãn cho trục x là 'Date'
        plt.ylabel('Sales')  # Đặt nhãn cho trục y là 'Sales'
        plt.grid(True)  # Bật lưới để dễ nhìn biểu đồ hơn
        plt.savefig(f'results/{table_name}_total_sales.png')  # Lưu biểu đồ dưới dạng tệp PNG trong thư mục 'results'
        plt.close()  # Đóng biểu đồ để giải phóng bộ nhớ
        
    # Phân tích bảng cleaned_test
    if table_name == 'cleaned_test':
        # Đếm số lượng bản ghi theo ngày và lưu vào kết quả phân tích
        record_counts_by_date = df['date'].value_counts().to_dict()  # Đếm số lượng bản ghi theo ngày và chuyển thành từ điển
        analysis_result['record_counts_by_date'] = record_counts_by_date  # Lưu số lượng bản ghi theo ngày vào analysis_result
        
        # Vẽ biểu đồ số lượng bản ghi theo ngày
        plt.figure(figsize=(12, 6))  # Tạo khung vẽ với kích thước 12x6 inch
        sns.countplot(data=df, x='date')  # Vẽ biểu đồ cột đếm số lượng bản ghi theo ngày
        plt.title('Record Counts by Date')  # Đặt tiêu đề cho biểu đồ
        plt.xlabel('Date')  # Đặt nhãn cho trục x là 'Date'
        plt.ylabel('Count')  # Đặt nhãn cho trục y là 'Count'
        plt.grid(True)  # Bật lưới để dễ nhìn biểu đồ hơn
        plt.savefig(f'results/{table_name}_record_counts_by_date.png')  # Lưu biểu đồ dưới dạng tệp PNG trong thư mục 'results'
        plt.close()  # Đóng biểu đồ để giải phóng bộ nhớ
        
    return analysis_result


def save_analysis_result(result, mode='w'):
    """
    Lưu kết quả phân tích vào tệp analysis_report.txt.
    """
    results_dir = 'results'
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    file_path = os.path.join(results_dir, "analysis_report.txt")
    
    with open(file_path, mode) as f:
        f.write(f"Analysis result for {result['table_name']}:\n")
        for key, value in result.items():
            if key != 'table_name':
                f.write(f"  {key}: {value}\n")
        f.write("\n")
    print(f"Analysis result saved to {file_path}")

def main():
    """
    Đọc dữ liệu từ các bảng, phân tích và lưu lại kết quả.
    """
    tables = ['cleaned_holidays_events', 'cleaned_oil', 'cleaned_stores', 'cleaned_transactions', 'cleaned_train', 'cleaned_test']
    
    mode = 'w'  # Bắt đầu với chế độ ghi đè
    for table in tables:
        print(f"Analyzing {table} table...")
        df = read_data_from_db(table)
        analysis_result = analyze_data(df, table)
        print(f"Analysis result for {table}: {analysis_result}")
        save_analysis_result(analysis_result, mode)
        mode = 'a'  # Chuyển sang chế độ thêm sau lần ghi đầu tiên

if __name__ == "__main__":
    main()