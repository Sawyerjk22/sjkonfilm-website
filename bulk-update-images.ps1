# bulk-update-images.ps1
# Updates category pages to use WebP thumbs + data-full while preserving alt text.

$ErrorActionPreference = "Stop"

$categories = @("street","scenes","color","vertical")

foreach ($cat in $categories) {
  $pagePath = "pages\$cat.html"
  if (!(Test-Path $pagePath)) {
    Write-Host "SKIP: $pagePath not found"
    continue
  }

  $html = Get-Content $pagePath -Raw -Encoding UTF8

  # Replace <img src="../assets/images/<cat>/<file>.<ext>" ...>
  # with <img src="../assets/images/<cat>/thumbs/<file>.webp" data-full="../assets/images/<cat>/full/<file>.webp" ...>
  #
  # Notes:
  # - Preserves the rest of the attributes (alt, loading, etc.)
  # - If data-full already exists, we won't add a second one.
  # - Handles .jpg/.jpeg/.png and case variants.

  $pattern = "<img\s+([^>]*?)src\s*=\s*`"\.\./assets/images/$cat/([^`"]+?)\.(jpg|jpeg|png|JPG|JPEG|PNG)`"([^>]*?)>"

  $updated = [regex]::Replace($html, $pattern, {
    param($m)

    $beforeAttrs = $m.Groups[1].Value
    $baseName    = $m.Groups[2].Value
    $afterAttrs  = $m.Groups[4].Value

    $newSrc  = "../assets/images/$cat/thumbs/$baseName.webp"
    $newFull = "../assets/images/$cat/full/$baseName.webp"

    $allAttrs = ($beforeAttrs + $afterAttrs)

    # If data-full already present, just swap src to thumbs and keep existing data-full
    if ($allAttrs -match "data-full\s*=") {
      return "<img ${beforeAttrs}src=`"$newSrc`"${afterAttrs}>"
    }

    # Otherwise, inject data-full right after src
    return "<img ${beforeAttrs}src=`"$newSrc`" data-full=`"$newFull`"${afterAttrs}>"
  })

  if ($updated -ne $html) {
    Set-Content -Path $pagePath -Value $updated -Encoding UTF8
    Write-Host "UPDATED: $pagePath"
  } else {
    Write-Host "NO CHANGES: $pagePath"
  }
}

Write-Host "Done."
