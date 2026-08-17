from src.login import login
from src.usuarios import desactivar_usuario


def main():

    print("========================================")
    print("          RPA DE GOMEDISYS")
    print("========================================")
    print()

    # --------------------------------
    # Solicitar documento
    # --------------------------------

    documento = input("Ingrese el documento del usuario: ").strip()

    if not documento:

        print()
        print("ERROR: Debe ingresar un documento.")
        input("\nPresiona ENTER para cerrar...")
        return

    print()
    print(f"Documento ingresado: {documento}")
    print()

    driver = None

    try:

        # --------------------------------
        # Iniciar RPA
        # --------------------------------

        print("Iniciando RPA de Gomedisys...")

        # --------------------------------
        # Login
        # --------------------------------

        print("Abriendo Gomedisys...")
        print("Iniciando sesión...")

        driver = login()

        print("Inicio de sesión completado.")
        print()

        # --------------------------------
        # Buscar y desactivar usuario
        # --------------------------------

        print("Buscando usuario...")
        print(f"Documento: {documento}")
        print()

        resultado = desactivar_usuario(driver, documento)

        # --------------------------------
        # Mostrar resultado
        # --------------------------------

        print()
        print("========================================")
        print("              RESULTADO")
        print("========================================")

        print(resultado["mensaje"])

        print()

        if resultado.get("ok"):

            print("Proceso completado correctamente.")

        else:

            print("El proceso no pudo completarse.")

        print("========================================")

    except Exception as error:

        print()
        print("========================================")
        print("                ERROR")
        print("========================================")

        print(error)

        print("========================================")

    finally:

        if driver:

            print()
            print("Cerrando navegador...")

            driver.quit()

    print()
    input("Presiona ENTER para cerrar...")


if __name__ == "__main__":
    main()
