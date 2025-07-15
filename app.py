from flask import Flask, jsonify, request
import jwt
import datetime
import os
from dotenv import load_dotenv
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app, methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
print("Clave secreta cargada:", app.config['SECRET_KEY'])   

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    return response

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_access_token(usuario):
    token_data = {
        'nombre': usuario['nombre'],
        'id': usuario['id'],
        'rol': usuario['rol'],
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=3)
    }
    print("Tiempo de creacion del token (servidor):", datetime.datetime.now(datetime.timezone.utc))
    return jwt.encode(token_data, app.config['SECRET_KEY'], algorithm='HS256')

def create_refresh_token(usuario):
    token_data = {
        'nombre': usuario['nombre'],
        'id': usuario['id'],
        'rol': usuario['rol'],
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)
    }
    token = jwt.encode(token_data, app.config['SECRET_KEY'], algorithm='HS256')
    return token

@app.route('/refresh', methods=['POST'])
def refresh():
    data = request.get_json()
    refresh_token = data.get('refresh_token')

    try:
        token_data = jwt.decode(refresh_token, app.config['SECRET_KEY'], algorithms=['HS256'])
        new_access_token = create_access_token(token_data)
        return jsonify({'access_token': new_access_token})
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Refresh token caducado'}), 401
    except Exception:
        return jsonify({'message': 'Refresh token invalido'}), 401

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        #print("Headers recibidos:", dict(request.headers))
        if 'Authorization' in request.headers:
            parts = request.headers['Authorization'].split()
            if len(parts) == 2 and parts[0] == 'Bearer':
                token = parts[1]
                print("Token recibido:", token)

        if not token:
            return jsonify({'message': 'No hay token!'}), 401

        try:
            print("Tiempo actual (servidor):", datetime.datetime.now())
            token_data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            print("Datos del token decodificado:", token_data)
        except jwt.ExpiredSignatureError:
            print("Token caducado")
            return jsonify({'message': 'Token caducado!'}), 401
        except Exception:
            print("Token invalido")
            return jsonify({'message': 'Token invalido!'}), 401
        
        return f(token_data, *args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    @token_required  
    def decorated(usuario, *args, **kwargs):
        if usuario.get('rol') != 'admin':
            return jsonify({'message': 'Acceso denegado: solo para administradores'}), 403
        return f(*args, **kwargs)
    return decorated

@app.route('/profesionales', methods=['GET'])
def get_profesionales():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM profesionales').fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/profesionales', methods=['POST'])
@admin_required
def crear_profesional():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.execute(
        'INSERT INTO profesionales (nombre, especialidad, email) VALUES (?, ?, ?)',
        (data['nombre'], data['especialidad'], data['email'])
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return jsonify({**data, 'id': new_id}), 201

@app.route('/profesionales/<int:id>', methods=['GET'])
def obtener_profesional(id):
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM profesionales WHERE id = ?', (id,)).fetchone()
    conn.close()
    if row is None:
        return jsonify({'error': 'No encontrado'}), 404
    return jsonify(dict(row))

@app.route('/profesionales/<int:id>', methods=['PUT'])
@admin_required
def actualizar_profesional(id):
    data = request.get_json()
    conn = get_db_connection()
    conn.execute(
        'UPDATE profesionales SET nombre = ?, especialidad = ?, email = ? WHERE id = ?',
        (data['nombre'], data['especialidad'], data['email'], id)
    )
    conn.commit()
    conn.close()
    return jsonify({'status': 'actualizado'})

@app.route('/profesionales/<int:id>', methods=['DELETE'])
@admin_required
def eliminar_profesional(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM profesionales WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'eliminado'})

@app.route('/servicios', methods=['GET'])
@admin_required
def get_servicios():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM servicios').fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/profesionales/<int:prof_id>/servicios', methods=['GET'])
def get_servicios_por_profesional(prof_id):
    print("Obteniendo servicios para el profesional con ID:", prof_id)
    conn = get_db_connection()
    rows = conn.execute(
        'SELECT * FROM servicios WHERE profesional_id = ?',
        (prof_id,)
    ).fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/profesionales/<int:prof_id>/servicios', methods=['POST'])
