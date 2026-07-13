$ErrorActionPreference = "SilentlyContinue"
$contextFile = "ai-context.md"

# Print a status message to the VS Code terminal
Write-Host "Appending codebase to $contextFile..." -ForegroundColor Cyan

# 1. Add the Appendix Header
Add-Content -Path $contextFile -Value "`n`n## 7. Appendix: Core Codebase Assets`n"

# 2. Append style.css
if (Test-Path "style.css") {
    Add-Content -Path $contextFile -Value "### style.css"
    Add-Content -Path $contextFile -Value '```css'
    Get-Content "style.css" -Raw | Add-Content -Path $contextFile
    Add-Content -Path $contextFile -Value '```'
    Write-Host "  -> Added style.css" -ForegroundColor Green
}

# 3. Append Lightbox.js
if (Test-Path "Lightbox.js") {
    Add-Content -Path $contextFile -Value "### Lightbox.js"
    Add-Content -Path $contextFile -Value '```javascript'
    Get-Content "Lightbox.js" -Raw | Add-Content -Path $contextFile
    Add-Content -Path $contextFile -Value '```'
    Write-Host "  -> Added Lightbox.js" -ForegroundColor Green
}

# 4. Append HTML Skeleton (First 75 lines of a gallery page)
if (Test-Path "pages\street.html") {
    Add-Content -Path $contextFile -Value "### Structural Sample: pages\street.html"
    Add-Content -Path $contextFile -Value '```html'
    Get-Content "pages\street.html" -TotalCount 75 | Add-Content -Path $contextFile
    Add-Content -Path $contextFile -Value '```'
    Write-Host "  -> Added HTML skeleton (pages\street.html)" -ForegroundColor Green
}

Write-Host "Done! Your AI Context file is now fully comprehensive." -ForegroundColor Cyan