/* =========================================================
   WIZE · interactions légères, sans dépendance.
   - menu mobile
   - bordure de l'en-tête après défilement (IntersectionObserver)
   - apparition des sections au défilement
   ========================================================= */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.add("js");

  /* Menu mobile */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("nav");
  function setMenu(open) {
    if (!toggle || !nav) return;
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    nav.classList.toggle("is-open", open);
  }
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      setMenu(toggle.getAttribute("aria-expanded") !== "true");
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) setMenu(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") setMenu(false);
    });
    window.matchMedia("(min-width: 861px)").addEventListener("change", function (m) {
      if (m.matches) setMenu(false);
    });
  }

  /* En-tête : bordure dès que la page a défilé */
  var header = document.querySelector(".site-header");
  var sentinel = document.querySelector(".top-sentinel");
  if ("IntersectionObserver" in window && header && sentinel) {
    new IntersectionObserver(function (entries) {
      header.classList.toggle("is-scrolled", !entries[0].isIntersecting);
    }).observe(sentinel);
  }

  /* Apparition au défilement */
  var items = document.querySelectorAll(".reveal");
  if (!("IntersectionObserver" in window)) {
    items.forEach(function (el) { el.classList.add("is-in"); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-in");
        io.unobserve(entry.target);
      }
    });
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.12 });
  items.forEach(function (el) { io.observe(el); });
})();
