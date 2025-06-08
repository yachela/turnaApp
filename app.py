from flask import Flask, jsonify
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
    profesionales = conn.execute('SELECT * FROM profesionales').fetchall()
    conn.close()
    return jsonify([dict(p) for p in profesionales])

@app.route('/profesionales/<int:profesional_id>/servicios', methods=['GET'])
def get_servicios_por_profesional(profesional_id):
    conn = get_db_connection()
    servicios = conn.execute(
        'SELECT * FROM servicios WHERE profesional_id = ?',
        (profesional_id,)
    ).fetchall()
    conn.close()
    return jsonify([dict(s) for s in servicios])

if __name__ == '__main__':
    app.run(debug=True, port=5001)