import bisect
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

class Interpolacion:
    def __init__(self, db_config):
        self.db_config = db_config
        self.data = self.fetch_data_from_db()
        self.bi_values = [row[0] for row in self.data]

    def fetch_data_from_db(self):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            query = "SELECT Bi, lambda1, A1 FROM Coeficientes_Bi ORDER BY Bi"
            cursor.execute(query)
            
            data = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return data
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    def get_value(self, bi, column):
        if not self.data:
            return None

        # Buscamos el valor exacto
        exact_match = next((row for row in self.data if row[0] == bi), None)
        if exact_match:
            return exact_match[column]

        # Si no hay coincidencia exacta, interpolamos
        if bi < self.bi_values[0]:
            return self.data[0][column]
        if bi > self.bi_values[-1]:
            return self.data[-1][column]

        index = bisect.bisect_right(self.bi_values, bi)
        x0, y0 = float(self.data[index-1][0]), float(self.data[index-1][column])
        x1, y1 = float(self.data[index][0]), float(self.data[index][column])

        return y0 + (y1 - y0) * (bi - x0) / (x1 - x0)

    def get_lambda1(self, bi):
        return self.get_value(bi, 1)

    def get_A1(self, bi):
        return self.get_value(bi, 2)

    def get_bi_given_lambda1(self, lambda1):
        if not self.data:
            return None

        exact_match = next((row for row in self.data if row[1] == lambda1), None)
        if exact_match:
            return exact_match[0]

        if lambda1 < self.data[0][1]:
            return self.data[0][0]
        if lambda1 > self.data[-1][1]:
            return self.data[-1][0]

        index = bisect.bisect_right([row[1] for row in self.data], lambda1)
        x0, y0 = float(self.data[index-1][1]), float(self.data[index-1][0])
        x1, y1 = float(self.data[index][1]), float(self.data[index][0])

        return y0 + (y1 - y0) * (lambda1 - x0) / (x1 - x0)
    
    def get_bi_given_A1(self, A1):
        if not self.data:
            return None

        exact_match = next((row for row in self.data if row[2] == A1), None)
        if exact_match:
            return exact_match[0]

        if A1 < self.data[0][2]:
            return self.data[0][0]
        if A1 > self.data[-1][2]:
            return self.data[-1][0]

        index = bisect.bisect_right([row[2] for row in self.data], A1)
        x0, y0 = float(self.data[index-1][2]), float(self.data[index-1][0])
        x1, y1 = float(self.data[index][2]), float(self.data[index][0])

        return y0 + (y1 - y0) * (A1 - x0) / (x1 - x0)
