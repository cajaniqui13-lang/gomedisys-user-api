from src.login import login
from src.usuarios import desactivar_usuario

driver = login()

desactivar_usuario(driver, "111111111")

input("Presiona ENTER para cerrar...")

driver.quit()
