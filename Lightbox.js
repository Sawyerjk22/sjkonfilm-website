(() => {
  // Direct Mobile Traffic Tracker (Business Card Conversion Proxy)
  if (!sessionStorage.getItem("sjkonfilm_visited")) {
    sessionStorage.setItem("sjkonfilm_visited", "true");
    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    const isDirect = document.referrer === "" || document.referrer.indexOf(location.hostname) !== -1;
    if (isMobile && isDirect) {
      let mobileDirectHits = parseInt(localStorage.getItem("sjkonfilm_direct_mobile_hits") || "0", 10);
      localStorage.setItem("sjkonfilm_direct_mobile_hits", (mobileDirectHits + 1).toString());
    }
  }

  // Do not activate Lightbox on landing page (index-page)
  if (document.body.classList.contains("index-page")) return;

  const allImgs = Array.from(document.querySelectorAll(".gallery img[data-full]"));
  if (!allImgs.length) return;

  let activeImgs = allImgs;

  const getSlug = (img) => {
    const src = img.dataset.full || img.getAttribute("src") || "";
    const base = src.split("/").pop() || "";
    return base.replace(/\.(webp|avif|jpe?g|png)$/i, "").replace(/-400w$/i, "");
  };

  allImgs.forEach((img) => {
    const slug = getSlug(img);
    if (slug && !img.id) {
      img.id = slug;
    }
  });

  // Build overlay once
  const overlay = document.createElement("div");
  overlay.className = "lightbox";
  overlay.innerHTML = `
    <button class="lightbox__close" aria-label="Close (Esc)">&times;</button>
    <button class="lightbox__prev" aria-label="Previous (Left arrow)">&lsaquo;</button>
    <figure class="lightbox__figure" aria-live="polite">
      <img class="lightbox__img" alt="">
      <figcaption class="lightbox__caption">
        <div class="lightbox__caption-text"></div>
        <div class="lightbox__meta-links">
          <a href="https://www.instagram.com/sawyer.j.knox" target="_blank" rel="me noopener noreferrer">@sawyer.j.knox</a>
          <span class="lightbox__sep">&middot;</span>
          <a class="lightbox__print-link" href="/contact.html">Print Inquiry</a>
        </div>
      </figcaption>
    </figure>
    <button class="lightbox__next" aria-label="Next (Right arrow)">&rsaquo;</button>
  `;
  document.body.appendChild(overlay);

  const lbImg = overlay.querySelector(".lightbox__img");
  const captionText = overlay.querySelector(".lightbox__caption-text");
  const printLink = overlay.querySelector(".lightbox__print-link");
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
    if (!activeImgs.length) return;
    index = (i + activeImgs.length) % activeImgs.length;
    const img = activeImgs[index];

    const targetSrc = img.dataset.full || img.currentSrc || img.src;
    
    // Smooth image load transition
    if (lbImg.src !== targetSrc) {
      lbImg.style.opacity = "0.2";
      lbImg.onload = () => {
        lbImg.style.opacity = "1";
      };
      lbImg.src = targetSrc;
    } else {
      lbImg.style.opacity = "1";
    }
    lbImg.alt = img.alt || "";

    // Clean up caption for human display while preserving rich HTML alt tags for Google SEO
    const rawCaption = img.dataset.caption || img.alt || "";
    const cleanCaption = rawCaption
      .replace(/\s*-\s*(?:35mm|120)?(?:\s*Black\s*&\s*White|\s*Color|\s*Medium\s*Format)?\s*Film Photography/gi, "")
      .replace(/\s*-\s*Sawyer Knox/gi, "")
      .trim();
    captionText.textContent = cleanCaption;

    const slug = getSlug(img);
    const photoRef = cleanCaption ? `${cleanCaption} (${slug})` : slug;
    if (printLink) {
      printLink.href = `/contact.html?inquiry=print&photo=${encodeURIComponent(photoRef)}`;
    }

    if (slug && overlay.classList.contains("is-open")) {
      window.history.replaceState(null, "", `#${slug}`);
    }

    // Silently preload NEXT image
    const nextIndex = (index + 1) % activeImgs.length;
    const nextImg = activeImgs[nextIndex];
    const preload = new Image();
    preload.src = nextImg.dataset.full || nextImg.currentSrc || nextImg.src;
  };

  const open = (i) => {
    overlay.classList.add("is-open");
    setBodyScroll(true);
    show(i);
  };

  const close = () => {
    overlay.classList.remove("is-open");
    setBodyScroll(false);
    lbImg.src = "";
    lbImg.style.opacity = "0";
    if (window.location.hash) {
      window.history.replaceState(null, "", window.location.pathname + window.location.search);
    }
  };

  const next = () => show(index + 1);
  const prev = () => show(index - 1);

  allImgs.forEach((img) => {
    img.style.cursor = "zoom-in";
    img.addEventListener("click", () => {
      const visible = allImgs.filter(el => !el.classList.contains("is-filtered-out") && el.offsetParent !== null);
      activeImgs = visible.length ? visible : allImgs;
      const clickedIdx = activeImgs.indexOf(img);
      open(clickedIdx >= 0 ? clickedIdx : 0);
    });
  });

  btnClose.addEventListener("click", close);
  btnNext.addEventListener("click", (e) => { e.stopPropagation(); next(); });
  btnPrev.addEventListener("click", (e) => { e.stopPropagation(); prev(); });

  overlay.addEventListener("click", (e) => {
    if (e.target === overlay) close();
  });

  document.addEventListener("keydown", (e) => {
    if (!overlay.classList.contains("is-open")) return;
    if (e.key === "Escape") close();
    if (e.key === "ArrowRight") next();
    if (e.key === "ArrowLeft") prev();
  });

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

    if (Math.abs(dy) > Math.abs(dx)) return;
    if (dx < -40) next();
    if (dx > 40) prev();
  }, { passive: true });

  // Deep-link support (e.g. from Pinterest RSS or direct shared links: #photo-slug)
  const openFromHash = () => {
    const rawHash = window.location.hash ? decodeURIComponent(window.location.hash.slice(1)).trim() : "";
    if (!rawHash) return;
    const targetImg = allImgs.find((img) => getSlug(img).toLowerCase() === rawHash.toLowerCase());
    if (!targetImg) return;

    const tone = targetImg.getAttribute("data-tone");
    if (tone && targetImg.classList.contains("is-filtered-out")) {
      const filterBtn = document.querySelector(`.text-nav-btn[data-filter="${tone}"]`);
      if (filterBtn) filterBtn.click();
    }

    const visible = allImgs.filter((el) => !el.classList.contains("is-filtered-out") && el.offsetParent !== null);
    activeImgs = visible.length ? visible : allImgs;
    const idx = activeImgs.indexOf(targetImg);
    if (idx >= 0) {
      open(idx);
    }
  };

  if (document.readyState === "complete" || document.readyState === "interactive") {
    setTimeout(openFromHash, 50);
  } else {
    window.addEventListener("DOMContentLoaded", () => setTimeout(openFromHash, 50));
  }
})();

// Automatic Glass Badge Initializer
document.addEventListener("DOMContentLoaded", () => {
  const badge = document.querySelector(".glass-badge");
  if (badge) {
    badge.addEventListener("click", (e) => e.stopPropagation());
    setTimeout(() => {
      badge.classList.add("fade-in");
    }, 5000);
  }
});
