# standardize-webp.ps1
$ErrorActionPreference = "SilentlyContinue"

# Added featured and about so it checks all 6 folders
$categories = @("street", "scenes", "color", "vertical", "featured", "about")

foreach ($cat in $categories) {
    $fullDir = "assets\images\$cat\full"

    if (Test-Path $fullDir) {
        Write-Host "Converting any JPEGs in $cat..."
        
        # Convert any .jpg or .jpeg files to high-res .webp
        magick mogrify -format webp -quality 90 "$fullDir\*.jpg"
        magick mogrify -format webp -quality 90 "$fullDir\*.jpeg"
        
        # Delete the original JPEGs to prevent messy duplicates
        Remove-Item "$fullDir\*.jpg"
        Remove-Item "$fullDir\*.jpeg"
    }
}

Write-Host "SUCCESS: All 'full' folders are now 100% WebP!"