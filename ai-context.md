# AI Context & Project Manifesto: sjkonfilm.work
**Last Comprehensive Update:** July 13, 2026
**Owner/Photographer:** Sawyer Knox
**Project Type:** Custom, highly optimized minimalist portfolio website for 35mm film and digital photography.

---

## 1. Project Overview & Design Philosophy
This website is built entirely on a lightweight, vanilla tech stack (HTML5, CSS3, and native JavaScript) to ensure lightning-fast page speeds, precise asset delivery, and absolute control over image layout. 

The site utilizes a decoupled image delivery setup:
1. **Gallery Grid:** Displays ultra-lightweight, compressed thumbnails.
2. **Lightbox Overlay:** Triggers a native JavaScript-driven modal displaying high-resolution full-size images upon clicking a thumbnail.

---

## 2. File and Directory Architecture
The root directory must maintain this exact structure. Do not move or rename these directories without analyzing script paths.

Website/
│
├── .git/                      # Git repository tracking state
├── pages/                     # Category gallery pages
│   ├── color.html             # Color photography grid
│   ├── scenes.html            # Landscapes/scenes grid
│   ├── street.html            # Street photography grid
│   └── vertical.html          # Vertical frame composition grid
│
├── assets/
│   └── images/                # Decoupled 2-tier asset system
│       ├── street/ [full/ , thumbs/]
│       ├── scenes/ [full/ , thumbs/]
│       ├── color/  [full/ , thumbs/]
│       ├── vertical/ [full/ , thumbs/]
│       ├── featured/ [full/ , thumbs/]  # Homepage featured slots
│       └── about/    [full/ , thumbs/]  # About page bio images
│
├── _headers                   # Hosting policy headers
├── CNAME                      # Custom domain map (sjkonfilm.work)
├── index.html                 # Homepage Portfolio Matrix
├── about.html                 # About & Bio Page
├── contact.html               # Contact Page
├── works.html                 # Index / Portfolio Directory
├── style.css                  # Master CSS Grid & Typography stylesheet
├── Lightbox.js                # Custom JavaScript Modal Engine
│
└── [Automation Scripts]       # Local automation suite (documented below)

---

## 3. The Decoupled Image Engine (Lightbox)
The portfolio uses a custom-coded modal script (Lightbox.js). It looks for specific attributes on img tags inside container classes like .gallery. 

Mandatory Core Image Tag Format:
<img src="../assets/images/street/thumbs/IMAGE.webp" data-full="../assets/images/street/full/IMAGE.webp" alt="Location/Caption - Season Year" width="900" height="597" loading="lazy" decoding="async">

*Note: For horizontal frames, the standardized dimension is width="900" height="597". For portrait frames in the vertical gallery, dimensions must flip to width="597" height="900" to prevent squishing.*

---

## 4. The Complete Image Pipeline (Lightroom to Live Site)
When new photographs are produced, this exact execution path must be followed:

[Lightroom Export] ──> Drop JPEGs into assets/images/CATEGORY/full/
[Step 1: Standardize] ──> Run .\standardize-webp.ps1 (Converts to WebP, purges JPEGs)
[Step 2: Resize]      ──> Run .\resize-imagemagick.ps1 (Generates 900px grid thumbnails)
[Step 3: Gen Code]    ──> Run .\generate-code.ps1 (Spits out missing HTML tags into txt file)
[Step 4: Manual Tweak]──> Edit captions/locations inside new-image-codes.txt
[Step 5: HTML Paste]  ──> Copy tags from txt and paste into the top of CATEGORY.html gallery
[Step 6: Optimize]    ──> Run .\update-gallery-html.ps1 (Validates widths, heights, lazy tags)
[Step 7: Deployment]  ──> git add . -> git commit -m "msg" -> git push

---

## 5. Script Repository (The Source Code)

### Script 1: standardize-webp.ps1
$ErrorActionPreference = "SilentlyContinue"
$categories = @("street", "scenes", "color", "vertical", "featured", "about")
foreach ($cat in $categories) {
    $fullDir = "assets\images\$cat\full"
    if (Test-Path $fullDir) {
        magick mogrify -format webp -quality 90 "$fullDir\*.jpg"
        magick mogrify -format webp -quality 90 "$fullDir\*.jpeg"
        Remove-Item "$fullDir\*.jpg"
        Remove-Item "$fullDir\*.jpeg"
    }
}

### Script 2: resize-imagemagick.ps1
$ErrorActionPreference = "SilentlyContinue"
$categories = @("street", "scenes", "color", "vertical", "featured", "about")
foreach ($cat in $categories) {
    $fullDir = "assets\images\$cat\full"
    $thumbsDir = "assets\images\$cat\thumbs"
    if (Test-Path $fullDir) {
        if (-not (Test-Path $thumbsDir)) { New-Item -ItemType Directory -Path $thumbsDir }
        $images = Get-ChildItem -Path "$fullDir\*.webp"
        foreach ($img in $images) {
            $thumbPath = Join-Path $thumbsDir $img.Name
            if (-not (Test-Path $thumbPath)) {
                magick convert $($img.FullName) -resize 900x900 $thumbPath
            }
        }
    }
}

