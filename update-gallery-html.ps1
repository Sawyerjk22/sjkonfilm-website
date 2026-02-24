# update-gallery-html.ps1
$ErrorActionPreference = "Continue"

$categories = @("street","scenes","color","vertical")

foreach ($cat in $categories) {
    $pagePath = "pages\$cat.html"
    if (!(Test-Path $pagePath)) {
        continue
    }

    $html = Get-Content $pagePath -Raw -Encoding UTF8
    $w = if ($cat -eq "vertical") { "597" } else { "900" }
    $h = if ($cat -eq "vertical") { "900" } else { "597" }

    $counter = 0
    $updated = [regex]::Replace($html, '(?i)<img\s+([^>]+)>', {
        param($m)
        $inner = $m.Groups[1].Value
        $counter++

        # Strip old attributes to prevent duplicates
        $inner = $inner -replace '(?i)\s*loading="lazy"', ''
        $inner = $inner -replace '(?i)\s*fetchpriority="high"', ''
        $inner = $inner -replace '(?i)\s*width="\d+"', ''
        $inner = $inner -replace '(?i)\s*height="\d+"', ''
        $inner = $inner -replace '(?i)\s*decoding="async"', ''
        $inner = $inner.Trim()

        # Inject new optimized attributes (Top 3 eager, the rest lazy)
        if ($counter -le 3) {
            return "<img $inner width=`"$w`" height=`"$h`" fetchpriority=`"high`" decoding=`"async`">"
        } else {
            return "<img $inner width=`"$w`" height=`"$h`" loading=`"lazy`" decoding=`"async`">"
        }
    })

    Set-Content -Path $pagePath -Value $updated -Encoding UTF8
    Write-Host "SUCCESS: Updated $pagePath ($counter images)."
}