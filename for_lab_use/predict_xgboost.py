import numpy as np
import pickle


def predict(input_data, predict_target="both"):
    """
    Predict temperature and/or rod pressure using the best XGBoost models.

    Parameters:
    input_data (array-like): A 2D array or matrix with columns
        [lhgr, fuel_radius, gap_size, clad_thickness, coolant_temperature, time].
    predict_target (str): Specify the target to predict: 'temperature', 'rod_pressure', or 'both'.

    Returns:
    dict: Predicted temperature and/or rod pressure values as a dictionary.
    """
    # Validate input data
    if input_data.ndim != 2:
        raise ValueError(
            "Input data must be a 2D array with columns [lhgr, fuel_radius, gap_size, clad_thickness, coolant_temperature, time]."
        )

    # Load scalers and models
    try:
        with open("scaler_temperature.pkl", "rb") as temp_scaler_file:
            scaler_temp = pickle.load(temp_scaler_file)
        with open("best_xgboost_model_temperature.pkl", "rb") as temp_model_file:
            model_temp = pickle.load(temp_model_file)
    except FileNotFoundError as e:
        raise FileNotFoundError("Temperature scaler or model file not found.") from e

    try:
        with open("scaler_rodpressure.pkl", "rb") as pressure_scaler_file:
            scaler_pressure = pickle.load(pressure_scaler_file)
        with open("best_xgboost_model_rodpressure.pkl", "rb") as pressure_model_file:
            model_pressure = pickle.load(pressure_model_file)
    except FileNotFoundError as e:
        raise FileNotFoundError("Rod pressure scaler or model file not found.") from e

    # Predictions
    results = {}
    if predict_target in ["temperature", "both"]:
        input_data_temp_scaled = scaler_temp.transform(input_data)
        results["temperature"] = model_temp.predict(input_data_temp_scaled)

    if predict_target in ["rod_pressure", "both"]:
        input_data_pressure_scaled = scaler_pressure.transform(input_data)
        results["rod_pressure"] = model_pressure.predict(input_data_pressure_scaled)

    return results


if __name__ == "__main__":
    # Example usage with a matrix input
    sample_input = np.array(
        [
            [25941.6, 0.004107, 0.00018261, 0.000954, 594.924, 11494.46648],
            [25941.6, 0.004107, 0.00018261, 0.000954, 594.924, 194243.7632],
        ]
    )  # Example input

    try:
        # Predict both temperature and rod pressure
        predictions = predict(sample_input, predict_target="both")
        print("Predictions:", predictions)
    except Exception as e:
        print(f"Error: {e}")
