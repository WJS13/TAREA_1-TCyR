import numpy as np
from scipy import optimize

def calcular_lambda1(T_cascara, T_centro, T_amb):
    def ecuacion(lambda1):
        return (T_cascara - T_amb) / (T_centro -T_amb) - np.sin(lambda1) / lambda1
    
    lambda1 = optimize.root_scalar(ecuacion, method='secant', x0=0.1, x1=1).root
    return lambda1

# Ejemplo de uso
T_cascara = -1.8  # Puedes cambiar este valor
T_centro = -9
T_amb = 28.6    # Puedes cambiar este valor

lambda1 = calcular_lambda1(T_cascara, T_centro, T_amb)

print(lambda1)