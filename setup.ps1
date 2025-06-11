# DeepMedicV2 Setup Script for Windows (PowerShell)
# This script clones the DeepMedicV2 repository from GitHub

# Set error action preference
$ErrorActionPreference = "Stop"

Write-Host "=====================================" -ForegroundColor Green
Write-Host "DeepMedicV2 Setup Script (PowerShell)" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

$RepoUrl = "https://github.com/DarkSteelD/DeepMedicV2.git"
$ProjectName = "DeepMedicV2"

Write-Host "Cloning DeepMedicV2 repository..." -ForegroundColor Cyan
Write-Host "Repository: $RepoUrl" -ForegroundColor Yellow
Write-Host "Branch: master" -ForegroundColor Yellow

# Check if directory exists and remove it
if (Test-Path $ProjectName) {
    Write-Host "Directory $ProjectName already exists. Removing it..." -ForegroundColor Yellow
    Remove-Item -Path $ProjectName -Recurse -Force
}

# Clone the repository
try {
    git clone -b master $RepoUrl $ProjectName
    
    if ($LASTEXITCODE -ne 0) {
        throw "Git clone failed with exit code $LASTEXITCODE"
    }
    
    Write-Host "Repository cloned successfully!" -ForegroundColor Green
    Write-Host "Project directory: $ProjectName" -ForegroundColor Green
    
    # Change to project directory
    Set-Location $ProjectName
    
    Write-Host "Current directory: $(Get-Location)" -ForegroundColor Cyan
    Write-Host "Repository contents:" -ForegroundColor Cyan
    Get-ChildItem | Format-Table Name, Length, LastWriteTime
    
    Write-Host "=====================================" -ForegroundColor Green
    Write-Host "Setup completed successfully!" -ForegroundColor Green
    Write-Host "=====================================" -ForegroundColor Green
    Write-Host "To get started:" -ForegroundColor Cyan
    Write-Host "  cd $ProjectName" -ForegroundColor White
    Write-Host "  # Follow the README.md for further instructions" -ForegroundColor White
    Write-Host "=====================================" -ForegroundColor Green
    
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Press any key to continue..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host "Press any key to continue..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 