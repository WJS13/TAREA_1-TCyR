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
Cp = 1.0
radio = 1.0
masa = 1.0 
volumen = 1.0
densidad = masa/volumen
t = [0.0, 300.0, 600.0, 900.0, 1200.0, 1500.0, 1800.0, 2100.0, 2400.0, 2700.0, 3000.0, 3300.0, 3600.0]

def calcular_lambda(T_amb_list, T_centro_list, T_sup_list):
    def ecuacion(lambda1, T_amb, T_centro, T_sup):
        return (T_sup - T_amb) / (T_centro - T_amb) - np.sin(lambda1) / lambda1

    lambdas = []
    for T_amb, T_centro, T_sup in zip(T_amb_list, T_centro_list, T_sup_list):
        lambda1 = optimize.root_scalar(ecuacion, method='secant', args=(T_amb, T_centro, T_sup), x0=0.1, x1=1).root
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


def calcular_tau(lambda1, A1):
    
    tau = lambda1*1+A1
    return tau

def calcular_difusividad_termica(tau):
    difusividad_termica = (tau*radio^2)/t[1]
    return difusividad_termica

def calcular_k(difusividad_termica, Cp, densidad):
    k = difusividad_termica * Cp * densidad
    return k

def calcular_h(Bi, k):
    
    h = (Bi*k)/radio
    return h



def main():
    resultados = fetch_temperatures()
    T_amb_list, T_centro_list, T_sup_list = guardar_temperaturas(resultados)
    lambda1 = calcular_lambda(T_amb_list, T_centro_list, T_sup_list)
    tau = calcular_tau(T_amb_list, T_centro_list, T_sup_list)
    h = calcular_h(tau, T_centro_list, T_sup_list)
    k = calcular_k(h, Cp, densidad)
    difusividad_termica = calcular_difusividad_termica(k)

if __name__ == "__main__":
    main()

    




