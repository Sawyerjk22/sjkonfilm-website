$ErrorActionPreference = "SilentlyContinue"
$categories = @("street", "scenes", "color", "vertical", "featured", "about")

foreach ($cat in $categories) {
    $fullDir = "assets\images\$cat\full"
    $thumbsDir = "assets\images\$cat\thumbs"
    
    if (Test-Path $fullDir) {
        if (-not (Test-Path $thumbsDir)) { New-Item -ItemType Directory -Path $thumbsDir }
        
        # Grab all WebP files
        $images = Get-ChildItem -Path "$fullDir\*.webp"
        
        foreach ($img in $images) {
            $baseName = $img.BaseName
            $ext = $img.Extension
            
            # Define output paths
            $thumb900 = Join-Path $thumbsDir "$baseName$ext"          # Desktop standard
            $thumb400 = Join-Path $thumbsDir "$baseName-400w$ext"     # Mobile standard
            
            # Generate 900px if missing
            if (-not (Test-Path $thumb900)) {
                magick $($img.FullName) -resize 900x900 $thumb900
            }
            # Generate 400px if missing
            if (-not (Test-Path $thumb400)) {
                magick $($img.FullName) -resize 400x400 $thumb400
            }
        }
    }
}
Write-Host "Responsive thumbnails generated."