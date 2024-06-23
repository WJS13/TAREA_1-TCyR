import numpy as np
from scipy import optimize

def calcular_lambda(T_amb_list, T_centro_list, T_sup_list):
    def ecuacion(lambda1, T_amb, T_centro, T_sup):
        return np.abs(T_sup - T_amb) / np.abs(T_centro - T_amb) - np.sin(lambda1) / lambda1

    lambdas = []
    for T_amb, T_centro, T_sup in zip(T_amb_list, T_centro_list, T_sup_list):
        try:
            lambda1 = optimize.root_scalar(ecuacion, method='secant', args=(T_amb, T_centro, T_sup), x0=0.1, x1=1).root
        except ValueError as e:
            print(f"Error finding root for T_amb={T_amb}, T_centro={T_centro}, T_sup={T_sup}: {e}")
            lambda1 = np.nan
        lambdas.append(lambda1)

    return lambdas

T_amb_list = [23.0, 22.9, 22.9, 23.0, 22.9, 22.9, 22.9, 23.1, 23.4, 23.1, 23.3, 23.4]
T_centro_list = [-5.95, -5.826, -5.456, -5.212, -4.896, -4.679, -4.392, -3.518, -2.503, -1.488, -0.279, 0.239]
T_sup_list = [-1.981, -0.214, 0.083, 0.368, 0.872, 1.073, 1.636, 2.238, 2.568, 3.686, 4.286, 5.545]


lambdas = calcular_lambda(T_amb_list, T_centro_list, T_sup_list)
print(lambdas)
