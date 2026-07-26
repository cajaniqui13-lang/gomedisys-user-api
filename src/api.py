from flask import request, jsonify

from src.login import login
from src.usuarios import desactivar_usuario


def registrar_rutas(app):

    @app.post("/desactivar")
    def desactivar():

        datos = request.get_json()

        documento = datos.get("documento")

        if not documento:
            return jsonify({
                "ok": False,
                "mensaje": "Debe enviar el documento."
            }), 400

        driver = None

        try:

            driver = login()

            desactivar_usuario(driver, documento)

            return jsonify({
                "ok": True,
                "mensaje": "Usuario desactivado correctamente."
            })

        except Exception as e:

            return jsonify({
                "ok": False,
                "mensaje": str(e)
            }), 500

        finally:

            if driver:
                driver.quit()
