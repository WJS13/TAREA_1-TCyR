import serial
import mysql.connector
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_ADDON_HOST")
MYSQL_USER = os.getenv("MYSQL_ADDON_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_ADDON_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_ADDON_DB")

ser = serial.Serial('', 9600)  

data = {}

def store_data(temp_amb, temp_centro, temp_sup):
    now = datetime.now().strftime('%H:%M:%S')
    data['T_amb'] = temp_amb
    data['T_centro'] = temp_centro
    data['T_sup'] = temp_sup
    data['Hora'] = now

db = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE
)

cursor = db.cursor()

def insert_data():
    if data:
        sql = "INSERT INTO Temperatura (T_amb, T_centro, T_sup, Hora) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (data['T_amb'], data['T_centro'], data['T_sup'], data['Hora']))
        db.commit()
        data.clear()

try:
    while True:
        line = ser.readline().decode('utf-8').strip()
        print(f"Línea leída: {line}")

        parts = line.split()
        temp_amb = temp_centro = temp_sup = None

        for part in parts:
            key, temp = part.split(':')
            if key == 'T_amb':
                temp_amb = temp
            elif key == 'T_centro':
                temp_centro = temp
            elif key == 'T_sup':
                temp_sup = temp

        if temp_amb and temp_centro and temp_sup:
            store_data(temp_amb, temp_centro, temp_sup)
            insert_data()

except KeyboardInterrupt:
    print("Interrumpido por el usuario")

finally:
    cursor.close()
    db.close()
    ser.close()
