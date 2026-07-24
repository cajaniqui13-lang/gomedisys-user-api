from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

    return True
    