import os
from datetime import datetime
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from config import BASE_URL, WAIT_TIMEOUT, RUTA_EXCEL


def guardar_usuario_inactivo_excel(documento, estado_mensaje, ruta_excel=RUTA_EXCEL):
    """
    Registra o actualiza en un archivo Excel los datos de los usuarios inactivos.
    """
    nuevo_registro = {
        "Documento": [documento],
        "Estado": [estado_mensaje],
        "Fecha_Registro": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    }
    df_nuevo = pd.DataFrame(nuevo_registro)

    try:
        if os.path.exists(ruta_excel):
            df_existente = pd.read_excel(ruta_excel)
            # Evita duplicar el mismo documento si ya fue registrado
            if documento not in df_existente["Documento"].astype(str).values:
                df_final = pd.concat([df_existente, df_nuevo], ignore_index=True)
            else:
                df_final = df_existente
        else:
            df_final = df_nuevo

        df_final.to_excel(ruta_excel, index=False)
        print(f"[Excel] Usuario {documento} guardado en {ruta_excel}")
    except Exception as e:
        print(f"[Excel] Error al escribir en Excel: {e}")


def desactivar_usuario(driver, documento):
    """
    Busca un usuario en Gomedisys y lo desactiva.
    """
    wait = WebDriverWait(driver, WAIT_TIMEOUT)
    driver.get(BASE_URL + "GeneralArea/UserSystem")

    wait.until(EC.visibility_of_element_located((By.ID, "btnSearchRecord")))
    boton_buscar = wait.until(EC.element_to_be_clickable((By.ID, "btnSearchRecord")))
    boton_buscar.click()

    campo_documento = wait.until(
        EC.visibility_of_element_located((By.ID, "lblDocumentToFind"))
    )
    campo_documento.clear()
    campo_documento.send_keys(documento)

    boton_buscar_popup = wait.until(EC.element_to_be_clickable((By.ID, "sendFilter")))
    boton_buscar_popup.click()

    try:
        fila_usuario = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "tbody.k-table-tbody tr.k-table-row")
            )
        )
        fila_usuario.click()

    except TimeoutException:
        return {"ok": False, "mensaje": "No se encontró un usuario con ese documento."}

    casilla_activo = wait.until(EC.element_to_be_clickable((By.ID, "isActive")))
    wait.until(EC.invisibility_of_element_located((By.ID, "loader")))

    # Si ya está inactivo
    if not casilla_activo.is_selected():
        boton_nuevo = wait.until(EC.element_to_be_clickable((By.ID, "btnNewRecord")))
        wait.until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "notification-message"))
        )
        boton_nuevo.click()
        wait.until(EC.invisibility_of_element_located((By.ID, "loader")))

        # Guardar en Excel
        guardar_usuario_inactivo_excel(documento, "Inactivo Previamente")

        return {"ok": True, "mensaje": "El usuario ya se encontraba inactivo."}

    # Desactivar
    casilla_activo.click()
    boton_guardar = wait.until(EC.element_to_be_clickable((By.ID, "btnSaveRecord")))
    boton_guardar.click()

    wait.until(EC.invisibility_of_element_located((By.ID, "loader")))

    boton_nuevo = wait.until(EC.element_to_be_clickable((By.ID, "btnNewRecord")))
    wait.until(
        EC.invisibility_of_element_located((By.CLASS_NAME, "notification-message"))
    )
    boton_nuevo.click()
    wait.until(EC.invisibility_of_element_located((By.ID, "loader")))

    # Guardar en Excel
    guardar_usuario_inactivo_excel(documento, "Desactivado Recientemente")

    return {"ok": True, "mensaje": "Usuario desactivado correctamente."}