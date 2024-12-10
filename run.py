import os
import shutil
import numpy as np
import subprocess
import math
import time

# List to keep track of running processes
running_processes = []
max_parallel_runs = 4  # Maximum number of parallel runs allowed

# Define the ranges
lhgr_range = np.linspace(10e3, 40e3, 10)  # LHGR in W/m
fuel_outer_radius_range = np.linspace(0.004, 0.005, 3)  # Fuel outer radius in m
gap_size_range = np.linspace(20e-6, 200e-6, 3)  # Gap size in m
clad_thickness_range = np.linspace(0.0005, 0.001, 3)  # Cladding thickness in m
coolant_temperature_range = np.linspace(
    290 + 273.15, 330 + 273.15, 2
)  # Coolant temp in K

# Constants
base_density = 10960 * 0.95  # kg/m3
burnup_target = 20e6  # Wd/kg
base_case_folder = "baseCase"
output_base = "simulation_cases"

# Create output folder if it doesn't exist
os.makedirs(output_base, exist_ok=True)


def calculate_runtime(Q, density):
    """Calculate total running time in seconds for a given Q."""
    power_density = Q / density  # W/kg
    runtime = burnup_target / power_density  # days
    runtime *= 24 * 3600  # seconds
    return runtime


def modify_endTime(case_folder, end_time):
    """Modify endTime in controlDict."""
    control_dict_path = os.path.join(case_folder, "system", "controlDict")
    subprocess.run(
        [
            "foamDictionary",
            control_dict_path,
            "-entry",
            "endTime",
            "-set",
            str(end_time),
        ]
    )
    subprocess.run(
        [
            "foamDictionary",
            control_dict_path,
            "-entry",
            "maxDeltaT",
            "-set",
            str(end_time / 200),
        ]
    )


def modify_heatSource(case_folder, end_time, lhgr):
    """Modify heatSourceOptions and other entries in solverDict."""
    solver_dict_path = os.path.join(case_folder, "constant", "solverDict")
    subprocess.run(
        [
            "foamDictionary",
            solver_dict_path,
            "-entry",
            "heatSourceOptions/timePoints",
            "-set",
            f"(0 60 1e15)",
        ]
    )
    subprocess.run(
        [
            "foamDictionary",
            solver_dict_path,
            "-entry",
            "heatSourceOptions/lhgr",
            "-set",
            f"(0 {lhgr} {lhgr})",
        ]
    )


def modify_rodDict(case_folder, r_fuel, r_inner_clad, r_outer_clad):
    """Modify rodDict Python dictionary for radii."""
    rod_dict_path = os.path.join(case_folder, "rodDict")

    # Read the existing Python dictionary
    with open(rod_dict_path, "r") as file:
        rod_dict = eval(file.read())  # Convert string to Python dictionary

    # Modify the necessary entries
    rod_dict["rOuterFuel"] = [r_fuel * 1e3]  # Convert to mm
    rod_dict["rInnerClad"] = [r_inner_clad * 1e3, r_inner_clad * 1e3]  # Convert to mm
    rod_dict["rOuterClad"] = [r_outer_clad * 1e3, r_outer_clad * 1e3]  # Convert to mm

    # Write back the modified dictionary
    with open(rod_dict_path, "w") as file:
        file.write(str(rod_dict))


def modify_materials(case_folder, r_fuel, gap_size):
    """Modify materials entries in solverDict."""
    solver_dict_path = os.path.join(case_folder, "constant", "solverDict")
    subprocess.run(
        [
            "foamDictionary",
            solver_dict_path,
            "-entry",
            "materials/fuel/DiamCold",
            "-set",
            f"{2 * r_fuel}",
        ]
    )
    subprocess.run(
        [
            "foamDictionary",
            solver_dict_path,
            "-entry",
            "materials/fuel/GapCold",
            "-set",
            f"{2 * gap_size}",
        ]
    )


def modify_coolant_temperature(case_folder, coolant_temperature):
    """Modify coolant temperature in boundaryField."""
    boundary_field_path = os.path.join(case_folder, "0", "T")
    subprocess.run(
        [
            "foamDictionary",
            boundary_field_path,
            "-entry",
            "boundaryField/cladOuter/value",
            "-set",
            f"uniform {coolant_temperature}",
        ]
    )


def calculate_fuel_area(r_fuel):
    """Calculate the cross-sectional area of the fuel."""
    return math.pi * (r_fuel**2)


def run_case(case_folder):
    """Run the case without waiting for completion."""
    os.chdir(case_folder)

    # Step 1: Run Allclean
    subprocess.Popen(["./Allclean"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Step 2: Run Allrun
    process = subprocess.Popen(
        ["./Allrun"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    os.chdir("../..")
    running_processes.append(process)

    # Check if the number of running processes exceeds the limit
    if len(running_processes) >= max_parallel_runs:
        wait_for_cases_to_finish()


def wait_for_cases_to_finish():
    """Wait for running cases to finish."""
    global running_processes
    while running_processes:
        for process in running_processes:
            # Check if the process has finished
            if process.poll() is not None:
                running_processes.remove(process)  # Remove completed processes
        time.sleep(1)  # Avoid busy waiting


# Main loop
for lhgr in lhgr_range:
    for fuel_outer_radius in fuel_outer_radius_range:
        for gap_size in gap_size_range:
            for clad_thickness in clad_thickness_range:
                for coolant_temperature in coolant_temperature_range:
                    # Calculate fuel area and Q
                    fuel_area = calculate_fuel_area(fuel_outer_radius)
                    Q = lhgr / fuel_area

                    # Calculate end time
                    end_time = calculate_runtime(Q, base_density)

                    # Construct case folder name
                    case_name = f"lhgr_{lhgr:.1f}_fuelRadius_{fuel_outer_radius*1e3:.1f}_gap_{gap_size*1e6:.1f}_clad_{clad_thickness*1e3:.1f}_coolant_{coolant_temperature:.1f}"
                    case_folder = os.path.join(output_base, case_name)

                    print(case_folder)

                    # Copy the base case folder
                    if os.path.exists(case_folder):
                        shutil.rmtree(case_folder)  # Remove the existing directory
                    shutil.copytree(base_case_folder, case_folder)

                    # Modify case files
                    modify_endTime(case_folder, end_time)
                    modify_heatSource(case_folder, end_time, lhgr)
                    modify_rodDict(
                        case_folder,
                        fuel_outer_radius,
                        fuel_outer_radius + gap_size,
                        fuel_outer_radius + gap_size + clad_thickness,
                    )
                    modify_materials(case_folder, fuel_outer_radius, gap_size)
                    modify_coolant_temperature(case_folder, coolant_temperature)

                    # Run the case
                    run_case(case_folder)
