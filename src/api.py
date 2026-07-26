from flask import request, jsonify
import traceback

from src.login import login
from src.usuarios import desactivar_usuario
from src.logger import escribir_log


def registrar_rutas(app):

    @app.post("/desactivar")
    def desactivar():

        datos = request.get_json()

        documento = datos.get("documento")

        if not documento:

            escribir_log("SIN DOCUMENTO", "La petición llegó sin documento.")

            return jsonify({"ok": False, "mensaje": "Debe enviar el documento."}), 400

        driver = None

        try:

            driver = login()

            resultado = desactivar_usuario(driver, documento)

            escribir_log(documento, resultado["mensaje"])

            return jsonify(resultado)

        except Exception as e:

            traceback.print_exc()

            escribir_log(documento, f"ERROR: {str(e)}")

            return jsonify({"ok": False, "mensaje": str(e)}), 500

        finally:

            if driver:
                driver.quit()