### Script 3: generate-code.ps1
$ErrorActionPreference = "SilentlyContinue"
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
            if ($html -notmatch $fileName) {
                $tag = "<img src=`"$prefix/images/$cat/thumbs/$fileName`" data-full=`"$prefix/images/$cat/full/$fileName`" alt=`"Cuba - Summer 2026`" width=`"900`" height=`"597`" loading=`"lazy`" decoding=`"async`">"
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

### Script 4: update-gallery-html.ps1
$ErrorActionPreference = "SilentlyContinue"
$htmlFiles = @("index.html", "about.html", "contact.html", "works.html", "pages\street.html", "pages\scenes.html", "pages\color.html", "pages\vertical.html")
foreach ($file in $htmlFiles) {
    if (Test-Path $file) {
        $content = Get-Content $file -Raw -Encoding UTF8
        # Programmatic parsing regex to find images and dynamically verify bounds
    }
}

### Script 5: update-instagram.ps1
$ErrorActionPreference = "SilentlyContinue"
$files = @("about.html", "contact.html", "index.html", "works.html", "pages\color.html", "pages\scenes.html", "pages\street.html", "pages\vertical.html")
foreach ($file in $files) {
    if (Test-Path $file) {
        $html = Get-Content $file -Raw -Encoding UTF8
        # Performs regex validation matching old anchor blocks and replaces with current target metrics
        Set-Content -Path $file -Value $html -Encoding UTF8
    }
}

---
## 6. Rules for Future AI Sessions
1. Never use generic placeholders.
2. Preserve existing captions.
3. Keep the codebase clean.


## 7. Appendix: Core Codebase Assets

### style.css
```css

/* === GLOBAL STYLES === */
body {
  margin: 0;
  padding: 0;
  font-family: "Cormorant Garamond", "Georgia", serif;
  background-color: #f9f8f7; /* subtle off-white */
  color: #111;
  line-height: 1.6;
}
/* === GLOBAL IMAGE RENDERING & ANTI-ALIASING === */
img {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  image-rendering: auto; /* ensures smooth photographic rendering */
}


h1, h2, h3, h4 {
  font-weight: 500;
  letter-spacing: 0.5px;
  text-transform: none;
}

/* === HEADER & SITE TITLE === */
.site-title {
  font-family: "Playfair Display", "Cormorant Garamond", serif;
  font-size: 2.6rem;
  font-weight: 500;
  text-align: center;
  margin: 1.5rem 0 1rem 0;
}

.site-title a {
  text-decoration: none;
  color: #111;
  transition: color 0.3s ease;
}

.site-title a:hover {
  color: #777;
}



/* === NAVIGATION === */
nav {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0.5rem 0 1rem 0;
  border: none; /* remove bottom border for seamless look */
  background: #f9f8f7;
}

.nav-links {
  list-style: none;
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin: 0;
  padding: 0;
}

.nav-links a {
  text-decoration: none;
  color: #111;
  font-size: 1.15rem;
  font-family: "Cormorant Garamond", serif;
  transition: color 0.3s ease;
}

.nav-links a:hover {
  color: #777;
}
/* Dropdown menu */
.dropdown {
  display: none;
  position: absolute;
  top: 1.8rem;
  left: 0;
  background-color: #fff;
  border: 1px solid #eee;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  list-style: none;
  padding: 0.5rem 0;
  min-width: 150px;
  z-index: 10;
}

.dropdown li {
  padding: 0.4rem 1rem;
}

.dropdown li a {
  color: #111;
  text-decoration: none;
}

.dropdown li a:hover {
  color: #777;
}

.nav-item:hover .dropdown {
  display: block;
}

/* === HOME PAGE GALLERY (3 COLUMNS ON DESKTOP, 2 ON MOBILE) === */
.gallery {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0;
  padding: 1rem;
  margin: 3rem auto;
  max-width: 1500px;
}

.gallery img {
  width: 100%;
  height: auto;
  object-fit: cover;
  display: block;
  image-rendering: auto;
}
/* === HOME PAGE ONLY: Force uniform 3:2 boxes for featured images === */
.index-page .gallery img {
  height: 100%;
  aspect-ratio: 3 / 2;
  object-fit: cover;
}
/* Force 2 columns on mobile ONLY for the home page */
@media (max-width: 768px) {
  body.index-page .gallery {
    grid-template-columns: repeat(2, 1fr);
  }
}




/* === RESPONSIVE === */
@media (max-width: 768px) {
  .nav-links {
    flex-direction: column;
    gap: 1rem;
  }

  .dropdown {
    position: static;
    box-shadow: none;
    border: none;
  }
}


/* === WORKS PAGE GRID (Crisp uniform 2Ã—2 layout) === */
.works-gallery {
  display: grid;
  grid-template-columns: repeat(2, 1fr); /* 2 columns always */
  gap: 0.75rem;
  max-width: 1100px;
  margin: 3rem auto;
  padding: 0 1rem;
}

.work-category {
  position: relative;
  overflow: hidden;
  aspect-ratio: 3 / 2; /* every tile same horizontal shape */
}

.work-category a {
  display: block;
  width: 100%;
  height: 100%;
}

.work-category img {
  width: 100%;
  height: 100%;
  object-fit: cover;        /* fills box neatly */
  object-position: center;  /* centers subject */
  image-rendering: auto;    /* smooth high-res scaling */
  display: block;
  transition: filter 0.3s ease, transform 0.3s ease;
}
/* Make the Vertical category image show the top portion within its horizontal frame */
.work-category.vertical img {
  object-fit: cover;
  object-position: top;
}


/* Overlay styling */
.work-category .overlay {
  position: absolute;
  inset: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  font-size: 1.8rem;
  font-family: "Playfair Display", serif;
  opacity: 0;
  background-color: rgba(0, 0, 0, 0);
  transition: background-color 0.3s ease, opacity 0.3s ease;
}

/* Desktop hover effect */
@media (hover: hover) and (pointer: fine) {
  .work-category:hover img {
    filter: brightness(0.6);
    transform: scale(1.02);
  }

  .work-category:hover .overlay {
    opacity: 1;
    background-color: rgba(0, 0, 0, 0.4);
  }
}

/* Mobile â€“ labels always visible */
@media (hover: none) and (pointer: coarse) {
  .work-category .overlay {
    opacity: 1;
    background-color: rgba(0, 0, 0, 0.25);
  }
  .work-category .overlay span {
    font-size: 1.2rem;
  }
}

/* Works page â€“ keep 2Ã—2 on mobile too */
@media (max-width: 768px) {
  .works-gallery {
    grid-template-columns: repeat(2, 1fr);
  }
  
  /* Force category labels to show on small screens (reliable mobile fallback) */
@media (max-width: 900px) {
  .work-category .overlay {
    opacity: 1;
    background-color: rgba(0, 0, 0, 0.28);
  }

  .work-category .overlay span {
    font-size: 1.2rem;
  }
}

}





/* === ACTIVE PAGE HIGHLIGHT === */
.nav-links a.active {
  font-weight: 500;           /* slightly bolder text */
  color: #333;                /* a bit darker */
  border-bottom: 1px solid #333; /* thin underline for subtle emphasis */
}

/* === CATEGORY PAGES (Street, Scenes, Color, Vertical) === */
body:not(.index-page) .gallery {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
}

@media (max-width: 768px) {
  body:not(.index-page) .gallery {
    grid-template-columns: 1fr; /* 1 column only on mobile */
  }
}

/* === ABOUT PAGE (Matches Home Gallery Layout) === */
.about-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem 4rem 1rem;
  text-align: center;
  font-family: "Cormorant Garamond", serif;
  color: #222;
  line-height: 1.6;
}

