<#
.SYNOPSIS
    Automated Multi-Account GitHub Setup for Kernelwise Labs Portfolio.
.DESCRIPTION
    1. Creates .gitconfig-portfolio in C:\Users\aravi\kernelwise-portfolio\.
    2. Configures Git includeIf in the user's global ~/.gitconfig.
    3. Checks or generates an ED25519 SSH key pair for the business account.
    4. Updates ~/.ssh/config with the github.com-kernelwise host alias.
    5. Prints the public key to add to GitHub.
#>

[CmdletBinding()]
param (
    [string]$BusinessName = "Kernelwise Labs Engineering",
    [string]$BusinessEmail = "engineering@kernelwiselabs.com",
    [string]$KeyName = "id_ed25519_kernelwise"
)

$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   Kernelwise Labs - GitHub Multi-Account Setup Wizard   " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$portfolioPath = "C:/Users/aravi/kernelwise-portfolio"
$portfolioGitConfig = "$portfolioPath/.gitconfig-portfolio"
$sshDir = Join-Path $HOME ".ssh"
$sshKeyPath = Join-Path $sshDir $KeyName
$sshConfigPath = Join-Path $sshDir "config"

# 1. Ensure .ssh directory exists
if (-not (Test-Path $sshDir)) {
    Write-Host "[1/5] Creating $sshDir..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $sshDir -Force | Out-Null
} else {
    Write-Host "[1/5] Directory $sshDir exists." -ForegroundColor Green
}

# 2. Check or Generate SSH Key
if (-not (Test-Path $sshKeyPath)) {
    Write-Host "[2/5] Generating SSH key: $sshKeyPath..." -ForegroundColor Yellow
    python -c "import subprocess; subprocess.run(['ssh-keygen', '-t', 'ed25519', '-C', '$BusinessEmail', '-f', r'$sshKeyPath', '-N', ''], check=True)"
    Write-Host "      SSH Key created successfully." -ForegroundColor Green
} else {
    Write-Host "[2/5] SSH Key $sshKeyPath already exists. Skipping creation." -ForegroundColor Green
}

# 3. Configure ~/.ssh/config
Write-Host "[3/5] Updating $sshConfigPath..." -ForegroundColor Yellow
$sshConfigContent = @"

# Business / Agency GitHub Account (Kernelwise Labs)
Host github.com-kernelwise
    HostName github.com
    User git
    IdentityFile ~/.ssh/$KeyName
    IdentitiesOnly yes
"@

$existingConfig = ""
if (Test-Path $sshConfigPath) {
    $existingConfig = Get-Content $sshConfigPath -Raw
}

if ($existingConfig -notmatch "Host github.com-kernelwise") {
    Add-Content -Path $sshConfigPath -Value $sshConfigContent
    Write-Host "      Added 'github.com-kernelwise' host alias to ~/.ssh/config." -ForegroundColor Green
} else {
    Write-Host "      Host alias 'github.com-kernelwise' already present in ~/.ssh/config." -ForegroundColor Green
}

# 4. Create .gitconfig-portfolio
Write-Host "[4/5] Writing portfolio gitconfig..." -ForegroundColor Yellow
$portfolioConfigContent = @"
[user]
    name = $BusinessName
    email = $BusinessEmail

[init]
    defaultBranch = main

[core]
    sshCommand = ssh -i ~/.ssh/$KeyName -F ~/.ssh/config
"@
Set-Content -Path "C:\Users\aravi\kernelwise-portfolio\.gitconfig-portfolio" -Value $portfolioConfigContent -Encoding UTF8
Write-Host "      Created $portfolioGitConfig" -ForegroundColor Green

# 5. Link in global ~/.gitconfig
Write-Host "[5/5] Checking global gitconfig includeIf..." -ForegroundColor Yellow
$globalGitConfigFile = Join-Path $HOME ".gitconfig"
$includeStatement = "[includeIf `"gitdir:C:/Users/aravi/kernelwise-portfolio/`"]`n    path = C:/Users/aravi/kernelwise-portfolio/.gitconfig-portfolio"

$globalConfigText = ""
if (Test-Path $globalGitConfigFile) {
    $globalConfigText = Get-Content $globalGitConfigFile -Raw
}

if ($globalConfigText -notmatch "gitdir:C:/Users/aravi/kernelwise-portfolio/") {
    Add-Content -Path $globalGitConfigFile -Value "`n$includeStatement`n"
    Write-Host "      Added directory include to global ~/.gitconfig." -ForegroundColor Green
} else {
    Write-Host "      includeIf rule already present in ~/.gitconfig." -ForegroundColor Green
}

Write-Host "`nSetup Complete! Next steps:" -ForegroundColor Cyan
Write-Host "1. Copy your public key below and paste it into GitHub Settings -> SSH and GPG keys:" -ForegroundColor Yellow
Write-Host "----------------------------------------------------------------------------------" -ForegroundColor Gray
Get-Content "$sshKeyPath.pub"
Write-Host "----------------------------------------------------------------------------------" -ForegroundColor Gray
Write-Host "2. Test the connection with:" -ForegroundColor White
Write-Host "   ssh -T git@github.com-kernelwise" -ForegroundColor Cyan
Write-Host "3. When adding remotes to any project repo in this portfolio, use:" -ForegroundColor White
Write-Host "   git remote add origin https://github.com/DAravindReddy/<repo-name>.git" -ForegroundColor Cyan
