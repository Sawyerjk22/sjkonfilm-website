# update-instagram.ps1
$ErrorActionPreference = "Continue"

# Define your handles here
$oldHandle = "sjkonfilm"
$newHandle = "sawyer.j.knox" # <-- CHANGE THIS to your actual personal Instagram handle

# Grab all HTML files in the main folder AND the pages folder
$files = @(Get-ChildItem -Path ".\*.html" -File)
$files += @(Get-ChildItem -Path ".\pages\*.html" -File)

foreach ($file in $files) {
    $html = Get-Content $file.FullName -Raw -Encoding UTF8
    
    # Swap out the Instagram URL
    $updated = $html -replace "instagram.com/$oldHandle", "instagram.com/$newHandle"
    
    Set-Content -Path $file.FullName -Value $updated -Encoding UTF8
    Write-Host "SUCCESS: Updated Instagram link in $($file.Name)"
}