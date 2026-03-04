import sys
import os
import datetime

# --- CONFIGURACIÓN DE RUTAS INTELIGENTE ---
current_dir = os.path.dirname(os.path.abspath(__file__))
# Si estamos en la carpeta "de afuera", entramos a la subcarpeta
nested_folder = os.path.join(current_dir, "backend-lummia-platform-main")

if os.path.exists(os.path.join(nested_folder, "src")):
    sys.path.insert(0, nested_folder)
else:
    sys.path.insert(0, current_dir)

# --- IMPORTACIONES ---
try:
    from src.config.db import get_mongodb_db
    print(" Módulos de Lummia encontrados.")
except ImportError as e:
    print(f" Error: No se encontró 'src'. Revisa que estés en la carpeta correcta.")
    sys.exit(1)

def initialize_lummia_cloud():
    print(" Conectando Lummia Platform a MongoDB Atlas...")
    db = get_mongodb_db()
    
    if db is not None:
        collection = db['stream_cache']
        init_doc = {
            "id": "current_live",
            "video_id": None,
            "timestamp": 0,
            "status": "cloud_active",
            "last_init": datetime.datetime.now()
        }
        
        try:
            collection.update_one({"id": "current_live"}, {"$setOnInsert": init_doc}, upsert=True)
            print(" ¡CONEXIÓN EXITOSA!")
            print(f" Base de datos '{db.name}' activa en la nube.")
        except Exception as e:
            print(f" Error al escribir: {e}")
    else:
        print(" Revisa tu contraseña Lummia2026%40 en el .env")

if __name__ == "__main__":
    initialize_lummia_cloud()