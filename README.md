# Gomedisys User API

API REST desarrollada en Python para automatizar la desactivación de usuarios en Gomedisys utilizando Selenium y Flask.

## Características

- Inicio de sesión automático en Gomedisys.
- Selección automática de la sede de trabajo.
- Navegación al módulo Configuración de Usuarios.
- Búsqueda de usuarios por documento.
- Desactivación de usuarios activos.
- Detección de usuarios ya inactivos.
- Manejo de usuarios inexistentes.
- Registro de eventos en archivos de log.

## Tecnologías utilizadas

- Python 3
- Flask
- Selenium
- ChromeDriver

## Instalación

1. Clonar el repositorio:

```bash
git clone <URL_DEL_REPOSITORIO>
```

2. Entrar al proyecto:

```bash
cd gomedisys-user-api
```

3. Crear el entorno virtual:

```bash
python -m venv .venv
```

4. Activar el entorno virtual.

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Windows CMD:

```cmd
.venv\Scripts\activate.bat
```

5. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

6. Configurar el archivo `.env` con las credenciales de acceso.

7. Ejecutar la API:

```bash
python app.py
```

La API quedará disponible en:

```
http://127.0.0.1:5000
```

## Endpoint

### POST /desactivar

Ejemplo de petición:

```json
{
    "documento": "900000001"
}
```

Respuesta cuando el usuario fue desactivado:

```json
{
    "ok": true,
    "mensaje": "Usuario desactivado correctamente."
}
```

Respuesta cuando el usuario ya estaba inactivo:

```json
{
    "ok": true,
    "mensaje": "El usuario ya se encontraba inactivo."
}
```

Respuesta cuando el usuario no existe:

```json
{
    "ok": false,
    "mensaje": "No se encontró un usuario con ese documento."
}
```

## Estructura del proyecto

```
gomedisys-user-api/
│
├── logs/
├── src/
│   ├── api.py
│   ├── login.py
│   ├── logger.py
│   └── usuarios.py
│
├── app.py
├── config.py
├── README.md
└── requirements.txt
```

## Autor

Carlos Javier Nieva Quiceno