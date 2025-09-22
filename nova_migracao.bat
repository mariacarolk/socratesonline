@echo off
REM =====================================
REM  MIGRAÇÃO AUTOMÁTICA - SÓCRATES ONLINE
REM =====================================

echo Iniciando processo de migração...

call venv\Scripts\activate.bat
set FLASK_APP=app.py

REM Solicitar descrição
set /p DESCRICAO="Descreva a mudança (ex: Adicionar campo X na tabela Y): "

REM Criar migração
echo.
echo [1/3] Criando migração...
flask db migrate -m "%DESCRICAO%"

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Erro ao criar migração!
    pause
    exit /b 1
)

REM Aplicar localmente
echo.
echo [2/3] Aplicando migração localmente...
flask db upgrade

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Erro ao aplicar migração!
    pause
    exit /b 1
)

REM Verificar status
echo.
echo [3/3] Status atual:
flask db current

echo.
echo =====================================
echo ✅ MIGRAÇÃO PRONTA PARA DEPLOY!
echo.
echo Para enviar para o Railway:
echo   git add .
echo   git commit -m "migration: %DESCRICAO%"
echo   git push origin main
echo.
echo O Railway aplicará automaticamente!
echo =====================================
pause