def crear_servicio(prof_id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.execute(
        'INSERT INTO servicios (nombre, duracion, precio, profesional_id) VALUES (?, ?, ?, ?)',
        (data['nombre'], data['duracion'], data['precio'], prof_id)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return jsonify({**data, 'id': new_id, 'profesional_id': prof_id}), 201

@app.route('/servicios/<int:id>', methods=['GET'])
def obtener_servicio(id):
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM servicios WHERE id = ?', (id,)).fetchone()
    conn.close()
    if row is None:
        return jsonify({'error': 'No encontrado'}), 404
    return jsonify(dict(row))

@app.route('/servicios/<int:id>', methods=['PUT'])
def actualizar_servicio(id):
    data = request.get_json()
    conn = get_db_connection()
    conn.execute(
        'UPDATE servicios SET nombre = ?, duracion = ?, precio = ? WHERE id = ?',
        (data['nombre'], data['duracion'], data['precio'], id)
    )
    conn.commit()
    conn.close()
    return jsonify({'status': 'actualizado'})

@app.route('/servicios/<int:id>', methods=['DELETE'])
def eliminar_servicio(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM servicios WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'eliminado'})

@app.route('/turnos', methods=['GET'])
def listar_turnos():
    conn = get_db_connection()
    rows = conn.execute("""
        SELECT
            t.id,
            t.profesional_id,
            t.cliente_id,            
            p.nombre AS profesional_nombre,
            p.especialidad AS profesional_especialidad,
            c.nombre AS cliente_nombre,
            t.servicio_id,
            s.nombre AS servicio_nombre,
            s.duracion AS servicio_duracion,
            s.precio AS servicio_precio,
            t.fecha,
            t.hora,
            t.estado
        FROM turnos t
        JOIN profesionales p ON t.profesional_id = p.id
        JOIN servicios s ON t.servicio_id = s.id
        JOIN usuarios c ON t.cliente_id = c.id    
    """).fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/turnos/<int:id>', methods=['GET'])
def obtener_turno(id):
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM turnos WHERE id = ?', (id,)).fetchone()
    conn.close()
    if row is None:
        return jsonify({'error': 'No encontrado'}), 404
    return jsonify(dict(row))

@app.route('/mis-turnos', methods=['GET'])
@token_required
def turnos_usuario(usuario):
    usuario_id = usuario["id"]

    conn = get_db_connection()
    rows = conn.execute("""
        SELECT
            t.id,
            t.profesional_id,
            t.cliente_id,            
            p.nombre AS profesional_nombre,
            p.especialidad AS profesional_especialidad,
            c.nombre AS cliente_nombre,
            t.servicio_id,
            s.nombre AS servicio_nombre,
            s.duracion AS servicio_duracion,
            s.precio AS servicio_precio,
            t.fecha,
            t.hora,
            t.estado
        FROM turnos t
        JOIN profesionales p ON t.profesional_id = p.id
        JOIN servicios s ON t.servicio_id = s.id
        JOIN usuarios c ON t.cliente_id = c.id
        WHERE t.cliente_id = ? AND t.estado != 'cancelado'
    """, (usuario_id,)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/turnos', methods=['POST'])
@token_required
def crear_turno(usuario):
    data = request.get_json()
    estado = data.get('estado', 'pendiente')
    conn = get_db_connection()
    if usuario['rol']=='admin':
       clienteId = data['cliente_id']
    else:
       clienteId = usuario['id']
    conn.execute(
        'INSERT INTO turnos (profesional_id, cliente_id, servicio_id, fecha, hora, estado) VALUES (?, ?, ?, ?, ?, ?)',
        (data['profesional_id'], clienteId, data['servicio_id'], data['fecha'], data['hora'], estado)
    )
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"}), 201

@app.route('/turnos/<int:id>', methods=['PUT'])
@token_required
def actualizar_turno(usuario, id):
    conn = get_db_connection()
    turno = conn.execute('SELECT * FROM turnos WHERE id = ?', (id,)).fetchone()

    if not turno:
        conn.close()
        return jsonify({'message': 'Turno no encontrado'}), 404

    if usuario['rol'] != 'admin' and turno['cliente_id'] != usuario['id']:
        conn.close()
        print("Usuario no autorizado para actualizar el turno")
        return jsonify({'message': 'Acceso denegado'}), 403

    data = request.get_json()
    if usuario['rol'] == 'admin':
        conn.execute(
            'UPDATE turnos SET cliente_id = ?, profesional_id = ?, servicio_id =?, fecha = ?, hora = ?, estado =? WHERE id = ?',
            (data['cliente_id'], data['profesional_id'], data['servicio_id'], data['fecha'], data['hora'], data['estado'], id)
        )
    elif usuario['rol'] == 'cliente' and turno['cliente_id'] == usuario['id']:
        conn.execute(
            'UPDATE turnos SET estado =? WHERE id = ?',
            (data['estado'], id)
        )
    conn.commit()
    conn.close()
    return jsonify({'status': 'actualizado'})

@app.route('/turnos/<int:turno_id>', methods=['PATCH'])
@token_required 
def actualizar_estado_turno(usuario, turno_id):
    print("Actualizar estado de turno:", turno_id)
    data = request.get_json()
    print("Datos recibidos para actualizar estado de turno:", data)
    nuevo_estado = data.get('estado')
    conn = get_db_connection()
    turno = conn.execute('SELECT * FROM turnos WHERE id = ?', (id,)).fetchone()

    if not turno:
        conn.close()
        return jsonify({'message': 'Turno no encontrado'}), 404

    if turno['cliente_id'] != usuario['id']:
        conn.close()
        print("Usuario no autorizado para actualizar este turno")
        return jsonify({'message': 'Acceso denegado'}), 403

    conn.execute('UPDATE turnos SET estado = ? WHERE id = ?', (nuevo_estado, turno_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Estado de turno actualizado con éxito"})

@app.route('/turnos/<int:id>', methods=['DELETE'])
def eliminar_turno(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM turnos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'eliminado'})

@app.route('/profesionales/<int:prof_id>/disponibilidades', methods=['GET'])
def listar_disponibilidades(prof_id):
    conn = get_db_connection()
    rows = conn.execute(
        'SELECT * FROM disponibilidades WHERE profesional_id = ?',
        (prof_id,)
    ).fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/profesionales/<int:prof_id>/disponibilidades', methods=['POST'])
def crear_disponibilidad(prof_id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.execute(
        'INSERT INTO disponibilidades (profesional_id, dia_semana, fecha_especifica, hora_inicio, hora_fin) VALUES (?, ?, ?, ?, ?)',
        (
            prof_id,
            data.get('dia_semana'),
            data.get('fecha_especifica'),
            data['hora_inicio'],
            data['hora_fin']
        )
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return jsonify({**data, 'id': new_id, 'profesional_id': prof_id}), 201

@app.route('/disponibilidades/<int:id>', methods=['PUT'])
def actualizar_disponibilidad(id):
    data = request.get_json()
    conn = get_db_connection()
    conn.execute(
        'UPDATE disponibilidades SET dia_semana = ?, fecha_especifica = ?, hora_inicio = ?, hora_fin = ? WHERE id = ?',
        (
            data.get('dia_semana'),
            data.get('fecha_especifica'),
            data['hora_inicio'],
            data['hora_fin'],
            id
        )
    )
    conn.commit()
    conn.close()
    return jsonify({'status': 'actualizado'})

@app.route('/disponibilidades/<int:id>', methods=['DELETE'])
def eliminar_disponibilidad(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM disponibilidades WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'eliminado'})

@app.route('/profesionales/<int:prof_id>/disponibilidades_libres', methods=['GET'])
def listar_disponibilidades_libres(prof_id):
    conn = get_db_connection()
    rows = conn.execute(
        'SELECT * FROM disponibilidades WHERE profesional_id = ?',
        (prof_id,)
    ).fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/registration', methods=['POST'])
def register():
    data = request.get_json()

    nombre = data.get('nombre')
    email = data.get('email')
    contrasena = data.get('contrasena')

    if not nombre or not email or not contrasena:
        return jsonify({'message': 'Todos los campos son obligatorios'}), 400

    hashed_password = generate_password_hash(contrasena)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO usuarios (nombre, email, contrasena, rol) VALUES (?, ?, ?, ?)',
            (nombre, email, hashed_password, 'cliente')
        )
        conn.commit()
        return jsonify({'message': 'Usuario registrado', 'success': True}), 201

    except sqlite3.IntegrityError as e:
        print("DB error:", e)  
        return jsonify({'message': f'Error de base de datos: {str(e)}', 'success': False}), 409
    finally:
        conn.close()


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    data_email = data.get('email')
    contrasena = data.get('contrasena')
    print("Datos de login recibidos:", data)

    conn = get_db_connection()
    row = conn.execute(
        'SELECT id, nombre, email, contrasena, rol FROM usuarios WHERE email = ?',
        (data_email,)
    ).fetchone()
    conn.close()

    if row is None:
        return jsonify({'message': 'Credenciales incorrectas', 'success': False}), 401

    if not check_password_hash(row['contrasena'], contrasena):
        return jsonify({'message': 'Credenciales incorrectas', 'success': False}), 401

    usuario = dict(row)
    print("Usuario autenticado:", usuario);
    access_token = create_access_token(usuario)
    refresh_token = create_refresh_token(usuario)

    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'success': True
    })

@app.route('/usuarios', methods=['GET'])
@admin_required
def get_usuarios():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM usuarios').fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/clientes', methods=['GET'])
@admin_required
def get_clientes():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM usuarios WHERE rol = "cliente" ').fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/usuarios/<int:id>', methods=['GET'])
@admin_required
def obtener_usuario(id):
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM usuarios WHERE id = ?', (id,)).fetchone()
    conn.close()
    if row is None:
        return jsonify({'error': 'No encontrado'}), 404
    return jsonify(dict(row))

