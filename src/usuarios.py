from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import WAIT_TIMEOUT


def desactivar_usuario(driver, documento):
    """
    Busca un usuario en Gomedisys y lo desactiva.
    """

    wait = WebDriverWait(driver, WAIT_TIMEOUT)

    # Entrar al módulo Configuración de Usuarios
    boton_usuarios = wait.until(
        EC.element_to_be_clickable((By.ID, "27"))
    )

    boton_usuarios.click()

    return True
    