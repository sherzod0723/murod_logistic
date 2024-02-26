const sidebar = document.querySelector(".prt_sidebar"),
  hamburger = document.querySelector(".prt_mb_hamburger"),
  overlay = document.querySelector(".overlay"),
  title = document.querySelector(".title");

hamburger.addEventListener("click", () => {
  sidebar.classList.toggle("sidebar_active");
  overlay.classList.add("overlay_active");
  title.style.zIndex = 0;
});

overlay.addEventListener("click", () => {
  sidebar.classList.toggle("sidebar_active");
  overlay.classList.toggle("overlay_active");
  title.style.zIndex = 1;
});
