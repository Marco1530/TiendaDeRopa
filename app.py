from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- Base de datos simulada ---
prendas = [
    {"id": 1, "nombre": "Camisa", "precio": 15000, "stock": 10},
    {"id": 2, "nombre": "Pantalón", "precio": 25000, "stock": 5}
]

# --- Endpoints CRUD ---
@app.route('/prendas', methods=['GET'])
def get_prendas():
    return jsonify(prendas)

@app.route('/prendas', methods=['POST'])
def add_prenda():
    data = request.get_json()
    nueva = {
        "id": len(prendas) + 1,
        "nombre": data["nombre"],
        "precio": data["precio"],
        "stock": data["stock"]
    }
    prendas.append(nueva)
    return jsonify(nueva), 201

@app.route('/prendas/<int:prenda_id>', methods=['PUT'])
def update_prenda(prenda_id):
    data = request.get_json()
    for p in prendas:
        if p["id"] == prenda_id:
            p["nombre"] = data["nombre"]
            p["precio"] = data["precio"]
            p["stock"] = data["stock"]
            return jsonify(p)
    return jsonify({"error": "Prenda no encontrada"}), 404

@app.route('/prendas/<int:prenda_id>', methods=['DELETE'])
def delete_prenda(prenda_id):
    global prendas
    prendas = [p for p in prendas if p["id"] != prenda_id]
    return jsonify({"message": "Prenda eliminada"})

# --- Endpoints Reportes ---
@app.route('/reportes/marcas-ventas', methods=['GET'])
def marcas_ventas():
    marcas = [{"nombre": "Nike"}, {"nombre": "Adidas"}, {"nombre": "Puma"}]
    return jsonify(marcas)

@app.route('/reportes/prendas-stock', methods=['GET'])
def prendas_stock():
    prendas_info = [
        {"nombre": "Camisa", "vendidas": 3, "stock": 10},
        {"nombre": "Pantalón", "vendidas": 2, "stock": 5}
    ]
    return jsonify(prendas_info)

@app.route('/reportes/top-marcas', methods=['GET'])
def top_marcas():
    top = [
        {"nombre": "Nike", "ventas": 15},
        {"nombre": "Adidas", "ventas": 12},
        {"nombre": "Puma", "ventas": 8}
    ]
    return jsonify(top)

# --- Ruta para la página web ---
@app.route('/')
def index():
    return render_template('index.html')

# --- Arrancar servidor Flask ---
if __name__ == '__main__':
    app.run(debug=True)
