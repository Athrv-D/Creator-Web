const form = document.getElementById("leadForm");
const statusBox = document.getElementById("formStatus");
const submitButton = form.querySelector("button[type='submit']");
const menuToggle = document.getElementById("menuToggle");
const nav = document.getElementById("nav");

document.getElementById("year").textContent = new Date().getFullYear();

menuToggle.addEventListener("click", () => {
  const open = nav.classList.toggle("open");
  menuToggle.setAttribute("aria-expanded", String(open));
  menuToggle.setAttribute("aria-label", open ? "Close navigation" : "Open navigation");
});

nav.querySelectorAll("a").forEach((link) => link.addEventListener("click", () => {
  nav.classList.remove("open");
  menuToggle.setAttribute("aria-expanded", "false");
}));

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  statusBox.textContent = "";
  statusBox.className = "form-status";
  if (!form.reportValidity()) return;

  const payload = Object.fromEntries(new FormData(form).entries());
  submitButton.disabled = true;
  submitButton.querySelector("span:first-child").textContent = "Sending…";

  try {
    const response = await fetch("/api/leads", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const result = await response.json();
    if (!response.ok) {
      const detail = Array.isArray(result.detail) ? result.detail.map((item) => item.msg).join(" ") : result.detail;
      throw new Error(detail || "Unable to submit your request. Please try again.");
    }
    statusBox.textContent = "Your request has been received. We'll be in touch soon.";
    statusBox.classList.add("success");
    form.reset();
  } catch (error) {
    statusBox.textContent = error.message || "Something went wrong. Please try again.";
    statusBox.classList.add("error");
  } finally {
    submitButton.disabled = false;
    submitButton.querySelector("span:first-child").textContent = "Send me the demo";
  }
});