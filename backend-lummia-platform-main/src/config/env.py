import os
from dotenv import load_dotenv


load_dotenv()

class Config:
    """
    Configuración centralizada para Lummia Platform.
    Maneja las credenciales de YouTube, MongoDB y MySQL de forma segura.
    """
    
    # --- CONFIGURACIÓN DE SERVIDOR ---
    PORT = int(os.getenv("PORT", 5000))
    DEBUG = os.getenv("DEBUG", "True") == "True"

    # --- YOUTUBE DATA API V3 ---
    
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    YOUTUBE_CHANNEL_ID = os.getenv("CHANNEL_ID", "UCd8QTo7NF9IoQPrNF9mu9VA")

    # --- MONGODB (Data Flexible / Streams) ---
    # Mantenemos tu conexión exitosa a MongoDB Atlas
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "lummia_platform_db")

    # --- MYSQL (Datos Estructurales / Aiven Cloud) ---
    
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", 10987)) 
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DB = os.getenv("MYSQL_DB", "lummia_platform")

    @classmethod
    def validate_config(cls):
        """
        Valida que las variables críticas existan para evitar errores al arrancar.
        """
        critical_vars = [
            ("YOUTUBE_API_KEY", cls.YOUTUBE_API_KEY),
            ("MYSQL_DB", cls.MYSQL_DB),
            ("MYSQL_PORT", cls.MYSQL_PORT),
            ("MONGO_URI", cls.MONGO_URI)
        ]
        
        for name, value in critical_vars:
            if not value:
                raise ValueError(f" Error: La variable {name} no está bien definida en el .env")
        
        print(f" Configuración de Lummia Platform cargada correctamente para Medellín.")

# Ejecutamos validación al importar para asegurar que la nube esté lista
if __name__ == "__main__":
    Config.validate_config()