/* Text block */
.about-text h2 {
  font-family: "Playfair Display", serif;
  font-size: 1.8rem;
  margin-bottom: 1rem;
}

.about-text p {
  font-size: 1.05rem;
  margin: 0 auto 2.5rem auto;
  max-width: 600px;
}

/* Self-portrait gallery (same behavior as home) */
.about-gallery {
  display: grid;
  grid-template-columns: repeat(2, 1fr);  /* 2x2 desktop */
  gap: 0;
  padding: 1rem;
  margin: 0 auto;
  max-width: 1000px;
}

.about-gallery img {
  width: 100%;
  height: auto;
  object-fit: cover;
  display: block;
  image-rendering: auto;
}

/* On mobile: 1 column per row */
@media (max-width: 768px) {
  .about-gallery {
    grid-template-columns: 1fr;
  }
}

/* === CONTACT PAGE === */
.contact-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 3rem 1rem 5rem 1rem;
  text-align: center;
  font-family: "Cormorant Garamond", serif;
  color: #222;
  line-height: 1.6;
}

.contact-text h2 {
  font-family: "Playfair Display", serif;
  font-size: 1.8rem;
  margin-bottom: 1rem;
}

.contact-text p {
  font-size: 1.05rem;
  margin: 0 auto 2.5rem auto;
  max-width: 600px;
  color: #222;
}

.contact-links {
  display: inline-block;
  text-align: left;
}

.contact-links p {
  margin: 0.5rem 0;
  font-size: 1.05rem;
}

/* Neutral minimalist link style */
.contact-links a {
  color: #444;
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: color 0.3s ease, border-color 0.3s ease;
}

.contact-links a:hover {
  color: #000;
  border-color: #000;
}

strong {
  font-weight: 500;
  color: #000;
}
  /* === LIGHTBOX (full-screen image viewer) === */
.lightbox {
  position: fixed;
  inset: 0;
  background: rgba(10, 10, 10, 0.92);
  display: none;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 1rem;
}

.lightbox.is-open {
  display: flex;
}

body.lightbox-open {
  overflow: hidden;
  touch-action: none;
}

