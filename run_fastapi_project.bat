@echo off
setlocal

echo VODAFONE FastAPI Project loading...

REM Docker kurulu mu degil mi
where docker >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Docker kurulu degil. Docker engine kurun.
    pause
    exit /b
)

REM Docker Engine  calisiyo mu?
sc query com.docker.service | findstr /i "RUNNING" >nul
if %ERRORLEVEL% neq 0 (
    echo Docker Engine calismiyor. simdi baslatilacak...
    net start com.docker.service >nul 2>&1
    timeout /t 5 >nul
) else (
    echo Docker Engine calisiyor.
)


cd /d %~dp0


echo Docker container ayaga kaldiriliyor...
docker-compose up -d --build
echo Docker container calisiyor


pause
echo   bir sekikde docker durduruldu. exit icin bir tusa basin.

endlocal