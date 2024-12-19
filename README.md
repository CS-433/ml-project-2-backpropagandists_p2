# Project 2: Machine learning-based predictions of rod temperature and pressure in a nuclear reactor

## Overview

This project develops surrogate machine learning (ML) models for predicting rod temperature (Trod) and rod pressure (Prod) in a nuclear reactor core. Traditional physics-based simulations, though precise, are computationally expensive. This work aims to create ML models that enable rapid, accurate predictions based on key physical and geometric parameters, allowing real-time decision-making and anomaly detection.

The repository contains Jupyter notebooks, Python scripts, and a report detailing the methodology, results, and implications of the project.

---

## Project Files and Structure

### Main Components:
1. **Report**  
   - **`CSS433_Machine_Learning___Project_2_report_ver_finale.pdf`**  
     This document provides a detailed explanation of the project's objectives, data, models, and results. It serves as the main reference for understanding the project's context and findings.

2. **Jupyter Notebooks**  
   These notebooks demonstrate model training, evaluation, and feature engineering:
   - **`RodPressure_GBDT_unscaled.ipynb`**: Contains the implementation and analysis for gradient boosting models predicting rod pressure.
   - **`RodPressure_base_line.ipynb`**: Provides baseline model performance for rod pressure predictions.
   - **`T_GBDT_unscaled.ipynb`**: Covers gradient boosting models for predicting rod temperature.
   - **`T_base_line.ipynb`**: Presents baseline temperature prediction models.
   - **`labo2.ipynb`**: Includes additional experimentation or detailed visualizations on neural networks and least square with feature expansion.

3. **Python Scripts**  
   These scripts automate simulation data preparation, cleaning, and processing:
   - **`run.py`**: Generates and executes multiple simulation cases based on predefined parameter ranges. It manages parallel runs and adjusts simulation parameters dynamically.
   - **`cleanup.py`**: Deletes unnecessary simulation cases while allowing specific cases to be excluded from deletion.
   - **`parse.py`**: Extracts simulation results and merges them with metadata into a comprehensive CSV file.

4. **Dataset**  
   - **`simulation_results_with_pressure_without_early_values.csv`**: Contains processed simulation data with features and outputs for ML training.

---

## Installation and Usage

### Requirements
- **Python 3.8+**
- Dependencies: Install required libraries using:
  ```bash
  pip install -r requirements.txt
  ```

---

## Running the Scripts

### Data Generation
Use `run.py` to generate simulation data:

### Data Cleanup
Delete unused simulation cases with `cleanup.py`:

### Data Processing
Parse and consolidate simulation results using `parse.py`:

### Notebook Workflow
Open the relevant Jupyter notebooks in your preferred environment.
Follow the instructions and execute the cells sequentially to replicate the experiments.

---

## Results and Performance

The results demonstrate the effectiveness of surrogate ML models:

- **Random Forest** and **XGBoost** performed exceptionally well for both temperature and pressure predictions.
- Feature expansion and noise analysis highlighted robustness across various scenarios.

Detailed results, including model comparisons, hyperparameter tuning, and validation metrics, are available in the final report and in respective Jupyter notebooks.

---

## Contributors

- **Guillaume Salha**  
- **Jean Lefort**  
- **Göktuğ İlter**  


