$ErrorActionPreference = "Stop"

Write-Host "=====================================" -ForegroundColor Green
Write-Host "DeepMedicV2 Setup Script (PowerShell)" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

Write-Host "Checking if Git is installed..." -ForegroundColor Cyan
try {
    $gitVersion = git --version 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Git command failed"
    }
    Write-Host "Git found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Git is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Git from: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host "After installation, restart PowerShell and try again." -ForegroundColor Yellow
    Write-Host "Press any key to exit..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

$RepoUrl = "https://github.com/DarkSteelD/DeepMedicV2.git"
$ProjectName = "DeepMedicV2"

Write-Host "Cloning DeepMedicV2 repository..." -ForegroundColor Cyan
Write-Host "Repository: $RepoUrl" -ForegroundColor Yellow
Write-Host "Branch: master" -ForegroundColor Yellow

if (Test-Path $ProjectName) {
    Write-Host "Directory $ProjectName already exists. Removing it..." -ForegroundColor Yellow
    try {
        Remove-Item -Path $ProjectName -Recurse -Force
    } catch {
        Write-Host "Error: Failed to remove existing directory" -ForegroundColor Red
        Write-Host "Please check if any files are in use and try again." -ForegroundColor Yellow
        Write-Host "Error details: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "Press any key to exit..." -ForegroundColor Yellow
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        exit 1
    }
}

try {
    Write-Host "Starting git clone..." -ForegroundColor Cyan
    git clone -b master $RepoUrl $ProjectName
    
    if ($LASTEXITCODE -ne 0) {
        throw "Git clone failed with exit code $LASTEXITCODE"
    }
    
    Write-Host "Repository cloned successfully!" -ForegroundColor Green
    Write-Host "Project directory: $ProjectName" -ForegroundColor Green
    
    try {
        Set-Location $ProjectName
        Write-Host "Current directory: $(Get-Location)" -ForegroundColor Cyan
        Write-Host "Repository contents:" -ForegroundColor Cyan
        Get-ChildItem | Format-Table Name, Length, LastWriteTime
    } catch {
        Write-Host "Warning: Could not change to project directory" -ForegroundColor Yellow
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Yellow
    }
    
    Write-Host "=====================================" -ForegroundColor Green
    Write-Host "Setup completed successfully!" -ForegroundColor Green
    Write-Host "=====================================" -ForegroundColor Green
    Write-Host "To get started:" -ForegroundColor Cyan
    Write-Host "  cd $ProjectName" -ForegroundColor White
    Write-Host "  # Follow the README.md for further instructions" -ForegroundColor White
    Write-Host "=====================================" -ForegroundColor Green
    
} catch {
    Write-Host "Error: Failed to clone repository" -ForegroundColor Red
    Write-Host "This could be due to:" -ForegroundColor Yellow
    Write-Host "- Network connectivity issues" -ForegroundColor Yellow
    Write-Host "- Repository access issues" -ForegroundColor Yellow
    Write-Host "- Insufficient disk space" -ForegroundColor Yellow
    Write-Host "- Firewall blocking the connection" -ForegroundColor Yellow
    Write-Host "Please check your internet connection and try again." -ForegroundColor Yellow
    Write-Host "Error details: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Press any key to exit..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host "Press any key to continue..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 