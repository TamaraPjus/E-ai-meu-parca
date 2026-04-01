@echo off
cd /d "C:\Users\tamara.araujo\PJUS INVESTIMENTOS EM DIREITOS CREDITORIOS LTDA\USwork - INTELIGENCIA DE MERCADO\02. robos\e_ai_meu_parca"

echo.
echo ============================================================
echo  Publicando dashboard no GitHub...
echo ============================================================
echo.

:: Verifica se o remote ja esta configurado
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Remote "origin" nao configurado.
    echo.
    echo Execute o seguinte comando UMA VEZ para conectar ao GitHub:
    echo.
    echo   git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
    echo.
    echo Depois rode este script novamente.
    pause
    exit /b 1
)

:: Adiciona os arquivos que mudam a cada execucao
git add e_ai_meu_parca.html parceiros_data.json

:: Cria commit com data/hora
for /f "tokens=1-3 delims=/ " %%a in ("%date%") do set DT=%%c-%%b-%%a
for /f "tokens=1-2 delims=: " %%a in ("%time%") do set HM=%%a:%%b
git commit -m "Atualizacao automatica %DT% %HM% - dashboard + dados" 2>&1

:: Push para o GitHub
echo.
echo Enviando para GitHub...
git push origin master 2>&1

if errorlevel 1 (
    echo.
    echo [AVISO] Push falhou. Verifique sua conexao ou credenciais do GitHub.
    echo Dica: rode  git push origin master  manualmente para ver o erro completo.
) else (
    echo.
    echo [OK] Dashboard publicado com sucesso no GitHub!
    echo.
    :: Exibe a URL do GitHub Pages se configurado
    for /f "tokens=*" %%u in ('git remote get-url origin 2^>nul') do (
        set REPO_URL=%%u
    )
    echo Repositorio: %REPO_URL%
)

echo.
