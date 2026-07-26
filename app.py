from flask import Flask
from src.api import registrar_rutas

app = Flask(__name__)

registrar_rutas(app)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
    