document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector(".menu-toggle");
  const nav = document.querySelector(".nav-links");
  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const isOpen = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(isOpen));
    });
  }

  document.querySelectorAll(".flash").forEach((message) => {
    window.setTimeout(() => {
      message.classList.add("flash-hide");
      window.setTimeout(() => message.remove(), 350);
    }, 4500);
  });

  document.querySelectorAll('input[type="number"]').forEach((input) => {
    input.addEventListener("change", () => {
      const min = Number(input.min || 0);
      const max = Number(input.max || 99);
      let value = Number(input.value);
      if (!Number.isFinite(value)) value = min;
      input.value = Math.max(min, Math.min(max, Math.trunc(value)));
    });
  });
});
