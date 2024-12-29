import numpy as np
from joblib import load

print('bonjour')

def predict_random_forests(input_data, predict_target="both"):
    """
    Predict temperature and/or rod pressure using the best random forests models.

    Parameters:
    input_data (array-like): A 2D array or matrix with columns
        [lhgr, fuel_radius, gap_size, clad_thickness, coolant_temperature, time].
    predict_target (str): Specify the target to predict: 'temperature', 'rod_pressure', or 'both'.
    The input data is not scaled, since scaling is not needed for random forests

    Returns:
    dict: Predicted temperature and/or rod pressure values as a dictionary.
    """
    # Validate input data
    if input_data.ndim != 2:
        raise ValueError(
            "Input data must be a 2D array with columns [lhgr, fuel_radius, gap_size, clad_thickness, coolant_temperature, time]."
        )
    
    print('test')

    # Load models
    try:
        model_temp = load("random_forest_model_temperature.joblib")
    except FileNotFoundError as e:
        raise FileNotFoundError("Temperature model file not found.") from e

    try:
        model_pressure = load("random_forest_model_pressure.joblib")
    except FileNotFoundError as e:
        raise FileNotFoundError("Rod pressure model file not found.") from e

    # Predictions
    results = {}
    if predict_target in ["temperature", "both"]:
        results["temperature"] = model_temp.predict(input_data)

    if predict_target in ["rod_pressure", "both"]:
        results["rod_pressure"] = model_pressure.predict(input_data)

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
        predictions = predict_random_forests(sample_input, predict_target="both")
        print("Predictions:", predictions)
    except Exception as e:
        print(f"Error: {e}")
