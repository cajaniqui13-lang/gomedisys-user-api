from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import WAIT_TIMEOUT


def desactivar_usuario(driver, nombre_usuario):
    """
    Busca un usuario en Gomedisys y lo desactiva.
    """

    wait = WebDriverWait(driver, WAIT_TIMEOUT)
    