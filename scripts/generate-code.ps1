$ErrorActionPreference = "SilentlyContinue"
$map = @(
    @{ Cat = "street"; File = "pages\street.html"; Prefix = "../assets" },
    @{ Cat = "scenes"; File = "pages\scenes.html"; Prefix = "../assets" },
    @{ Cat = "color"; File = "pages\color.html"; Prefix = "../assets" },
    @{ Cat = "vertical"; File = "pages\vertical.html"; Prefix = "../assets" },
    @{ Cat = "featured"; File = "index.html"; Prefix = "assets" },
    @{ Cat = "about"; File = "about.html"; Prefix = "assets" }
)
$outputFile = "new-image-codes.txt"
Clear-Content $outputFile -ErrorAction SilentlyContinue
$foundAny = $false

foreach ($item in $map) {
    $cat = $item.Cat
    $htmlPath = $item.File
    $prefix = $item.Prefix
    $thumbsDir = "assets\images\$cat\thumbs"
    
    if ((Test-Path $htmlPath) -and (Test-Path $thumbsDir)) {
        $html = Get-Content $htmlPath -Raw -Encoding UTF8
        $thumbs = Get-ChildItem -Path "$thumbsDir\*.webp"
        $newTags = @()
        
        foreach ($thumb in $thumbs) {
            $fileName = $thumb.Name
            
            # CRITICAL: Skip the mobile thumbnails so they don't get their own HTML tag
            if ($fileName -match "-400w") { continue }
            
            if ($html -notmatch $fileName) {
                $base = $thumb.BaseName
                $ext = $thumb.Extension
                
                # The updated HTML tag with srcset injected
                $tag = "<img src=`"$prefix/images/$cat/thumbs/$fileName`" srcset=`"$prefix/images/$cat/thumbs/$base-400w$ext 400w, $prefix/images/$cat/thumbs/$fileName 900w`" sizes=`"(max-width: 768px) 100vw, 33vw`" data-full=`"$prefix/images/$cat/full/$fileName`" alt=`"New Location - Season Year`" width=`"900`" height=`"597`" loading=`"lazy`" decoding=`"async`">"
                $newTags += $tag
            }
        }
        
        if ($newTags.Count -gt 0) {
            $foundAny = $true
            Add-Content -Path $outputFile -Value "`n<!-- === NEW PHOTOS FOR $htmlPath === -->"
            foreach ($t in $newTags) { Add-Content -Path $outputFile -Value $t }
        }
    }
}
Write-Host "Code generation complete. Check new-image-codes.txt"