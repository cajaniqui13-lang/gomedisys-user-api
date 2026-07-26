from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from config import BASE_URL, WAIT_TIMEOUT


def desactivar_usuario(driver, documento):
    """
    Busca un usuario en Gomedisys y lo desactiva.
    """

    wait = WebDriverWait(driver, WAIT_TIMEOUT)

    driver.get(BASE_URL + "GeneralArea/UserSystem")

    # Esperar a que cargue la página
    wait.until(
    EC.visibility_of_element_located((By.ID, "btnSearchRecord"))
)

    # Abrir el buscador
    boton_buscar = wait.until(
    EC.element_to_be_clickable((By.ID, "btnSearchRecord"))
)

    boton_buscar.click()

    # Esperar el campo Documento del popup
    campo_documento = wait.until(
    EC.visibility_of_element_located((By.ID, "lblDocumentToFind"))
)

    campo_documento.clear()

    campo_documento.send_keys(documento)

    # Buscar el usuario
    boton_buscar_popup = wait.until(
        EC.element_to_be_clickable((By.ID, "sendFilter"))
    )

    boton_buscar_popup.click()

# Esperar el resultado de la búsqueda
    try:

     fila_usuario = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "tbody.k-table-tbody tr.k-table-row")
        )
    )

     fila_usuario.click()

    except TimeoutException:

     return {
            "ok": False,
            "mensaje": "No se encontró un usuario con ese documento."
    }          

# Esperar a que cargue el formulario del usuario
    casilla_activo = wait.until(
    EC.element_to_be_clickable((By.ID, "isActive"))
)

# Esperar a que desaparezca el loader
    wait.until(
    EC.invisibility_of_element_located((By.ID, "loader"))
)

    print("Checkbox encontrado")
    print("Está seleccionado:", casilla_activo.is_selected())
    print("Está habilitado:", casilla_activo.is_enabled())

# Solo desactivar si actualmente está activa
    if casilla_activo.is_selected():
       casilla_activo.click()

# Guardar cambios
    boton_guardar = wait.until(
    EC.element_to_be_clickable((By.ID, "btnSaveRecord"))
)

    boton_guardar.click()

    wait.until(
    EC.invisibility_of_element_located((By.ID, "loader"))
)

# Limpiar formulario para la siguiente búsqueda
    boton_nuevo = wait.until(
    EC.element_to_be_clickable((By.ID, "btnNewRecord"))
)

    wait.until(
    EC.invisibility_of_element_located(
        (By.CLASS_NAME, "notification-message")
    )
)

    boton_nuevo.click()

    wait.until(
    EC.invisibility_of_element_located((By.ID, "loader"))
)

    return {
    "ok": True,
    "mensaje": "Usuario desactivado correctamente."
}
    