# Project 2: Machine learning-based predictions of rod temperature and pressure in a nuclear reactor

## Overview

This project develops surrogate machine learning (ML) models for predicting rod temperature (Trod) and rod pressure (Prod) in a nuclear reactor core. Traditional physics-based simulations, though precise, are computationally expensive. This work aims to create ML models that enable rapid, accurate predictions based on key physical and geometric parameters, allowing real-time decision-making and anomaly detection.

The repository contains Jupyter notebooks, Python scripts, simulation files, and a report detailing the methodology, results, and implications of the project.

---

## Project Files and Structure

### Main Components:
1. **Report**  
   - **`CSS433_Machine_Learning___Project_2_report_ver_finale.pdf`**  
     This document provides a detailed explanation of the project's objectives, data, models, and results. It serves as the main reference for understanding the project's context and findings.

2. **Jupyter Notebooks**  
   These notebooks demonstrate model training, evaluation, and feature engineering:
   - **`RodPressure_GBDT_unscaled.ipynb`**: Contains the implementation and analysis for gradient boosting models predicting rod pressure. (approx. 1h)
   - **`RodPressure_base_line.ipynb`**: Provides baseline model performance for rod pressure predictions. (approx. 10 min)
   - **`T_GBDT_unscaled.ipynb`**: Covers gradient boosting models for predicting rod temperature. (approx. 1h)
   - **`T_base_line.ipynb`**: Presents baseline temperature prediction models.(approx. 10 min)
   - **`NN_ft_exp_LR.ipynb`**: Includes additional experimentation or detailed visualizations on neural networks and least square with feature expansion. (approx. 1h)
   - **`Random_Forest.ipynb`**: Implements Random Forest models for regression tasks, analyzing feature importance and model performance metrics.

3. **Python Scripts**  
   These scripts automate simulation data preparation, cleaning, and processing:
   - **`run.py`**: Generates and executes multiple simulation cases based on predefined parameter ranges. It manages parallel runs, adjusts simulation parameters dynamically, and allows users to specify the file in which results are stored.
   - **`cleanup.py`**: Deletes unnecessary simulation cases while allowing specific cases to be excluded from deletion.
   - **`parse.py`**: Extracts simulation results and merges them with metadata into a comprehensive CSV file.
   - **`evaluate_rmse_time.py`**: Analyzes the relationship between polynomial degree in feature expansion and RMSE for the least squares method. It also tracks computation time for each degree, generating visualizations to identify the optimal polynomial degree.


4. **Dataset**  
   - **`simulation_results_with_pressure_without_early_values.csv`**: Contains processed simulation data with features and outputs for ML training.

5. **BaseCase Folder**  
   - **`baseCase/`**: This folder contains the base environment setup required for running the simulations. Ensure this folder is included in your working directory before executing any scripts to create another dataset using OFFBeat (an OpenFOAM-based nuclear simulator). The `baseCase` setup can be extended with scripts such as `run.py` to test various parameter ranges (e.g., LHGR, fuel radius, gap size, cladding thickness, coolant temperature). Simulation outputs like temperature and pressure are saved in the `postProcessing/` folder, providing training data for the ML model.

---

## Installation and Usage

### Requirements and Library citations
- **Python 3.8+**
- Dependencies: Install required libraries using:
  ```bash
  pip install -r requirements.txt
  ```
- **OpenFOAM 9**: Download and install from the [OpenFOAM website](https://openfoam.org).
- **OFFBEAT 2.1**: Obtain and configure as per instructions on the [OFFBEAT website](https://foam-for-nuclear.gitlab.io/offbeat/installation/).

---

## Running the Scripts

### Data Generation
Use `run.py` to generate simulation data. Ensure that the `baseCase` folder is set up in your environment and specify the file where results should be stored:
```bash
python run.py
```

### Data Cleanup
Delete unused simulation cases with `cleanup.py`:
```bash
python cleanup.py
```

### Data Processing
Parse and consolidate simulation results using `parse.py`:
```bash
python parse.py
```

### Notebook Workflow
Open the relevant Jupyter notebooks in your preferred environment:
```bash
jupyter notebook RodPressure_GBDT_unscaled.ipynb
```
Follow the instructions and execute the cells sequentially to replicate the experiments.

### Polynomial RMSE and Computation Time Analysis
Evaluate the relationship between polynomial degree, RMSE, and computation time using `evaluate_rmse_time.py`:
```bash
python evaluate_rmse_time.py
```
This script outputs:
- **`rmse_and_computation_time_vs_degree_log.pdf`**: A log-scaled plot of RMSE and computation time against polynomial degree.
- **`evaluation_results.csv`**: A CSV file recording RMSE and computation time for each polynomial degree.


---

## Results and Performance

The results demonstrate the effectiveness of surrogate ML models:

- **Random Forest** and **XGBoost** performed exceptionally well for both temperature and pressure predictions.
- Feature expansion and noise analysis highlighted robustness across various scenarios.

Detailed results, including model comparisons, hyperparameter tuning, and validation metrics, are available in the final report and in respective Jupyter notebooks.

---

## Contributors

- **Göktuğ İlter**  
- **Guillaume Salha**  
- **Jean Lefort**  


