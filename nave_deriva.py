from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

# Tabla de sistemas dañados y sus códigos
SYSTEM_CODES = {
    "navigation": "NAV-01",
    "communications": "COM-02",
    "life_support": "LIFE-03",
    "engines": "ENG-04",
    "deflector_shield": "SHLD-05"
}

# Simulación del sistema dañado
damaged_system = "engines"  # Puedes cambiar este valor para pruebas

@app.route('/status', methods=['GET'])
def status():
    """
    Primera llamada: Retorna el sistema dañado en formato JSON.
    """
    return jsonify({"damaged_system": damaged_system})

@app.route('/repair-bay', methods=['GET'])
def repair_bay():
    """
    Segunda llamada: Genera una página HTML con el código del sistema dañado.
    """
    system_code = SYSTEM_CODES.get(damaged_system, "UNKNOWN")
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Repair</title>
    </head>
    <body>
        <div class="anchor-point">{{ system_code }}</div>
    </body>
    </html>
    """
    return render_template_string(html_template, system_code=system_code)

@app.route('/teapot', methods=['POST'])
def teapot():
    """
    Tercera llamada: Retorna un código de estado HTTP 418 (I'm a teapot).
    """
    return "I'm a teapot", 418

if __name__ == '__main__':
    # Ejecuta la aplicación en el puerto 5001
    app.run(host='0.0.0.0', port=5001)