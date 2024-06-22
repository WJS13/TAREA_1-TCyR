import mysql.connector
from dotenv import load_dotenv
import os
from datetime import datetime

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
    def __init__(self):
        self.db_config = db_config()
        self.db = mysql.connector.connect(**self.db_config)
        self.cursor = self.db.cursor()

    def store_data(self, temp_amb, temp_centro, temp_sup):
        now = datetime.now().strftime('%H:%M:%S')
        if temp_amb is not None and temp_centro is not None and temp_sup is not None:
            sql = "INSERT INTO Temperatura (T_amb, T_centro, T_sup, Hora) VALUES (%s, %s, %s, %s)"
            values = (temp_amb, temp_centro, temp_sup, now)
            self.cursor.execute(sql, values)
            self.db.commit()
        else:
            print("Error: No se pueden insertar valores nulos en la base de datos.")

    def close_connection(self):
        self.cursor.close()
        self.db.close()
