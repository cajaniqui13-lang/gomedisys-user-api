from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from config import HEADLESS


def get_driver():
    """
    Crea y devuelve una instancia configurada de Chrome.
    """

    options = Options()

    # Mantiene la ventana abierta al finalizar el script
    options.add_experimental_option("detach", True)

    # Ejecutar sin interfaz gráfica (opcional)
    if HEADLESS:
        options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)

    driver.maximize_window()

    return driver
