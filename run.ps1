#!/usr/bin/env pwsh
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "LocalRankLens - Local Search Competitive Intelligence" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting LocalRankLens analysis..." -ForegroundColor Green
Write-Host "Business: Revive Irrigation" -ForegroundColor Yellow
Write-Host "Location: Spokane, WA" -ForegroundColor Yellow
Write-Host ""

# Run the analysis
python run_localranklens.py

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Analysis Complete!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Check the 'output' folder for your HTML report" -ForegroundColor Yellow
Write-Host ""

# Open the output folder
if (Test-Path "output") {
    $latestReport = Get-ChildItem "output\*.html" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if ($latestReport) {
        Write-Host "Latest report: $($latestReport.Name)" -ForegroundColor Green
        $openReport = Read-Host "Open the report in browser? (y/n)"
        if ($openReport -eq "y" -or $openReport -eq "Y") {
            Start-Process $latestReport.FullName
        }
    }
}

Read-Host "Press Enter to exit"
