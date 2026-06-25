# generate-code.ps1
$ErrorActionPreference = "SilentlyContinue"

# Map out which folders go to which HTML files
$map = @(
    @{ Cat="street"; File="pages\street.html"; Prefix="../assets" },
    @{ Cat="scenes"; File="pages\scenes.html"; Prefix="../assets" },
    @{ Cat="color"; File="pages\color.html"; Prefix="../assets" },
    @{ Cat="vertical"; File="pages\vertical.html"; Prefix="../assets" },
    @{ Cat="featured"; File="index.html"; Prefix="assets" },
    @{ Cat="about"; File="about.html"; Prefix="assets" }
)

$outputFile = "new-image-codes.txt"
Clear-Content $outputFile -ErrorAction SilentlyContinue

Write-Host "Scanning for genuinely NEW photos only..."

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
            
            # Check if this exact file name is already in your HTML
            if ($html -notmatch $fileName) {
                # If it is NOT in the HTML, build the tag
                $tag = "<img src=`"$prefix/images/$cat/thumbs/$fileName`" data-full=`"$prefix/images/$cat/full/$fileName`" alt=`"Cuba - Summer 2026`" width=`"900`" height=`"597`" loading=`"lazy`" decoding=`"async`">"
                $newTags += $tag
            }
        }
        
        # If we found missing photos, add them to the text file
        if ($newTags.Count -gt 0) {
            $foundAny = $true
            Add-Content -Path $outputFile -Value "`n"
            foreach ($t in $newTags) {
                Add-Content -Path $outputFile -Value $t
            }
            Write-Host "Found $($newTags.Count) new photos for $cat."
        }
    }
}

if ($foundAny) {
    Write-Host "Done! Open 'new-image-codes.txt' to see ONLY the missing tags."
} else {
    Write-Host "No new photos found! Everything in your folders is already in your HTML."
}