import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle
import config

def load_cleaned_data(table_name='cleaned_train'):
    """
    Tải dữ liệu đã làm sạch từ SQL Server.
    """
    engine = config.get_engine()
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, con=engine)
    return df

def preprocess_data(df):
    """
    Tiền xử lý dữ liệu trước khi huấn luyện mô hình.
    """
    # Chọn các cột đầu vào (features) và cột mục tiêu (target)
    X = df.drop(columns=['sales', 'date', 'id'])  # Đầu vào
    y = df['sales']  # Đầu ra
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_model(X_train, y_train):
    """
    Huấn luyện mô hình và lưu trữ mô hình đã huấn luyện vào tệp model.pkl.
    """
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Lưu trữ mô hình đã huấn luyện vào tệp
    with open('results/model.pkl', 'wb') as file:
        pickle.dump(model, file)
    print("Model trained and saved to 'results/model.pkl'")

def main():
    # Tải dữ liệu đã làm sạch
    df = load_cleaned_data()

    # Tiền xử lý dữ liệu
    X_train, X_test, y_train, y_test = preprocess_data(df)

    # Huấn luyện mô hình
    train_model(X_train, y_train)

if __name__ == "__main__":
    main()
