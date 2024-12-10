import os
import pandas as pd


def extract_parameters_from_directory(directory_name):
    """
    Extract parameters from the top-level directory name based on the naming convention:
    lhgr_XX.X_fuelRadius_XX.X_gap_XX.X_clad_XX.X_coolant_XXX.X
    """
    params = {}
    parts = directory_name.split("_")
    try:
        params["lhgr"] = float(parts[1])
        params["fuel_radius"] = float(parts[3]) / 1e3  # Convert mm back to m
        params["gap_size"] = float(parts[5]) / 1e6  # Convert µm back to m
        params["clad_thickness"] = float(parts[7]) / 1e3  # Convert mm back to m
        params["coolant_temperature"] = float(parts[9])  # In Kelvin
    except (IndexError, ValueError):
        print(f"Error parsing directory name: {directory_name}")
    return params


def parse_volFieldValue_dat(filepath):
    """
    Parse the volFieldValue.dat file to extract time, volAverage(T), and volAverage(Bu).
    """
    results = []
    with open(filepath, "r") as file:
        for line in file:
            if line.strip() and not line.startswith(
                "#"
            ):  # Ignore comments or empty lines
                parts = line.strip().split("\t")  # Split by tab
                if len(parts) == 3:  # Ensure there are exactly 3 columns
                    try:
                        time, vol_temp, vol_bu = map(float, parts)
                        results.append(
                            {
                                "time": time,
                                "volAverage(T)": vol_temp,
                                "volAverage(Bu)": vol_bu,
                            }
                        )
                    except ValueError:
                        print(f"Skipping invalid line: {line.strip()}")
    return results


def process_simulation_data(base_folder, output_csv):
    """
    Traverse the directory tree, process volFieldValue.dat files, and create a CSV.
    """
    data = []

    for root, dirs, _ in os.walk(base_folder):
        for directory in dirs:
            case_path = os.path.join(root, directory)
            print(f"Checking case directory: {case_path}")

            # Construct the path to volFieldValue.dat
            dat_file_path = os.path.join(
                case_path,
                "postProcessing",
                "averageTemperatureAndBurnup",
                "0",
                "volFieldValue.dat",
            )
            print(f"Looking for file: {dat_file_path}")

            if os.path.exists(dat_file_path):
                print(f"Found file: {dat_file_path}")

                # Extract parameters from the case directory name
                params = extract_parameters_from_directory(directory)
                print(f"Extracted parameters: {params}")

                # Parse the volFieldValue.dat file for simulation results
                results = parse_volFieldValue_dat(dat_file_path)

                if not results:
                    print(f"No valid data found in file: {dat_file_path}")

                # Combine parameters with each simulation result row
                for result in results:
                    row = {**params, **result}
                    data.append(row)
            else:
                print(f"File not found: {dat_file_path}")

    # Check if data was collected
    if not data:
        print("No data was collected. Check your folder structure and file contents.")
    else:
        print(f"Collected {len(data)} rows of data.")

    # Convert the collected data into a DataFrame
    df = pd.DataFrame(data)

    # Save to a CSV file
    df.to_csv(output_csv, index=False)
    print(f"Data successfully saved to {output_csv}")


# Specify the base folder containing simulation cases and the output CSV file name
base_folder = "simulation_cases"
output_csv = "simulation_results.csv"

# Run the script
process_simulation_data(base_folder, output_csv)