@app.route('/usuarios', methods=['POST'])
@admin_required
def crear_usuario():
    data = request.get_json()

    nombre = data.get('nombre')
    email = data.get('email')
    contrasena = data.get('contrasena')
    rol = data.get('rol')

    if not nombre or not email or not contrasena:
        return jsonify({'message': 'Todos los campos son obligatorios'}), 400

    hashed_password = generate_password_hash(contrasena)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO usuarios (nombre, email, contrasena, rol) VALUES (?, ?, ?, ?)',
            (nombre, email, hashed_password, rol)
        )
        conn.commit()
        return jsonify({'message': 'Usuario registrado', 'success': True}), 201

    except sqlite3.IntegrityError as e:
        print("DB error:", e)  
        return jsonify({'message': f'Error de base de datos: {str(e)}', 'success': False}), 409
    finally:
        conn.close()

@app.route('/usuarios/<int:id>', methods=['PUT'])
@admin_required
def actualizar_usuario(id):
    data = request.get_json()
    conn = get_db_connection()
    contrasena = data.get('contrasena', '').strip()
    if 'contrasena':
        hashed_password = generate_password_hash(contrasena)
        conn.execute(
            'UPDATE usuarios SET nombre = ?, email = ?, contrasena = ?, rol = ? WHERE id = ?',
            (data['nombre'], data['email'], hashed_password, data['rol'], id)
        )
    else:
        conn.execute(
            'UPDATE usuarios SET nombre = ?, email = ?, rol = ? WHERE id = ?',
            (data['nombre'], data['email'], data['rol'], id)
        )
    conn.commit()
    conn.close()
    return jsonify({'status': 'actualizado'})

@app.route('/usuarios/<int:id>', methods=['DELETE'])
@admin_required
def eliminar_usuario(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM usuarios WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'eliminado'})


if __name__ == '__main__':
    app.run(debug=True, port=5002)
