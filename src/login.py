from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import (
    BASE_URL,
    GOMEDISYS_USER,
    GOMEDISYS_PASS,
    WAIT_TIMEOUT
)

from src.driver import get_driver

def login():
    """
    Inicia sesión en Gomedisys y devuelve el navegador autenticado.
    """

    driver = get_driver()

    driver.get(BASE_URL)

    wait = WebDriverWait(driver, WAIT_TIMEOUT)

    usuario_input = wait.until(
        EC.visibility_of_element_located((By.ID, "uiUserName"))
    )

    print("Usuario:", GOMEDISYS_USER)
    print("Contraseña:", "*" * len(GOMEDISYS_PASS) if GOMEDISYS_PASS else "VACÍA")

    usuario_input.send_keys(GOMEDISYS_USER)

    password_input = wait.until(
        EC.visibility_of_element_located((By.ID, "uiUserPwd"))
    )

    password_input.send_keys(GOMEDISYS_PASS)

    login_button = wait.until(
        EC.element_to_be_clickable((By.ID, "btSubmit"))
    )

    login_button.click()

    return driver
