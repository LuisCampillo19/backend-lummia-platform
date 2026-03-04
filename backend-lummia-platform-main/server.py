from app import app
from src.config.env import Config
from src.config.logger import logger

if __name__ == '__main__':
    try:
        logger.info(f"Iniciando servidor de Lummia Platform en el puerto {Config.PORT}...")
        # Levantamos la app de Flask importada de app.py
        app.run(
            host='0.0.0.0', # Permite conexiones externas si es necesario
            port=Config.PORT,
            debug=Config.DEBUG
        )
    except Exception as e:
        logger.error(f"Error fatal al iniciar el servidor: {e}")