@echo off
setlocal


echo =====================================
echo DeepMedicV2 Setup Script (Windows)
echo =====================================


echo Checking if Git is installed...
where git >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Git is not installed or not in PATH
    echo Please install Git from: https://git-scm.com/download/win
    echo After installation, restart your command prompt and try again.
    pause
    exit /b 1
)
echo Git found: OK

set REPO_URL=https://github.com/DarkSteelD/DeepMedicV2.git
set PROJECT_NAME=DeepMedicV2

echo Cloning DeepMedicV2 repository...
echo Repository: %REPO_URL%
echo Branch: master

if exist "%PROJECT_NAME%" (
    echo Directory %PROJECT_NAME% already exists. Removing it...
    rmdir /s /q "%PROJECT_NAME%"
    if %errorlevel% neq 0 (
        echo Error: Failed to remove existing directory
        echo Please check if any files are in use and try again.
        pause
        exit /b 1
    )
)

echo Starting git clone...
git clone -b master "%REPO_URL%" "%PROJECT_NAME%"

if %errorlevel% neq 0 (
    echo Error: Failed to clone repository
    echo This could be due to:
    echo - Network connectivity issues
    echo - Repository access issues
    echo - Insufficient disk space
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)

echo Repository cloned successfully!
echo Project directory: %PROJECT_NAME%

cd "%PROJECT_NAME%"
if %errorlevel% neq 0 (
    echo Warning: Could not change to project directory
)

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