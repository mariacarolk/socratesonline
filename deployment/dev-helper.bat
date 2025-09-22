@echo off
REM Script helper para desenvolvimento do Sócrates Online
REM Executa ações comuns incluindo atualização do mapeamento

echo 🚀 HELPER DE DESENVOLVIMENTO - SÓCRATES ONLINE
echo ================================================

REM Ativar ambiente virtual
call .\venv\Scripts\activate.bat

REM Atualizar mapeamento
echo.
echo 📋 Atualizando mapeamento do sistema...
python scripts\atualizar_mapeamento.py

REM Verificar linting (se disponível)
echo.
echo 🔍 Verificando qualidade do código...
python -m flake8 app.py --count --select=E9,F63,F7,F82 --show-source --statistics 2>nul || echo Flake8 não disponível, pulando...

echo.
echo ✅ Pronto para desenvolvimento!
echo.
pause
