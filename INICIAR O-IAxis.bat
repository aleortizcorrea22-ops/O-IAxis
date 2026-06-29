@echo off
title O-IAxis by Vrilon — Launcher
color 0B

echo.
echo  ╔══════════════════════════════════════════╗
echo  ║       O-IAxis by Vrilon  v1.4            ║
echo  ║   Financial Intelligence Platform        ║
echo  ╚══════════════════════════════════════════╝
echo.

:: Verificar que el backend no este ya corriendo
netstat -an | findstr ":8000 " | findstr "LISTENING" >nul 2>&1
if %errorlevel% equ 0 (
    echo  [OK] Backend ya esta corriendo en puerto 8000
) else (
    echo  [..] Iniciando Backend FastAPI...
    start "O-IAxis Backend" /min cmd /c "cd /d ""C:\Users\Ortiz Alejandro\O-IAxis\backend"" && ..\venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000"
    timeout /t 4 /nobreak >nul
    echo  [OK] Backend iniciado en http://localhost:8000
)

:: Verificar que el frontend no este ya corriendo
netstat -an | findstr ":3001 " | findstr "LISTENING" >nul 2>&1
if %errorlevel% equ 0 (
    echo  [OK] Frontend ya esta corriendo en puerto 3001
) else (
    echo  [..] Iniciando Frontend...
    start "O-IAxis Frontend" /min "C:\Users\Ortiz Alejandro\AppData\Local\Programs\Python\Python314\python.exe" -m http.server 3001 --bind 0.0.0.0 --directory "C:\Users\Ortiz Alejandro\O-IAxis\frontend"
    timeout /t 2 /nobreak >nul
    echo  [OK] Frontend iniciado en http://127.0.0.1:3001
)

echo.
echo  ════════════════════════════════════════════
echo  Abriendo navegador...
echo  ════════════════════════════════════════════
timeout /t 2 /nobreak >nul
start http://127.0.0.1:3001

echo.
echo  Usuario: rodolfo    Password: cto2024
echo  Usuario: admin      Password: admin2024
echo  Usuario: demo       Password: demo
echo.
echo  API Docs: http://localhost:8000/api/docs
echo.
echo  Presiona cualquier tecla para cerrar esta ventana
echo  (los servidores siguen corriendo en segundo plano)
pause >nul
