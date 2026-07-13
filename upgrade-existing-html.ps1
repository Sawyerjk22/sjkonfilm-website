$ErrorActionPreference = "SilentlyContinue"
$htmlFiles = @("index.html", "about.html", "pages\street.html", "pages\scenes.html", "pages\color.html", "pages\vertical.html")

foreach ($file in $htmlFiles) {
    if (Test-Path $file) {
        $content = Get-Content $file -Raw -Encoding UTF8
        
        # Regex to find <img> tags that DO NOT already have a srcset attribute
        $pattern = '(<img\s+src="([^"]+/thumbs/)([^"]+)\.webp")(?!\s+srcset)'
        
        # Injects the 400w and 900w srcset definitions directly after the src attribute
        $content = [regex]::Replace($content, $pattern, {
            param($match)
            $fullMatch = $match.Groups[1].Value
            $path = $match.Groups[2].Value
            $filename = $match.Groups[3].Value
            
            return "$fullMatch srcset=`"$path$filename-400w.webp 400w, $path$filename.webp 900w`" sizes=`"(max-width: 768px) 100vw, 33vw`""
        })
        
        Set-Content -Path $file -Value $content -Encoding UTF8
    }
}
Write-Host "Existing HTML files upgraded with srcset."