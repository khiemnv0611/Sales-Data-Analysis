import pandas as pd
import config
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns

def load_model(model_path='results/model.pkl', feature_names_path='results/feature_names.pkl'):
    """
    Tải mô hình đã huấn luyện từ tệp 'model.pkl' và tên các cột từ 'feature_names.pkl'.
    """
    model = joblib.load(model_path)
    feature_names = joblib.load(feature_names_path)
    print(f"Model loaded from {model_path}")
    return model, feature_names

def load_cleaned_data(table_name='cleaned_test'):
    """
    Tải dữ liệu đã được làm sạch từ bảng 'cleaned_test' trong SQL Server.
    """
    engine = config.get_engine()
    query = f"SELECT * FROM {table_name}"
    data = pd.read_sql(query, con=engine)
    return data

def preprocess_data(data, feature_names):
    """
    Tiền xử lý dữ liệu để phù hợp với mô hình đã huấn luyện.
    """
    X = data.drop(['id', 'date'], axis=1)
    
    # One-Hot Encoding cho các cột dạng chuỗi
    X = pd.get_dummies(X, columns=['family'])
    
    # Đảm bảo rằng các cột của X phù hợp với các cột trong feature_names
    for col in feature_names:
        if col not in X.columns:
            X[col] = 0
    X = X[feature_names]
    
    return X

def make_predictions(model, data, feature_names):
    """
    Dự đoán dựa trên mô hình đã huấn luyện và dữ liệu đầu vào.
    """
    X = preprocess_data(data, feature_names) # Tiền xử lý dữ liệu
    predictions = model.predict(X) # Dự đoán
    return predictions

def save_predictions(predictions, file_path='results/predictions.csv'):
    """
    Lưu kết quả dự đoán vào tệp CSV.
    """
    results_dir = 'results'
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    df_predictions = pd.DataFrame(predictions, columns=['predictions'])
    df_predictions.to_csv(file_path, index=False)
    print(f"Predictions saved to {file_path}")

def plot_predictions(data, predictions):
    """
    Trực quan hóa dữ liệu và dự đoán.
    """
    plt.figure(figsize=(12, 6))  # Tạo khung vẽ với kích thước 12x6 inch
    sns.lineplot(x=data['date'], y=predictions, label='Predicted Sales')  # Vẽ biểu đồ đường cho dự đoán
    plt.title('Predicted Sales Over Time')  # Tiêu đề biểu đồ
    plt.xlabel('Date')  # Nhãn trục X
    plt.ylabel('Sales')  # Nhãn trục Y
    plt.legend()  # Hiển thị chú thích
    plt.grid(True)  # Hiển thị lưới
    plt.savefig('results/predicted_sales.png')  # Lưu biểu đồ vào tệp
    plt.close()  # Đóng khung vẽ
    print("Plot saved to results/predicted_sales.png")

def main():
    """
    Tải mô hình, dữ liệu, thực hiện dự đoán và lưu kết quả, trực quan hóa dữ liệu.
    """
    model, feature_names = load_model()
    data = load_cleaned_data()
    predictions = make_predictions(model, data, feature_names)
    save_predictions(predictions)
    plot_predictions(data, predictions)

if __name__ == "__main__":
    main()
