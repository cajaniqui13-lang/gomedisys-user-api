from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import (
    BASE_URL,
    USERNAME,
    PASSWORD,
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

    usuario_input.send_keys(USERNAME)

    password_input = wait.until(
        EC.visibility_of_element_located((By.ID, "uiUserPwd"))
    )

    password_input.send_keys(PASSWORD)

    login_button = wait.until(
        EC.element_to_be_clickable((By.ID, "btSubmit"))
    )

    login_button.click()

    return driver