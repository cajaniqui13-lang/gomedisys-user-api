@echo off
title RPA DE GOMEDISYS

cd /d "%~dp0"

echo ========================================
echo          RPA DE GOMEDISYS
echo ========================================
echo.
echo Iniciando RPA...
echo.

if not exist ".venv\Scripts\python.exe" (
    echo ERROR: No se encontro el entorno virtual.
    echo.
    echo Ruta esperada:
    echo %cd%\.venv\Scripts\python.exe
    echo.
    pause
    exit /b 1
)

if not exist "ejecutar_rpa.py" (
    echo ERROR: No se encontro ejecutar_rpa.py
    echo.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" ejecutar_rpa.py

echo.
echo ========================================
echo       RPA DE GOMEDISYS FINALIZADO
echo ========================================
echo.

pause