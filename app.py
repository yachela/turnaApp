from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

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

@app.route('/profesionales', methods=['GET'])
def get_profesionales():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM profesionales').fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/profesionales', methods=['POST'])
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
def eliminar_profesional(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM profesionales WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'eliminado'})

@app.route('/profesionales/<int:prof_id>/servicios', methods=['GET'])
def get_servicios_por_profesional(prof_id):
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
    rows = conn.execute('SELECT * FROM turnos').fetchall()
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

@app.route('/turnos', methods=['POST'])
def crear_turno():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO turnos (profesional_id, cliente_id, servicio_id, fecha, hora) VALUES (?, ?, ?, ?, ?)',
        (data['profesional_id'], data['cliente_id'], data['servicio_id'],
        data['fecha'], data['hora'])
    )
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"}), 201

@app.route('/turnos/<int:id>', methods=['PUT'])
def actualizar_turno(id):
    data = request.get_json()
    conn = get_db_connection()
    conn.execute(
        'UPDATE turnos SET fecha = ?, hora = ? WHERE id = ?',
        (data['fecha'], data['hora'], id)
    )
    conn.commit()
    conn.close()
    return jsonify({'status': 'actualizado'})

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
    """
    1. Con get_db_connection() abrimos la conexión a la base SQLite.
    2. La consulta SELECT trae todas las filas de 'disponibilidades'
       donde profesional_id coincide con prof_id.
    3. El AND NOT IN (...) excluye aquellas franjas cuyo id ya
       exista en la tabla 'turnos' para ese mismo profesional.
    4. Devolvemos un JSON con solo los registros libres.
    """
    conn = get_db_connection()
    rows = conn.execute(
        """
        SELECT d.*
        FROM disponibilidades d
        WHERE d.profesional_id = ?
          AND d.id NOT IN (
              SELECT disponibilidad_id
              FROM turnos
              WHERE profesional_id = ?
          )
        """,
        (prof_id, prof_id)
    ).fetchall()
    conn.close()

    return jsonify([dict(row) for row in rows])

if __name__ == '__main__':
    app.run(debug=True, port=5002)