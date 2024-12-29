---

# `for_lab_use` Directory

This directory contains files and scripts for predicting temperature and rod pressure using machine learning models (XGBoost and Random Forest). The models are trained on simulation data and can predict outcomes based on input parameters.

---

## File Descriptions

### 1. **Models**
- `best_xgboost_model_temperature.pkl`: Pre-trained XGBoost model for predicting temperature.
- `best_xgboost_model_rodpressure.pkl`: Pre-trained XGBoost model for predicting rod pressure.
- `random_forest_model_temperature.joblib`: Pre-trained Random Forest model for predicting temperature.
- `random_forest_model_pressure.joblib`: Pre-trained Random Forest model for predicting rod pressure.

### 2. **Scalers**
- `scaler_temperature.pkl`: Scaler for preprocessing input data for the temperature XGBoost model.
- `scaler_rodpressure.pkl`: Scaler for preprocessing input data for the rod pressure XGBoost model.

### 3. **Scripts**
- `predict_xgboost.py`: Python script to predict temperature and rod pressure using the pre-trained XGBoost models.
- `predict_random_forests.py`: Python script to predict temperature and rod pressure using the pre-trained Random Forest models.

### 4. **Other Files**
- `simulation_results_with_pressure_without_early_values.csv`: CSV file containing simulation results.

---

## Usage Instructions

### Running the Prediction Scripts

#### **1. Predicting with XGBoost Models (`predict_xgboost.py`)**
This script uses pre-trained XGBoost models to predict temperature and rod pressure. The input data must be scaled using the provided scalers.

**How to Run:**
1. Prepare your input data as a 2D array with columns:
   ```
   [lhgr, fuel_radius, gap_size, clad_thickness, coolant_temperature, time]
   ```
   Example:
   ```python
   sample_input = np.array([
       [25941.6, 0.004107, 0.00018261, 0.000954, 594.924, 11494.46648],
       [25941.6, 0.004107, 0.00018261, 0.000954, 594.924, 194243.7632]
   ])
   ```

2. Run the script:
   ```bash
   python predict_xgboost.py
   ```
3. Example output:
   ```
   Predictions: {'temperature': [...], 'rod_pressure': [...]}
   ```

---

#### **2. Predicting with Random Forest Models (`predict_random_forests.py`)**
This script uses pre-trained Random Forest models to predict temperature and rod pressure. No scaling is needed for input data.

**How to Run:**
1. Prepare your input data as a 2D array with columns:
   ```
   [lhgr, fuel_radius, gap_size, clad_thickness, coolant_temperature, time]
   ```
   Example:
   ```python
   sample_input = np.array([
       [25941.6, 0.004107, 0.00018261, 0.000954, 594.924, 11494.46648],
       [25941.6, 0.004107, 0.00018261, 0.000954, 594.924, 194243.7632]
   ])
   ```

2. Run the script:
   ```bash
   python predict_random_forests.py
   ```
3. Example output:
   ```
   Predictions: {'temperature': [...], 'rod_pressure': [...]}
   ```

---

### Notes:
- Ensure that all required model files and scalers are in the same directory as the scripts.
- If a file is missing, the script will raise a `FileNotFoundError`.

---

## Dependencies

- Python 3.7 or higher
- Libraries:
  - `numpy`
  - `joblib`
  - `pickle`
  - `xgboost`
  - `scikit-learn` (version 1.3.2 recommended for compatibility)
  - `scipy` 

Install dependencies using:
```bash
pip install numpy joblib xgboost scikit-learn scipy
```

---

## Example Input and Output

### Input:
A 2D array where each row contains the following columns:
```
lhgr, fuel_radius, gap_size, clad_thickness, coolant_temperature, time
```

Example:
```python
sample_input = np.array([
    [25941.6, 0.004107, 0.00018261, 0.000954, 594.924, 11494.46648],
    [25941.6, 0.004107, 0.00018261, 0.000954, 594.924, 194243.7632]
])
```

### Output:
A dictionary containing the predicted temperature and/or rod pressure:
```python
{'temperature': [600, 610], 'rod_pressure': [15, 18]}
```
