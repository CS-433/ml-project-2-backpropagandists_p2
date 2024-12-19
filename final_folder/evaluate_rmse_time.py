import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.metrics import mean_squared_error
import time


def linear_regression_model(
    df,
    feature_expansion=False,
    regularization=False,
    folder=".",
    alpha=1.0,
    plot_and_save=False,
    plot_coefs=False,
    degree=7,
):
    # Création du dossier si non existant
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Sélection des variables d'entrée et de sortie
    X = df[
        [
            "lhgr",
            "fuel_radius",
            "gap_size",
            "clad_thickness",
            "coolant_temperature",
            "time",
        ]
    ]
    y = df["volAverage(T)"]

    # Standardisation des données pour éviter les problèmes de conditionnement
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Expansion des caractéristiques si activée
    if feature_expansion:
        poly = PolynomialFeatures(
            degree=degree, interaction_only=False, include_bias=False
        )
        X_expanded = poly.fit_transform(X_scaled)
        feature_names = poly.get_feature_names_out(X.columns)
        X_scaled = X_expanded

    # Séparation des données en ensembles d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    # Création du modèle avec régularisation (Ridge) si activée
    if regularization:
        model = Ridge(alpha=alpha)
    else:
        model = LinearRegression()

    # Entraînement du modèle
    model.fit(X_train, y_train)

    # Prédictions
    y_pred = model.predict(X_test)

    # Calcul de l'erreur MSE et RMSE
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    print(f"Mean Squared Error: {mse}")
    print(f"Root Mean Squared Error (RMSE): {rmse}")

    # Paramètres utilisés dans le graphique
    feature_expansion_str = (
        "Feature Expansion" if feature_expansion else "No Feature Expansion"
    )
    regularization_str = (
        f"Regularization (alpha={alpha})" if regularization else "No Regularization"
    )

    # Plot et sauvegarde des résultats de prédiction si activé
    if plot_and_save:
        plt.figure(figsize=(8, 8))
        plt.scatter(y_test, y_pred, alpha=0.2, label="Predictions")
        plt.plot(
            [y_test.min(), y_test.max()],
            [y_test.min(), y_test.max()],
            color="red",
            linestyle="--",
            label="Ideal line",
        )
        plt.xlabel("True Values", fontsize=20)
        plt.ylabel("Predictions", fontsize=20)
        plt.title(
            f"Predictions vs True Values\n{feature_expansion_str}, {regularization_str}",
            fontsize=22,
        )
        plt.legend(title=f"RMSE: {rmse:.4f}", fontsize=16)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(
            f"{folder}/predictions_vs_true_values_{feature_expansion_str}_{regularization_str}_degree{degree}.pdf"
        )
        plt.show()
        plt.close()

    # Plot et sauvegarde des coefficients si activé
    if plot_coefs:
        coefs = model.coef_
        coef_names = X.columns if not feature_expansion else feature_names

        # Sélection des 15 plus grands coefficients en valeur absolue
        abs_coefs = np.abs(coefs)
        top_15_indices = np.argsort(abs_coefs)[-15:]

        top_15_coefs = coefs[top_15_indices]
        top_15_coef_names = [coef_names[i] for i in top_15_indices]

        plt.figure(figsize=(10, 6))
        plt.barh(top_15_coef_names, top_15_coefs)
        plt.xlabel("Coefficient Value", fontsize=20)
        plt.title(
            f"Top 15 Model Coefficients\n{feature_expansion_str}, {regularization_str}",
            fontsize=22,
        )
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(
            f"{folder}/top_15_model_coefficients_{feature_expansion_str}_{regularization_str}_degree{degree}.pdf"
        )
        plt.show()
        plt.close()

    return model, mse, rmse


def evaluate_rmse_time(df, folder="plots", regularization=False, alpha=1.0):
    results = []  # Pour stocker les résultats
    for degree in range(1, 11):  # Degré de 1 à 11
        print(f"Evaluating degree {degree}...")
        start_time = time.time()

        # Appel de la fonction de régression avec l'expansion des caractéristiques
        model, mse, rmse = linear_regression_model(
            df,
            feature_expansion=True,
            regularization=regularization,
            folder=folder,
            alpha=alpha,
            plot_and_save=False,
            plot_coefs=False,
            degree=degree,
        )

        elapsed_time = time.time() - start_time  # Temps de calcul
        print(f"Time for degree {degree}: {elapsed_time:.4f} seconds")

        # Enregistrement des résultats dans la liste
        results.append(
            {"Degree": degree, "RMSE": rmse, "Computation Time": elapsed_time}
        )

        # Sauvegarde dans un fichier CSV
        results_df = pd.DataFrame(results)
        results_df.to_csv(f"{folder}/evaluation_results.csv", index=False)

    # Lecture des résultats et tracé des courbes
    results_df = pd.read_csv(f"{folder}/evaluation_results.csv")

    plt.figure(figsize=(12, 8))

    # Axe principal pour RMSE
    ax1 = plt.gca()
    ax1.plot(
        results_df["Degree"], results_df["RMSE"], label="RMSE", marker="o", color="blue"
    )
    ax1.set_xlabel("Degree of Polynomial Expansion", fontsize=22)
    ax1.set_ylabel("RMSE (K)", fontsize=22, color="blue")
    ax1.tick_params(axis="y", labelcolor="blue", labelsize=16)
    ax1.tick_params(axis="x", labelsize=16)

    # Formatage des axes x pour n'afficher que des entiers
    ax1.set_xticks(np.arange(1, 10, 1))  # Seules les valeurs entières de 1 à 9
    ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x)}"))

    # Application de l'échelle logarithmique sur l'axe des RMSE
    ax1.set_yscale("log")

    # Axe secondaire pour le temps de calcul
    ax2 = ax1.twinx()
    ax2.plot(
        results_df["Degree"],
        results_df["Computation Time"],
        label="Computation Time",
        marker="o",
        color="black",
    )
    ax2.set_ylabel("Computation Time (s)", fontsize=22, color="black")
    ax2.tick_params(axis="y", labelcolor="black", labelsize=16)

    # Application de l'échelle logarithmique sur l'axe du temps de calcul
    ax2.set_yscale("log")

    # Formatage des axes y pour les entiers
    ax2.tick_params(axis="y", labelsize=16)

    # Suppression des lignes de grille horizontales (y) et ajout des petites marques de tirets
    ax1.grid(
        True, which="major", axis="x", color="gray", linestyle="-", linewidth=0.5
    )  # Grille uniquement sur l'axe des x
    ax1.minorticks_on()  # Activation des petites marques
    ax1.tick_params(
        axis="y", which="minor", length=5, width=1, color="blue"
    )  # Petites marques sur l'axe des y
    ax1.grid(
        True, which="minor", axis="y", color="gray", linestyle=":", linewidth=0.5
    )  # Petites marques de grille sur l'axe des y

    # Titre et légendes
    ax1.legend(loc="upper left", fontsize=18)
    ax2.legend(loc="upper right", fontsize=18)

    plt.tight_layout()
    plt.savefig(f"{folder}/rmse_and_computation_time_vs_degree_log.pdf")
    plt.show()
