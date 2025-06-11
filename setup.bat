@echo off
setlocal

REM DeepMedicV2 Setup Script for Windows
REM This script clones the DeepMedicV2 repository from GitHub

echo =====================================
echo DeepMedicV2 Setup Script (Windows)
echo =====================================

set REPO_URL=https://github.com/DarkSteelD/DeepMedicV2.git
set PROJECT_NAME=DeepMedicV2

echo Cloning DeepMedicV2 repository...
echo Repository: %REPO_URL%
echo Branch: master

REM Check if directory exists and remove it
if exist "%PROJECT_NAME%" (
    echo Directory %PROJECT_NAME% already exists. Removing it...
    rmdir /s /q "%PROJECT_NAME%"
)

REM Clone the repository
git clone -b master "%REPO_URL%" "%PROJECT_NAME%"

if %errorlevel% neq 0 (
    echo Error: Failed to clone repository
    pause
    exit /b 1
)

echo Repository cloned successfully!
echo Project directory: %PROJECT_NAME%

REM Change to project directory
cd "%PROJECT_NAME%"

echo Current directory: %cd%
echo Repository contents:
dir

echo =====================================
echo Setup completed successfully!
echo =====================================
echo To get started:
echo   cd %PROJECT_NAME%
echo   # Follow the README.md for further instructions
echo =====================================

pause 