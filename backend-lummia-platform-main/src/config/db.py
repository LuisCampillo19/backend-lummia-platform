import mysql.connector
from pymongo import MongoClient
from mysql.connector import Error
from src.config.env import Config

def get_mysql_connection():
    """
    Establece y retorna una conexión a la base de datos MySQL en Aiven.
   
    """
    try:
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            port=Config.MYSQL_PORT, 
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error al conectar a MySQL en la nube: {e}")
        return None

def get_mongodb_client():
    """
    Establece y retorna el cliente de MongoDB Atlas.
   
    """
    try:
        client = MongoClient(Config.MONGO_URI)
        client.admin.command('ping')
        return client
    except Exception as e:
        print(f"Error al conectar a MongoDB: {e}")
        return None

def get_mongodb_db():
    client = get_mongodb_client()
    if client:
        return client[Config.MONGO_DB_NAME]
    return None

def close_mysql_connection(connection, cursor=None):
    if cursor:
        cursor.close()
    if connection and connection.is_connected():
        connection.close()