from interpolacion import Interpolacion
import numpy as np
import mysql.connector
from scipy import optimize
from dotenv import load_dotenv
import os

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_ADDON_HOST")
MYSQL_USER = os.getenv("MYSQL_ADDON_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_ADDON_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_ADDON_DB")

def db_config():
    return {
        "host": MYSQL_HOST,
        "user": MYSQL_USER,
        "password": MYSQL_PASSWORD,
        "database": MYSQL_DATABASE
    }

def fetch_temperatures():
    db = mysql.connector.connect(**db_config())
    cursor = db.cursor()

    cursor.execute("SELECT T_amb, T_centro, T_sup FROM Temperaturas")
    resultados = cursor.fetchall()

    cursor.close()
    db.close()

    return resultados

def guardar_temperaturas(resultados):
    T_amb_list = []
    T_centro_list = []
    T_sup_list = []

    for fila in resultados:
        T_amb, T_centro, T_sup = fila
        T_amb_list.append(float(T_amb))
        T_centro_list.append(float(T_centro))
        T_sup_list.append(float(T_sup))

    return T_amb_list, T_centro_list, T_sup_list

# Constantes
Cp = 3.65
radio = 11.50e-2
masa = 0.175 
volumen1 = 500.00e-6
volumen2 = 700.00e-6
densidad = masa / np.abs(volumen1-volumen2)
t = [1, 300, 600, 900, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600]

def calcular_lambda(T_amb_list, T_centro_list, T_sup_list):
    def ecuacion(lambda1, T_amb, T_centro, T_sup):
        return (T_sup - T_amb) / (T_centro - T_amb) - np.sin(lambda1) / lambda1

    lambdas = []
    for T_amb, T_centro, T_sup in zip(T_amb_list, T_centro_list, T_sup_list):
        try:
            lambda1 = optimize.root_scalar(ecuacion, method='secant', args=(T_amb, T_centro, T_sup), x0=0.1, x1=1).root
        except ValueError as e:
            print(f"Error finding root for T_amb={T_amb}, T_centro={T_centro}, T_sup={T_sup}: {e}")
            lambda1 = np.nan
        lambdas.append(lambda1)

    return lambdas

def calcular_Bi(lambdas):
    interpolator = Interpolacion(db_config())
    Bi_list = [interpolator.get_bi_given_lambda1(lambda1) for lambda1 in lambdas]
    return Bi_list

def calcular_A1(Bi_list):
    interpolator = Interpolacion(db_config())
    A1_list = [interpolator.get_A1(Bi) for Bi in Bi_list]
    return A1_list

def calcular_tau(T_centro_list, lambdas, T_amb_list, A1_list):
    taus = []
    for i in range(len(T_centro_list)):
        tau = -np.log((T_centro_list[i] - T_amb_list[i]) / (A1_list[i] * (T_centro_list[0] - T_amb_list[i]))) / (lambdas[i] ** 2)
        taus.append(tau)
    return taus

def calcular_difusividad_termica(tau_list, radio, t_list):
    difusividad_termica_list = []
    for tau, t in zip(tau_list, t_list):
        if t != 0:  
            difusividad_termica = (tau * radio * radio) / t
            difusividad_termica_list.append(difusividad_termica)
        else:
            difusividad_termica_list.append(np.nan)
    return difusividad_termica_list

def calcular_k(difusividad_termica_list, Cp, densidad):
    k_list = []
    for difusividad_termica in difusividad_termica_list:
        k = difusividad_termica * Cp * densidad
        k_list.append(k)
    return k_list

def calcular_h(Bi_list, k_list, radio):
    h_list = []
    for Bi, k in zip(Bi_list, k_list):
        h = (Bi * k) / radio
        h_list.append(h)
    return h_list

def main():
    resultados = fetch_temperatures()
    T_amb_list, T_centro_list, T_sup_list = guardar_temperaturas(resultados)
    lambdas = calcular_lambda(T_amb_list, T_centro_list, T_sup_list)
    Bi_list = calcular_Bi(lambdas)
    A1_list = calcular_A1(Bi_list)
    tau_list = calcular_tau(T_centro_list, lambdas, T_amb_list, A1_list)
    difusividad_termica_list = calcular_difusividad_termica(tau_list, radio, t)
    k_list = calcular_k(difusividad_termica_list, Cp, densidad)
    h_list = calcular_h(Bi_list, k_list, radio)

    print(T_amb_list)
    print(T_centro_list)
    print(T_sup_list)
    print("Lambda1:", lambdas)
    print("Bi:", Bi_list)
    print("A1:", A1_list)
    print("Tau:", tau_list)
    print("Difusividad Térmica:", difusividad_termica_list)
    print("k:", k_list)
    print("h:", h_list)

if __name__ == "__main__":
    main()
