
# Sales Data Analysis

This project involves loading, cleaning, analyzing, and visualizing sales data from a SQL Server database. It also includes training a machine learning model to predict sales and saving the predictions to a CSV file.

## Getting Started

### Prerequisites

- Python 3.x

### Installing

1. **Install Required Libraries**: Install the required libraries using `requirements.txt`.
```bash
pip install -r requirements.txt
```

### Setting Up

1. **Clear Results Directory**: Ensure the `results` directory is empty to avoid any file overwrite issues.
2. **Configure SQL Server**: Update the `config.py` file to match your SQL Server connection details.

### Running the Scripts

**Step-by-Step Execution:**

1. **01_load_data.py**: This script creates the database and loads the data from CSV files.
    ```bash
    python scripts/01_load_data.py
    ```

2. **02_clean_data.py**: This script reads data from the database, cleans it, and saves the cleaned data back to the database.
    ```bash
    python scripts/02_clean_data.py
    ```

3. **03_data_analysis.py**: This script reads the cleaned data, analyzes it, and saves the analysis results and visualizations.
    ```bash
    python scripts/03_data_analysis.py
    ```

4. **04_model_training.py**: This script trains a machine learning model using the cleaned data and saves the model.
    ```bash
    python scripts/04_model_training.py
    ```

5. **05_visualization.py**: This script uses the trained model to make predictions, saves the predictions, and visualizes the predicted sales.
    ```bash
    python scripts/05_visualization.py
    ```

### Note

Before running the scripts, ensure that your SQL Server is running and accessible with the connection details provided in the `config.py` file.
