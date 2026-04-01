@echo off
cd /d "C:\Users\tamara.araujo\PJUS INVESTIMENTOS EM DIREITOS CREDITORIOS LTDA\USwork - INTELIGENCIA DE MERCADO\02. robos\e_ai_meu_parca"

echo ============================================================
echo  Iniciando pipeline e_ai_meu_parca...
echo ============================================================
echo.

:: 1. Roda o agente principal (coleta dados, classifica, gera HTML)
"C:\Users\tamara.araujo\AppData\Local\Programs\Python\Python314\python.exe" e_ai_meu_parca.py

if errorlevel 1 (
    echo.
    echo [AVISO] Agente terminou com erros. Verificar log acima.
    echo Tentando publicar mesmo assim...
)

echo.
echo ============================================================
echo  Publicando no GitHub...
echo ============================================================

:: 2. Publica automaticamente no GitHub
call publicar_no_github.bat

echo.
echo ============================================================
echo  Abrindo dashboard no navegador...
echo ============================================================

:: 3. Abre o dashboard
start "" "e_ai_meu_parca.html"

echo.
echo Pipeline concluido!
