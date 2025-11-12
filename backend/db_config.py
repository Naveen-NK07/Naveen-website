# db_config.py
import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",              # 🔹 your MySQL username
        password="Naveen@123",  # 🔹 your MySQL password
        database="portfolio_db"   # 🔹 your database name
    )
    return connection
