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
    lbImg.src = img.currentSrc || img.src;
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
