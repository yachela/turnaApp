from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

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

if __name__ == '__main__':
    app.run(debug=True)