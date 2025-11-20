@echo off
title SisRec - Inicialização Completa
echo ============================================
echo INICIANDO SISTEMA DE RECOMENDACAO DE PETS
echo ============================================

REM --------------------------------------------
REM 1) DEFINIR CAMINHO DO PROJETO
REM --------------------------------------------
set BASE_PATH=C:\Users\Usuário\Desktop\github\SisRec-Pets
set BACKEND_FILE=backend:app

REM --------------------------------------------
REM 2) ATIVAR AMBIENTE VIRTUAL (opcional)
REM --------------------------------------------
if exist "%BASE_PATH%\venv\Scripts\activate" (
    echo Ativando ambiente virtual...
    call "%BASE_PATH%\venv\Scripts\activate"
)

REM --------------------------------------------
REM 3) INICIAR BACKEND FASTAPI
REM --------------------------------------------
echo Iniciando backend FastAPI...
start cmd /k "cd /d %BASE_PATH% && uvicorn %BACKEND_FILE% --reload"

REM dar tempo para o backend subir
timeout /t 3 >nul

REM --------------------------------------------
REM 4) INICIAR SERVIDOR DO FRONTEND
REM --------------------------------------------
echo Iniciando servidor de arquivos...
start cmd /k "cd /d %BASE_PATH% && python -m http.server 8000"

REM --------------------------------------------
REM 5) ABRIR NAVEGADOR NA PÁGINA INICIAL
REM --------------------------------------------
echo Abrindo navegador...
start http://localhost:8000/index.html

echo ============================================
echo Sistema iniciado com sucesso!
echo ============================================
pause