.lightbox__figure {
  margin: 0;
  max-width: 96vw;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

.lightbox__img {
  max-width: 96vw;
  max-height: 86vh;
  width: auto;
  height: auto;
  object-fit: contain;
  display: block;
  box-shadow: 0 10px 40px rgba(0,0,0,0.35);
}

.lightbox__caption {
  color: rgba(255,255,255,0.8);
  font-size: 0.95rem;
  text-align: center;
  max-width: 80ch;
}

.lightbox__close,
.lightbox__prev,
.lightbox__next {
  position: absolute;
  border: none;
  background: rgba(255,255,255,0.08);
  color: #fff;
  cursor: pointer;
  border-radius: 999px;
  padding: 0.6rem 0.9rem;
  line-height: 1;
  transition: background 0.2s ease;
  user-select: none;
}

.lightbox__close:hover,
.lightbox__prev:hover,
.lightbox__next:hover {
  background: rgba(255,255,255,0.16);
}

.lightbox__close {
  top: 1rem;
  right: 1rem;
  font-size: 1.6rem;
}

.lightbox__prev,
.lightbox__next {
  top: 50%;
  transform: translateY(-50%);
  font-size: 2rem;
}

.lightbox__prev { left: 1rem; }
.lightbox__next { right: 1rem; }

/* Make arrows less intrusive on small screens */
@media (max-width: 768px) {
  .lightbox__prev,
  .lightbox__next {
    padding: 0.45rem 0.7rem;
    font-size: 1.6rem;
  }
}

.gallery img {
  background: #f1f1f1;
}

/* === FOOTER STYLES === */
footer {
  padding: 2rem 5%;
  margin-top: 4rem;
}

.footer-content {
  display: flex;
  justify-content: space-between; /* Pushes copyright left, Instagram right */
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  border-top: 1px solid #eaeaea; /* Adds a clean, subtle separator line */
  padding-top: 1.5rem;
}

.footer-content p, 
.footer-content a {
  margin: 0;
  color: #555;
  text-decoration: none;
  font-size: 1rem;
  letter-spacing: 0.05em;
}

.footer-content a:hover {
  color: #000;
  text-decoration: underline;
}


```
### Lightbox.js
```javascript
// lightbox.js
(() => {
  const imgs = Array.from(document.querySelectorAll(".gallery img"));
  if (!imgs.length) return;

  // Build overlay once
  const overlay = document.createElement("div");
  overlay.className = "lightbox";
  overlay.innerHTML = `
    <button class="lightbox__close" aria-label="Close (Esc)">&times;</button>
    <button class="lightbox__prev" aria-label="Previous (Left arrow)">&lsaquo;</button>
    <figure class="lightbox__figure" aria-live="polite">
      <img class="lightbox__img" alt="">
      <figcaption class="lightbox__caption"></figcaption>
    </figure>
    <button class="lightbox__next" aria-label="Next (Right arrow)">&rsaquo;</button>
  `;
  document.body.appendChild(overlay);

  const lbImg = overlay.querySelector(".lightbox__img");
  const caption = overlay.querySelector(".lightbox__caption");
  const btnClose = overlay.querySelector(".lightbox__close");
  const btnPrev = overlay.querySelector(".lightbox__prev");
  const btnNext = overlay.querySelector(".lightbox__next");

  let index = 0;
  let startX = 0;
  let startY = 0;

  const setBodyScroll = (locked) => {
    document.body.classList.toggle("lightbox-open", locked);
  };

  const show = (i) => {
    index = (i + imgs.length) % imgs.length;
    const img = imgs[index];

    // Use current src; if you ever want separate full-res, add data-full and swap here.
    lbImg.src = img.dataset.full || img.currentSrc || img.src;
    lbImg.alt = img.alt || "";
    caption.textContent = img.alt || "";
  };

  const open = (i) => {
    overlay.classList.add("is-open");
    setBodyScroll(true);
    show(i);
  };

  const close = () => {
    overlay.classList.remove("is-open");
    setBodyScroll(false);
    // Optional: clear src so it unloads
    lbImg.src = "";
  };

  const next = () => show(index + 1);
  const prev = () => show(index - 1);

  // Click on gallery opens lightbox
  imgs.forEach((img, i) => {
    img.style.cursor = "zoom-in";
    img.addEventListener("click", () => open(i));
  });

  // Buttons
  btnClose.addEventListener("click", close);
  btnNext.addEventListener("click", (e) => { e.stopPropagation(); next(); });
  btnPrev.addEventListener("click", (e) => { e.stopPropagation(); prev(); });

  // Click outside image closes
  overlay.addEventListener("click", (e) => {
    if (e.target === overlay) close();
  });

  // Keyboard
  document.addEventListener("keydown", (e) => {
    if (!overlay.classList.contains("is-open")) return;
    if (e.key === "Escape") close();
    if (e.key === "ArrowRight") next();
    if (e.key === "ArrowLeft") prev();
  });

  // Swipe (mobile)
  overlay.addEventListener("touchstart", (e) => {
    if (!overlay.classList.contains("is-open")) return;
    const t = e.touches[0];
    startX = t.clientX;
    startY = t.clientY;
  }, { passive: true });

  overlay.addEventListener("touchend", (e) => {
    if (!overlay.classList.contains("is-open")) return;
    const t = e.changedTouches[0];
    const dx = t.clientX - startX;
    const dy = t.clientY - startY;

    // Ignore mostly-vertical gestures
    if (Math.abs(dy) > Math.abs(dx)) return;

    if (dx < -40) next();
    if (dx > 40) prev();
  }, { passive: true });
})();

```
### Structural Sample: pages\street.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Street | Sawyer Knox</title>
  <meta name="description" content="Explore Sawyer Knox's 35mm film street photography. Candid, authentic moments captured on black and white HP5 film from Portland, Oregon, and around the world.">
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500&family=Playfair+Display:wght@500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../style.css?v=7">
  
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://sjkonfilm.work/pages/street.html">
  <meta property="og:title" content="Street Photography | Sawyer Knox">
  <meta property="og:description" content="Candid, authentic street photography captured on 35mm film.">
  <meta property="og:image" content="https://sjkonfilm.work/assets/images/featured/thumbs/img_3461.webp">
</head>

<body>
  <header>
    <h1 class="site-title">
      <a href="../index.html">Sawyer Knox</a>
    </h1>
    <nav>
      <ul class="nav-links">
        <li><a href="../works.html" class="active">Work</a></li>
        <li><a href="../about.html">About</a></li>
        <li><a href="../contact.html">Contact</a></li>
      </ul>
    </nav>
  </header>

  <main>
    <section class="gallery">
      <img src="../assets/images/street/thumbs/000017060001.webp"
  data-full="../assets/images/street/full/000017060001.webp"
  alt="Maui, Hawaii - Winter 2025" width="900" height="597" fetchpriority="high" decoding="async">

      <img src="../assets/images/street/thumbs/000017070023.webp" data-full="../assets/images/street/full/000017070023.webp" alt="Maui, Hawaii - Winter 2025" width="900" height="597" fetchpriority="high" decoding="async">
      <img src="../assets/images/street/thumbs/000017210009.webp" data-full="../assets/images/street/full/000017210009.webp" alt="Maui, Hawaii - Winter 2025" width="900" height="597" fetchpriority="high" decoding="async">
      <img src="../assets/images/street/thumbs/000094770022.webp" data-full="../assets/images/street/full/000094770022.webp" alt="Brighton, England - Autumn 2024" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/000094770035.webp" data-full="../assets/images/street/full/000094770035.webp" alt="London, England - Autumn 2024" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/000094820004.webp" data-full="../assets/images/street/full/000094820004.webp" alt="London, England - Autumn 2024" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/000094820013.webp" data-full="../assets/images/street/full/000094820013.webp" alt="Canon Beach, Oregon - Autumn 2024" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/000094820034.webp" data-full="../assets/images/street/full/000094820034.webp" alt="New York City - Late Summer 2024" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_0457.webp" data-full="../assets/images/street/full/IMG_0457.webp" alt="Florence, Italy - Spring 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_0463.webp" data-full="../assets/images/street/full/IMG_0463.webp" alt="Florence, Italy - Spring 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_0491.webp" data-full="../assets/images/street/full/IMG_0491.webp" alt="Florence, Italy - Spring 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_0501.webp" data-full="../assets/images/street/full/IMG_0501.webp" alt="London, England - Spring 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_0512.webp" data-full="../assets/images/street/full/IMG_0512.webp" alt="Florence, Italy - Spring 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_0544.webp" data-full="../assets/images/street/full/IMG_0544.webp" alt="Florence, Italy - Spring 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_0608.webp" data-full="../assets/images/street/full/IMG_0608.webp" alt="Portland, Oregon - Spring 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_0647.webp" data-full="../assets/images/street/full/IMG_0647.webp" alt="Florence, Italy - Spring 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_1163.webp" data-full="../assets/images/street/full/IMG_1163.webp" alt="Victoria, BC - Summer 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_1169.webp" data-full="../assets/images/street/full/IMG_1169.webp" alt="Victoria, BC - Summer 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_1194.webp" data-full="../assets/images/street/full/IMG_1194.webp" alt="Victoria, BC - Summer 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_1219.webp" data-full="../assets/images/street/full/IMG_1219.webp" alt="Victoria, BC - Summer 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_1723.webp" data-full="../assets/images/street/full/IMG_1723.webp" alt="Portland, Oregon - Summer 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_1760.webp" data-full="../assets/images/street/full/IMG_1760.webp" alt="Portland, Oregon - Summer 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_1762.webp" data-full="../assets/images/street/full/IMG_1762.webp" alt="Portland, Oregon - Summer 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_2438.webp" data-full="../assets/images/street/full/IMG_2438.webp" alt="St. Paul, Oregon - Summer 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_2447.webp" data-full="../assets/images/street/full/IMG_2447.webp" alt="St. Paul, Oregon - Summer 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_2465.webp" data-full="../assets/images/street/full/IMG_2465.webp" alt="St. Paul, Oregon - Summer 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_2469.webp" data-full="../assets/images/street/full/IMG_2469.webp" alt="St. Paul, Oregon - Summer 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_2565.webp" data-full="../assets/images/street/full/IMG_2565.webp" alt="Pickathon, Oregon - Summer 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_2571.webp" data-full="../assets/images/street/full/IMG_2571.webp" alt="Pickathon, Oregon - Summer 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_2617.webp" data-full="../assets/images/street/full/IMG_2617.webp" alt="Long Beach, Washington - Summer 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_2635.webp" data-full="../assets/images/street/full/IMG_2635.webp" alt="Sauvie Island, Oregon - Summer 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_2642.webp" data-full="../assets/images/street/full/IMG_2642.webp" alt="Corvalis, Oregon - Summer 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_2644.webp" data-full="../assets/images/street/full/IMG_2644.webp" alt="Sauvie Island, Oregon - Summer 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_2645.webp" data-full="../assets/images/street/full/IMG_2645.webp" alt="Oregon Coast - Summer 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_2650.webp" data-full="../assets/images/street/full/IMG_2650.webp" alt="Sauvie Island, Oregon - Summer 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_2653.webp" data-full="../assets/images/street/full/IMG_2653.webp" alt="Corvalis, Oregon - Summer 2025" width="900" height="597" loading="lazy" decoding="async">

```


## 7. Appendix: Core Codebase Assets

### style.css
```css

/* === GLOBAL STYLES === */
body {
  margin: 0;
  padding: 0;
  font-family: "Cormorant Garamond", "Georgia", serif;
  background-color: #f9f8f7; /* subtle off-white */
  color: #111;
  line-height: 1.6;
}
/* === GLOBAL IMAGE RENDERING & ANTI-ALIASING === */
img {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  image-rendering: auto; /* ensures smooth photographic rendering */
}


h1, h2, h3, h4 {
  font-weight: 500;
  letter-spacing: 0.5px;
  text-transform: none;
}

/* === HEADER & SITE TITLE === */
.site-title {
  font-family: "Playfair Display", "Cormorant Garamond", serif;
  font-size: 2.6rem;
  font-weight: 500;
  text-align: center;
  margin: 1.5rem 0 1rem 0;
}

.site-title a {
  text-decoration: none;
  color: #111;
  transition: color 0.3s ease;
}

.site-title a:hover {
  color: #777;
}



/* === NAVIGATION === */
nav {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0.5rem 0 1rem 0;
  border: none; /* remove bottom border for seamless look */
  background: #f9f8f7;
}

.nav-links {
  list-style: none;
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin: 0;
  padding: 0;
}

.nav-links a {
  text-decoration: none;
  color: #111;
  font-size: 1.15rem;
  font-family: "Cormorant Garamond", serif;
  transition: color 0.3s ease;
}

.nav-links a:hover {
  color: #777;
}
/* Dropdown menu */
.dropdown {
  display: none;
  position: absolute;
  top: 1.8rem;
  left: 0;
  background-color: #fff;
  border: 1px solid #eee;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  list-style: none;
  padding: 0.5rem 0;
  min-width: 150px;
  z-index: 10;
}

.dropdown li {
  padding: 0.4rem 1rem;
}

.dropdown li a {
  color: #111;
  text-decoration: none;
}

.dropdown li a:hover {
  color: #777;
}

.nav-item:hover .dropdown {
  display: block;
}

/* === HOME PAGE GALLERY (3 COLUMNS ON DESKTOP, 2 ON MOBILE) === */
.gallery {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0;
  padding: 1rem;
  margin: 3rem auto;
  max-width: 1500px;
}

.gallery img {
  width: 100%;
  height: auto;
  object-fit: cover;
  display: block;
  image-rendering: auto;
}
/* === HOME PAGE ONLY: Force uniform 3:2 boxes for featured images === */
.index-page .gallery img {
  height: 100%;
  aspect-ratio: 3 / 2;
  object-fit: cover;
}
/* Force 2 columns on mobile ONLY for the home page */
@media (max-width: 768px) {
  body.index-page .gallery {
    grid-template-columns: repeat(2, 1fr);
  }
}




/* === RESPONSIVE === */
@media (max-width: 768px) {
  .nav-links {
    flex-direction: column;
    gap: 1rem;
  }

  .dropdown {
    position: static;
    box-shadow: none;
    border: none;
  }
}


/* === WORKS PAGE GRID (Crisp uniform 2Ã—2 layout) === */
.works-gallery {
  display: grid;
  grid-template-columns: repeat(2, 1fr); /* 2 columns always */
  gap: 0.75rem;
  max-width: 1100px;
  margin: 3rem auto;
  padding: 0 1rem;
}

.work-category {
  position: relative;
  overflow: hidden;
  aspect-ratio: 3 / 2; /* every tile same horizontal shape */
}

.work-category a {
  display: block;
  width: 100%;
  height: 100%;
}

.work-category img {
  width: 100%;
  height: 100%;
  object-fit: cover;        /* fills box neatly */
  object-position: center;  /* centers subject */
  image-rendering: auto;    /* smooth high-res scaling */
  display: block;
  transition: filter 0.3s ease, transform 0.3s ease;
}
/* Make the Vertical category image show the top portion within its horizontal frame */
.work-category.vertical img {
  object-fit: cover;
  object-position: top;
}


/* Overlay styling */
.work-category .overlay {
  position: absolute;
  inset: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  font-size: 1.8rem;
  font-family: "Playfair Display", serif;
  opacity: 0;
  background-color: rgba(0, 0, 0, 0);
  transition: background-color 0.3s ease, opacity 0.3s ease;
}

/* Desktop hover effect */
@media (hover: hover) and (pointer: fine) {
  .work-category:hover img {
    filter: brightness(0.6);
    transform: scale(1.02);
  }

  .work-category:hover .overlay {
    opacity: 1;
    background-color: rgba(0, 0, 0, 0.4);
  }
}

/* Mobile â€“ labels always visible */
@media (hover: none) and (pointer: coarse) {
  .work-category .overlay {
    opacity: 1;
    background-color: rgba(0, 0, 0, 0.25);
  }
  .work-category .overlay span {
    font-size: 1.2rem;
  }
}

/* Works page â€“ keep 2Ã—2 on mobile too */
@media (max-width: 768px) {
  .works-gallery {
    grid-template-columns: repeat(2, 1fr);
  }
  
  /* Force category labels to show on small screens (reliable mobile fallback) */
@media (max-width: 900px) {
  .work-category .overlay {
    opacity: 1;
    background-color: rgba(0, 0, 0, 0.28);
  }

  .work-category .overlay span {
    font-size: 1.2rem;
  }
}

}





/* === ACTIVE PAGE HIGHLIGHT === */
.nav-links a.active {
  font-weight: 500;           /* slightly bolder text */
  color: #333;                /* a bit darker */
  border-bottom: 1px solid #333; /* thin underline for subtle emphasis */
}

/* === CATEGORY PAGES (Street, Scenes, Color, Vertical) === */
body:not(.index-page) .gallery {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
}

@media (max-width: 768px) {
  body:not(.index-page) .gallery {
    grid-template-columns: 1fr; /* 1 column only on mobile */
  }
}

/* === ABOUT PAGE (Matches Home Gallery Layout) === */
.about-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem 4rem 1rem;
  text-align: center;
  font-family: "Cormorant Garamond", serif;
  color: #222;
  line-height: 1.6;
}

/* Text block */
.about-text h2 {
  font-family: "Playfair Display", serif;
  font-size: 1.8rem;
  margin-bottom: 1rem;
}

.about-text p {
  font-size: 1.05rem;
  margin: 0 auto 2.5rem auto;
  max-width: 600px;
}

/* Self-portrait gallery (same behavior as home) */
.about-gallery {
  display: grid;
  grid-template-columns: repeat(2, 1fr);  /* 2x2 desktop */
  gap: 0;
  padding: 1rem;
  margin: 0 auto;
  max-width: 1000px;
}

.about-gallery img {
  width: 100%;
  height: auto;
  object-fit: cover;
  display: block;
  image-rendering: auto;
}

/* On mobile: 1 column per row */
@media (max-width: 768px) {
  .about-gallery {
    grid-template-columns: 1fr;
  }
}

/* === CONTACT PAGE === */
.contact-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 3rem 1rem 5rem 1rem;
  text-align: center;
  font-family: "Cormorant Garamond", serif;
  color: #222;
  line-height: 1.6;
}

.contact-text h2 {
  font-family: "Playfair Display", serif;
  font-size: 1.8rem;
  margin-bottom: 1rem;
}

.contact-text p {
  font-size: 1.05rem;
  margin: 0 auto 2.5rem auto;
  max-width: 600px;
  color: #222;
}

.contact-links {
  display: inline-block;
  text-align: left;
}

.contact-links p {
  margin: 0.5rem 0;
  font-size: 1.05rem;
}

/* Neutral minimalist link style */
.contact-links a {
  color: #444;
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: color 0.3s ease, border-color 0.3s ease;
}

.contact-links a:hover {
  color: #000;
  border-color: #000;
}

strong {
  font-weight: 500;
  color: #000;
}
  /* === LIGHTBOX (full-screen image viewer) === */
.lightbox {
  position: fixed;
  inset: 0;
  background: rgba(10, 10, 10, 0.92);
  display: none;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 1rem;
}

.lightbox.is-open {
  display: flex;
}

body.lightbox-open {
  overflow: hidden;
  touch-action: none;
}

.lightbox__figure {
  margin: 0;
  max-width: 96vw;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

.lightbox__img {
  max-width: 96vw;
  max-height: 86vh;
  width: auto;
  height: auto;
  object-fit: contain;
  display: block;
  box-shadow: 0 10px 40px rgba(0,0,0,0.35);
}

.lightbox__caption {
  color: rgba(255,255,255,0.8);
  font-size: 0.95rem;
  text-align: center;
  max-width: 80ch;
}

.lightbox__close,
.lightbox__prev,
.lightbox__next {
  position: absolute;
  border: none;
  background: rgba(255,255,255,0.08);
  color: #fff;
  cursor: pointer;
  border-radius: 999px;
  padding: 0.6rem 0.9rem;
  line-height: 1;
  transition: background 0.2s ease;
  user-select: none;
}

.lightbox__close:hover,
.lightbox__prev:hover,
.lightbox__next:hover {
  background: rgba(255,255,255,0.16);
}

.lightbox__close {
  top: 1rem;
  right: 1rem;
  font-size: 1.6rem;
}

.lightbox__prev,
.lightbox__next {
  top: 50%;
  transform: translateY(-50%);
  font-size: 2rem;
}

.lightbox__prev { left: 1rem; }
.lightbox__next { right: 1rem; }

/* Make arrows less intrusive on small screens */
@media (max-width: 768px) {
  .lightbox__prev,
  .lightbox__next {
    padding: 0.45rem 0.7rem;
    font-size: 1.6rem;
  }
}

.gallery img {
  background: #f1f1f1;
}

/* === FOOTER STYLES === */
footer {
  padding: 2rem 5%;
  margin-top: 4rem;
}

.footer-content {
  display: flex;
  justify-content: space-between; /* Pushes copyright left, Instagram right */
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  border-top: 1px solid #eaeaea; /* Adds a clean, subtle separator line */
  padding-top: 1.5rem;
}

.footer-content p, 
.footer-content a {
  margin: 0;
  color: #555;
  text-decoration: none;
  font-size: 1rem;
  letter-spacing: 0.05em;
}

.footer-content a:hover {
  color: #000;
  text-decoration: underline;
}


```
### Lightbox.js
```javascript
// lightbox.js
(() => {
  const imgs = Array.from(document.querySelectorAll(".gallery img"));
  if (!imgs.length) return;

  // Build overlay once
  const overlay = document.createElement("div");
  overlay.className = "lightbox";
  overlay.innerHTML = `
    <button class="lightbox__close" aria-label="Close (Esc)">&times;</button>
    <button class="lightbox__prev" aria-label="Previous (Left arrow)">&lsaquo;</button>
    <figure class="lightbox__figure" aria-live="polite">
      <img class="lightbox__img" alt="">
      <figcaption class="lightbox__caption"></figcaption>
    </figure>
    <button class="lightbox__next" aria-label="Next (Right arrow)">&rsaquo;</button>
  `;
  document.body.appendChild(overlay);

  const lbImg = overlay.querySelector(".lightbox__img");
  const caption = overlay.querySelector(".lightbox__caption");
  const btnClose = overlay.querySelector(".lightbox__close");
  const btnPrev = overlay.querySelector(".lightbox__prev");
  const btnNext = overlay.querySelector(".lightbox__next");

  let index = 0;
  let startX = 0;
  let startY = 0;

  const setBodyScroll = (locked) => {
    document.body.classList.toggle("lightbox-open", locked);
  };

  const show = (i) => {
    index = (i + imgs.length) % imgs.length;
    const img = imgs[index];

    // Use current src; if you ever want separate full-res, add data-full and swap here.
    lbImg.src = img.dataset.full || img.currentSrc || img.src;
    lbImg.alt = img.alt || "";
    caption.textContent = img.alt || "";
  };

  const open = (i) => {
    overlay.classList.add("is-open");
    setBodyScroll(true);
    show(i);
  };

  const close = () => {
    overlay.classList.remove("is-open");
    setBodyScroll(false);
    // Optional: clear src so it unloads
    lbImg.src = "";
  };

  const next = () => show(index + 1);
  const prev = () => show(index - 1);

  // Click on gallery opens lightbox
  imgs.forEach((img, i) => {
    img.style.cursor = "zoom-in";
    img.addEventListener("click", () => open(i));
  });

  // Buttons
  btnClose.addEventListener("click", close);
  btnNext.addEventListener("click", (e) => { e.stopPropagation(); next(); });
  btnPrev.addEventListener("click", (e) => { e.stopPropagation(); prev(); });

  // Click outside image closes
  overlay.addEventListener("click", (e) => {
    if (e.target === overlay) close();
  });

  // Keyboard
  document.addEventListener("keydown", (e) => {
    if (!overlay.classList.contains("is-open")) return;
    if (e.key === "Escape") close();
    if (e.key === "ArrowRight") next();
    if (e.key === "ArrowLeft") prev();
  });

  // Swipe (mobile)
  overlay.addEventListener("touchstart", (e) => {
    if (!overlay.classList.contains("is-open")) return;
    const t = e.touches[0];
    startX = t.clientX;
    startY = t.clientY;
  }, { passive: true });

  overlay.addEventListener("touchend", (e) => {
    if (!overlay.classList.contains("is-open")) return;
    const t = e.changedTouches[0];
    const dx = t.clientX - startX;
    const dy = t.clientY - startY;

    // Ignore mostly-vertical gestures
    if (Math.abs(dy) > Math.abs(dx)) return;

    if (dx < -40) next();
    if (dx > 40) prev();
  }, { passive: true });
})();

```
### Structural Sample: pages\street.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Street | Sawyer Knox</title>
  <meta name="description" content="Explore Sawyer Knox's 35mm film street photography. Candid, authentic moments captured on black and white HP5 film from Portland, Oregon, and around the world.">
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500&family=Playfair+Display:wght@500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../style.css?v=7">
  
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://sjkonfilm.work/pages/street.html">
  <meta property="og:title" content="Street Photography | Sawyer Knox">
  <meta property="og:description" content="Candid, authentic street photography captured on 35mm film.">
  <meta property="og:image" content="https://sjkonfilm.work/assets/images/featured/thumbs/img_3461.webp">
</head>

<body>
  <header>
    <h1 class="site-title">
      <a href="../index.html">Sawyer Knox</a>
    </h1>
    <nav>
      <ul class="nav-links">
        <li><a href="../works.html" class="active">Work</a></li>
        <li><a href="../about.html">About</a></li>
        <li><a href="../contact.html">Contact</a></li>
      </ul>
    </nav>
  </header>

  <main>
    <section class="gallery">
      <img src="../assets/images/street/thumbs/000017060001.webp"
  data-full="../assets/images/street/full/000017060001.webp"
  alt="Maui, Hawaii - Winter 2025" width="900" height="597" fetchpriority="high" decoding="async">

      <img src="../assets/images/street/thumbs/000017070023.webp" data-full="../assets/images/street/full/000017070023.webp" alt="Maui, Hawaii - Winter 2025" width="900" height="597" fetchpriority="high" decoding="async">
      <img src="../assets/images/street/thumbs/000017210009.webp" data-full="../assets/images/street/full/000017210009.webp" alt="Maui, Hawaii - Winter 2025" width="900" height="597" fetchpriority="high" decoding="async">
      <img src="../assets/images/street/thumbs/000094770022.webp" data-full="../assets/images/street/full/000094770022.webp" alt="Brighton, England - Autumn 2024" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/000094770035.webp" data-full="../assets/images/street/full/000094770035.webp" alt="London, England - Autumn 2024" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/000094820004.webp" data-full="../assets/images/street/full/000094820004.webp" alt="London, England - Autumn 2024" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/000094820013.webp" data-full="../assets/images/street/full/000094820013.webp" alt="Canon Beach, Oregon - Autumn 2024" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/000094820034.webp" data-full="../assets/images/street/full/000094820034.webp" alt="New York City - Late Summer 2024" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_0457.webp" data-full="../assets/images/street/full/IMG_0457.webp" alt="Florence, Italy - Spring 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_0463.webp" data-full="../assets/images/street/full/IMG_0463.webp" alt="Florence, Italy - Spring 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_0491.webp" data-full="../assets/images/street/full/IMG_0491.webp" alt="Florence, Italy - Spring 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_0501.webp" data-full="../assets/images/street/full/IMG_0501.webp" alt="London, England - Spring 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_0512.webp" data-full="../assets/images/street/full/IMG_0512.webp" alt="Florence, Italy - Spring 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_0544.webp" data-full="../assets/images/street/full/IMG_0544.webp" alt="Florence, Italy - Spring 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_0608.webp" data-full="../assets/images/street/full/IMG_0608.webp" alt="Portland, Oregon - Spring 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_0647.webp" data-full="../assets/images/street/full/IMG_0647.webp" alt="Florence, Italy - Spring 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_1163.webp" data-full="../assets/images/street/full/IMG_1163.webp" alt="Victoria, BC - Summer 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_1169.webp" data-full="../assets/images/street/full/IMG_1169.webp" alt="Victoria, BC - Summer 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_1194.webp" data-full="../assets/images/street/full/IMG_1194.webp" alt="Victoria, BC - Summer 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_1219.webp" data-full="../assets/images/street/full/IMG_1219.webp" alt="Victoria, BC - Summer 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_1723.webp" data-full="../assets/images/street/full/IMG_1723.webp" alt="Portland, Oregon - Summer 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_1760.webp" data-full="../assets/images/street/full/IMG_1760.webp" alt="Portland, Oregon - Summer 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_1762.webp" data-full="../assets/images/street/full/IMG_1762.webp" alt="Portland, Oregon - Summer 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_2438.webp" data-full="../assets/images/street/full/IMG_2438.webp" alt="St. Paul, Oregon - Summer 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_2447.webp" data-full="../assets/images/street/full/IMG_2447.webp" alt="St. Paul, Oregon - Summer 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_2465.webp" data-full="../assets/images/street/full/IMG_2465.webp" alt="St. Paul, Oregon - Summer 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_2469.webp" data-full="../assets/images/street/full/IMG_2469.webp" alt="St. Paul, Oregon - Summer 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_2565.webp" data-full="../assets/images/street/full/IMG_2565.webp" alt="Pickathon, Oregon - Summer 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_2571.webp" data-full="../assets/images/street/full/IMG_2571.webp" alt="Pickathon, Oregon - Summer 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_2617.webp" data-full="../assets/images/street/full/IMG_2617.webp" alt="Long Beach, Washington - Summer 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_2635.webp" data-full="../assets/images/street/full/IMG_2635.webp" alt="Sauvie Island, Oregon - Summer 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_2642.webp" data-full="../assets/images/street/full/IMG_2642.webp" alt="Corvalis, Oregon - Summer 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_2644.webp" data-full="../assets/images/street/full/IMG_2644.webp" alt="Sauvie Island, Oregon - Summer 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_2645.webp" data-full="../assets/images/street/full/IMG_2645.webp" alt="Oregon Coast - Summer 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_2650.webp" data-full="../assets/images/street/full/IMG_2650.webp" alt="Sauvie Island, Oregon - Summer 2025" width="900" height="597" loading="lazy" decoding="async">
      <img src="../assets/images/street/thumbs/IMG_2653.webp" data-full="../assets/images/street/full/IMG_2653.webp" alt="Corvalis, Oregon - Summer 2025" width="900" height="597" loading="lazy" decoding="async">
```
