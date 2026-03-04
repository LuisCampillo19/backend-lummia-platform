from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import time

# Importamos tu configuración y conexiones de bases de datos
from src.config.env import Config
from src.config.db import get_mysql_connection, get_mongodb_db, close_mysql_connection

# Inicialización de la App
app = Flask(__name__)
CORS(app) # Permite la conexión con tu frontend de Vanilla JS

# Validar configuración al arrancar el servidor
try:
    Config.validate_config()
except ValueError as e:
    print(e)
    exit(1)

# --- 1. ENDPOINT DE STREAMING (Usa MongoDB) ---
@app.route('/api/stream/status', methods=['GET'])
def get_stream_status():
    """
    Consulta si el canal de Lummia está en vivo.
    Usa MongoDB para cachear el resultado y no agotar la cuota de la API.
    """
    db_mongo = get_mongodb_db()
    if not db_mongo:
        return jsonify({"error": "No se pudo conectar a MongoDB"}), 500

    stream_coll = db_mongo['stream_cache']
    ahora = time.time()

    # Buscamos en caché para ahorrar peticiones a YouTube
    cache = stream_coll.find_one({"id": "current_live"})

    # Si no hay caché o es más vieja de 5 minutos (300 seg), actualizamos
    if not cache or (ahora - cache['timestamp'] > 300):
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={Config.YOUTUBE_CHANNEL_ID}&type=video&eventType=live&key={Config.YOUTUBE_API_KEY}"
        
        try:
            response = requests.get(url).json()
            video_id = response['items'][0]['id']['videoId'] if response.get('items') else None
            
            # Actualizamos MongoDB
            stream_coll.update_one(
                {"id": "current_live"},
                {"$set": {"video_id": video_id, "timestamp": ahora}},
                upsert=True
            )
            return jsonify({"videoId": video_id, "source": "youtube_api"})
        except Exception as e:
            return jsonify({"error": f"Error al consultar YouTube: {str(e)}"}), 500

    return jsonify({"videoId": cache['video_id'], "source": "mongodb_cache"})


# --- 2. ENDPOINT DE USUARIOS (Usa MySQL) ---
@app.route('/api/users/register', methods=['POST'])
def register_user():
    """
    Registra un nuevo usuario en la plataforma.
    Usa MySQL para garantizar orden y seguridad en los perfiles.
    """
    data = request.json
    db_mysql = get_mysql_connection()
    
    if not db_mysql:
        return jsonify({"error": "No se pudo conectar a MySQL"}), 500

    cursor = db_mysql.cursor(dictionary=True)
    try:
        # Query para insertar usuario (Previene SQL Injection)
        sql = "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)"
        values = (data['username'], data['email'], data['password'], 'student')
        
        cursor.execute(sql, values)
        db_mysql.commit()
        
        return jsonify({"message": "Usuario registrado exitosamente en Lummia"}), 201
    except Exception as e:
        return jsonify({"error": f"Error en MySQL: {str(e)}"}), 400
    finally:
        close_mysql_connection(db_mysql, cursor)


# --- 3. ENDPOINT DE PERFIL (Usa MySQL) ---
@app.route('/api/users/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    """Obtiene los datos de un perfil desde MySQL."""
    db_mysql = get_mysql_connection()
    cursor = db_mysql.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT id, username, email, role FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        
        if user:
            return jsonify(user), 200
        return jsonify({"message": "Usuario no encontrado"}), 404
    finally:
        close_mysql_connection(db_mysql, cursor)


# --- EJECUCIÓN DEL SERVIDOR ---
if __name__ == '__main__':
    # Usamos las variables de Config para arrancar
    app.run(port=Config.PORT, debug=Config.DEBUG)