import sys
import os

# --- CONFIGURACIÓN DE RUTAS INTELIGENTE (Estilo Lummia) ---
#
current_dir = os.path.dirname(os.path.abspath(__file__))
nested_folder = os.path.join(current_dir, "backend-lummia-platform-main")

if os.path.exists(os.path.join(nested_folder, "src")):
    sys.path.insert(0, nested_folder)
else:
    sys.path.insert(0, current_dir)

# --- IMPORTACIONES ---
try:
    from src.config.db import get_mysql_connection, close_mysql_connection
    from src.config.logger import logger
    print("  Módulos de Lummia (MySQL) encontrados.")
except ImportError as e:
    print(f"  Error: No se encontró 'src'. Revisa la carpeta ")
    sys.exit(1)

def initialize_mysql_cloud():
    print("  Conectando Lummia Platform a Aiven MySQL (San Francisco)...")
    db = get_mysql_connection()
    
    if db is not None:
        cursor = db.cursor()
        try:
            # Tabla de usuarios para el clan Thomson con sistema de EXP
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) NOT NULL UNIQUE,
                    email VARCHAR(100) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    role VARCHAR(20) DEFAULT 'student',
                    experience_points INT DEFAULT 0,
                    level INT DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            db.commit()
            print("  ¡CONEXIÓN EXITOSA!")
            print(f" Tabla 'users' activa en la nube de Aiven.")
        except Exception as e:
            print(f"  Error al crear tablas: {e}")
        finally:
            close_mysql_connection(db, cursor)
    else:
        print("  Error: Revisa el Host y el Puerto 10987 en tu .env")

if __name__ == "__main__":
    initialize_mysql_cloud()