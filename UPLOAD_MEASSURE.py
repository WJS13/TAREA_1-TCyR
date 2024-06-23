import serial
import time
import matplotlib.pyplot as plt
import cv2
import mysql.connector
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

class ArduinoDataSender:
    def _init_(self):
        self.db_config = db_config()
        self.db = mysql.connector.connect(**self.db_config)
        self.cursor = self.db.cursor()

    def store_data(self, temp_amb, temp_centro, temp_sup, date):
        if temp_amb is not None and temp_centro is not None and temp_sup is not None:
            sql = "INSERT INTO Temperaturas (T_amb, T_centro, T_sup, Hora) VALUES (%s, %s, %s, %s)"
            values = (temp_amb, temp_centro, temp_sup, date)
            self.cursor.execute(sql, values)
            self.db.commit()
        else:
            print("Error: No se pueden insertar valores nulos en la base de datos.")

    def close_connection(self):
        self.cursor.close()
        self.db.close()

# Configuración del puerto serial
puerto_serial = 'COM13'  # Cambiar según el puerto utilizado
baud_rate = 9600
tiempo_total = 5 * 60  # 1 hora
intervalo_lectura = 1.5 * 60  # 5 minutos

# Inicializar la comunicación serial
ser = serial.Serial(puerto_serial, baud_rate)

# Inicializar listas para almacenar los datos
tiempos = []
datos1 = []
datos2 = []
datos3 = []

# Función para registrar datos en un archivo
def registrar_datos():
    with open("datos.txt", "w") as archivo:
        inicio = time.time()
        i=0
        while (time.time() - inicio) < tiempo_total:
            try:
                promedio1 = 0.0
                promedio2 = 0.0
                promedio3 = 0.0
                for _ in range(10):
                    if ser.in_waiting > 0:
                        linea = ser.readline().decode('utf-8').strip()
                        datos = linea.split(',')
                        if len(datos) == 3:
                            dato1, dato2, dato3 = map(float, datos)
                            promedio1 += dato1
                            promedio2 += dato2
                            promedio3 += dato3
                        else:
                            print("Error: número incorrecto de datos recibidos")
                    time.sleep(1.5)
                
                promedio1 /= 10
                promedio2 /= 10
                promedio3 /= 10
                
                tiempo_actual = time.strftime('%Y-%m-%d_%H-%M-%S')
                archivo.write(f"{i}, {promedio1:.3f}, {promedio2:.3f}, {promedio3:.3f},{tiempo_actual}\n")
                archivo.flush()

                tiempos.append(tiempo_actual)
                datos1.append(promedio1)
                datos2.append(promedio2)
                datos3.append(promedio3)

            except Exception as e:
                print(f"Error de lectura: {e}")

            #Tomar foto
            tomar_foto()
            i += 1
            time.sleep(intervalo_lectura - 16)  # Ajustar el tiempo para compensar los retrasos

# Función para tomar una foto con la cámara
def tomar_foto():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error al abrir la cámara")
        return
    
    ret, frame = cap.read()
    time.sleep(1)
    if ret:
        nombre_archivo = time.strftime('Pera_%Y-%m-%d_%H-%M-%S.png')
        cv2.imwrite(nombre_archivo, frame)
        print(f"Foto guardada como {nombre_archivo}")
    else:
        print("Error al capturar la imagen")

    cap.release()
    cv2.destroyAllWindows()

# Iniciar la recolección de datos
registrar_datos()

# Cerrar el puerto serial
ser.close()

#Envía las medidas a la base de datos
sender = ArduinoDataSender()

for i in range(13):
    sender.store_data(datos1[i], datos2[i], datos3[i], tiempos[i])

sender.close_connection()

# Generar gráfica con Matplotlib
plt.figure(figsize=(10, 6))
plt.plot(tiempos, datos1, label='T_inf')
plt.plot(tiempos, datos2, label='T_0')
plt.plot(tiempos, datos3, label='T_r')

plt.xlabel('Tiempo')
plt.ylabel('Valores de los datos')
plt.title('Datos recolectados vs Tiempo')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("grafico_datos.png")
plt.show()