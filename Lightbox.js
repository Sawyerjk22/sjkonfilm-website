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

  const imgs = Array.from(document.querySelectorAll(".gallery img[data-full]"));
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
      <div class="lightbox__print-info"></div>
    </figure>
    <button class="lightbox__next" aria-label="Next (Right arrow)">&rsaquo;</button>
  `;
  document.body.appendChild(overlay);

  const lbImg = overlay.querySelector(".lightbox__img");
  const caption = overlay.querySelector(".lightbox__caption");
  const printContainer = overlay.querySelector(".lightbox__print-info");
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
      .replace(/\s*-\s*(?:35mm|120)?\s*Film Photography/gi, "")
      .replace(/\s*-\s*Sawyer Knox/gi, "")
      .trim();
    caption.textContent = cleanCaption;

    // Render Subtle Archival Print Inquiry Link (Path A)
    const isSubpage = window.location.pathname.includes("/pages/");
    const contactPath = isSubpage ? "../contact.html" : "contact.html";
    const photoTitle = encodeURIComponent(cleanCaption || img.alt || "Film Photograph");
    const inquireUrl = `${contactPath}?inquiry=print&photo=${photoTitle}`;
    
    // Always render subtle, understated inquiry link
    printContainer.innerHTML = `
      <a href="${inquireUrl}" class="lightbox__print-inquiry">Inquire about an archival print &rarr;</a>
    `;

    // Silently preload NEXT image
    const nextIndex = (index + 1) % imgs.length;
    const nextImg = imgs[nextIndex];
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
  };

  const next = () => show(index + 1);
  const prev = () => show(index - 1);

  imgs.forEach((img, i) => {
    img.style.cursor = "zoom-in";
    img.addEventListener("click", () => open(i));
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
