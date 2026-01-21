// lazyload.js
(() => {
  const imgs = Array.from(document.querySelectorAll(".gallery img"));

  // If the browser supports native lazy-loading well, still keep this
  // But we will also do IO-based swapping to be safe on iOS.
  imgs.forEach((img) => {
    // If already set up, skip
    if (img.dataset.src) return;

    // Move current src into data-src and load a tiny placeholder immediately
    img.dataset.src = img.getAttribute("src");
    img.setAttribute(
      "src",
      "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw=="
    );
  });

  // IntersectionObserver: load when near viewport
  if (!("IntersectionObserver" in window)) {
    // Fallback: just load everything
    imgs.forEach((img) => {
      if (img.dataset.src) img.src = img.dataset.src;
    });
    return;
  }

  const io = new IntersectionObserver(
    (entries, obs) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;

        const img = entry.target;
        if (img.dataset.src) {
          img.src = img.dataset.src;
          delete img.dataset.src;
        }
        obs.unobserve(img);
      });
    },
    {
      // Start loading a bit before the user sees it
      rootMargin: "600px 0px",
      threshold: 0.01,
    }
  );

  imgs.forEach((img) => io.observe(img));
})();
