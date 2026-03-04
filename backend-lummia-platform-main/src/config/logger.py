import logging
import os

# Creamos la carpeta logs si no existe
if not os.path.exists('logs'):
    os.makedirs('logs')

def setup_logger():
    """sistema de logging para Lummia Platform."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("logs/lummia_app.log"), # Guarda en archivo
            logging.StreamHandler() # Muestra en consola
        ]
    )
    return logging.getLogger("LummiaLogger")

logger = setup_logger()