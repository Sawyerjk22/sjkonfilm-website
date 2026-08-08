$baseUrl = "https://sjkonfilm.work"
$files = @("index.html", "about.html", "contact.html", "works.html", "pages/street.html", "pages/scenes.html", "pages/color.html", "pages/vertical.html")
$date = (Get-Date).ToString("yyyy-MM-dd")

$xml = "<?xml version=`"1.0`" encoding=`"UTF-8`"?>`n<urlset xmlns=`"http://www.sitemaps.org/schemas/sitemap/0.9`">"

foreach ($file in $files) {
    # Format URL and map index.html to the root domain cleanly
    $url = "$baseUrl/$file".Replace("\", "/")
    $url = $url.Replace("/index.html", "/") 
    
    $xml += "`n  <url>`n    <loc>$url</loc>`n    <lastmod>$date</lastmod>`n  </url>"
}

$xml += "`n</urlset>"
Set-Content -Path "sitemap.xml" -Value $xml -Encoding UTF8
Write-Host "sitemap.xml successfully generated."