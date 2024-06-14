import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib
import os
import config

def load_cleaned_data():
    """
    Tải dữ liệu đã được làm sạch từ bảng 'cleaned_train' trong SQL Server.
    """
    engine = config.get_engine()
    query = "SELECT * FROM cleaned_train"
    data = pd.read_sql(query, con=engine)
    return data

def preprocess_data(data):
    """
    Tiền xử lý dữ liệu, bao gồm tách các biến đầu vào (X) và đầu ra (y).
    """
    # Loại bỏ các cột không cần thiết và chuyển đổi các biến phân loại thành số
    data = pd.get_dummies(data, columns=['family'])
    # Tách các cột đầu vào (X) và cột đầu ra (y)
    X = data.drop(['sales', 'date', 'id'], axis=1)
    y = data['sales']
    return X, y

def train_model(X, y):
    """
    Huấn luyện mô hình học máy trên dữ liệu đầu vào (X) và đầu ra (y).
    """
    # Chia dữ liệu thành tập huấn luyện và tập kiểm tra với tỷ lệ 80/20
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Khởi tạo và huấn luyện mô hình Linear Regression
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # In ra chỉ số đánh giá mô hình R^2 score trên tập kiểm tra
    # R² score: 1 là hoàn hảo, 0 là không giải thích được gì, <0 là rất tệ
    print(f"Model trained with R^2 score: {model.score(X_test, y_test)}") 
    return model

def save_model(model):
    """
    Lưu mô hình đã huấn luyện vào tệp 'model.pkl'.
    """
    results_dir = 'results'
        
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)    
    file_path = os.path.join(results_dir, "model.pkl")
    
    # Lưu mô hình vào tệp
    joblib.dump(model, file_path)
    print(f"Model saved to {file_path}")

def main():
    """
    Hàm chính để tải dữ liệu, tiền xử lý, huấn luyện và lưu mô hình.
    """
    data = load_cleaned_data()    
    X, y = preprocess_data(data)
    model = train_model(X, y)
    save_model(model)

if __name__ == "__main__":
    main()
