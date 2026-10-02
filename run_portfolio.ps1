<#
.SYNOPSIS
    Kernelwise Labs Portfolio Master Runner (PowerShell Wrapper)
.DESCRIPTION
    Quick execution wrapper for executing any or all portfolio projects one by one.
.EXAMPLE
    .\run_portfolio.ps1
    .\run_portfolio.ps1 -Project 1
    .\run_portfolio.ps1 -All
    .\run_portfolio.ps1 -TestAll
#>

param(
    [Alias("p")]
    [string]$Project,

    [Alias("a")]
    [switch]$All,

    [Alias("t")]
    [switch]$TestAll,

    [Alias("w")]
    [switch]$Web,

    [Alias("l")]
    [switch]$List,

    [switch]$Website
)

$argsList = @()

if ($List) {
    $argsList += "--list"
} elseif ($Website) {
    $argsList += "--website"
} elseif ($All) {
    $argsList += "--all"
} elseif ($TestAll) {
    $argsList += "--test-all"
} elseif ($Project) {
    $argsList += "--project", $Project
    if ($Web) {
        $argsList += "--web"
    }
}

if ($argsList.Count -eq 0) {
    python "$PSScriptRoot\run_portfolio.py"
} else {
    python "$PSScriptRoot\run_portfolio.py" @argsList
}
