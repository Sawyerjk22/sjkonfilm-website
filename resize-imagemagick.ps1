# resize-imagemagick.ps1
$ErrorActionPreference = "Continue"

# The 4 folders we are targeting
$categories = @("street", "scenes", "color", "vertical", "featured", "about")

foreach ($cat in $categories) {
    $fullDir = "assets\images\$cat\full"
    $thumbDir = "assets\images\$cat\thumbs"

    if (Test-Path $fullDir) {
        Write-Host "Processing $cat..."
        
        # The Dimension Logic: '900x' = 900px wide. 'x900' = 900px tall.
        $resizeParam = if ($cat -eq "vertical") { "x900" } else { "900x" }
        
        # Runs ImageMagick: Grabs the full files, resizes them, maintains film grain, and saves as WebP to thumbs
        magick mogrify -path $thumbDir -resize $resizeParam -format webp -quality 85 "$fullDir\*.*"
    } else {
        Write-Host "Could not find folder: $fullDir"
    }
}

Write-Host "All thumbnails successfully resized!"