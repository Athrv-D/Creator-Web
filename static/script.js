const form = document.getElementById("leadForm");
const statusBox = document.getElementById("formStatus");
const submitButton = form.querySelector("button[type='submit']");
const menuToggle = document.getElementById("menuToggle");
const nav = document.getElementById("nav");

document.getElementById("year").textContent = new Date().getFullYear();

menuToggle.addEventListener("click", () => {
  const isOpen = nav.classList.toggle("open");
  menuToggle.setAttribute("aria-expanded", String(isOpen));
  menuToggle.setAttribute("aria-label", isOpen ? "Close navigation" : "Open navigation");
});

nav.querySelectorAll("a").forEach(link => {
  link.addEventListener("click", () => {
    nav.classList.remove("open");
    menuToggle.setAttribute("aria-expanded", "false");
  });
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  statusBox.textContent = "";
  statusBox.className = "form-status";

  if (!form.reportValidity()) return;

  const formData = new FormData(form);
  const payload = Object.fromEntries(formData.entries());

  submitButton.disabled = true;
  submitButton.querySelector("span:first-child").textContent = "Sending request…";

  try {
    const response = await fetch("/api/leads", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.detail || "We couldn't submit your request. Please try again.");
    }

    statusBox.textContent = "Thanks! Your request has been received. We'll follow up by email.";
    statusBox.classList.add("success");
    form.reset();
  } catch (error) {
    statusBox.textContent = error.message || "Something went wrong. Please try again.";
    statusBox.classList.add("error");
  } finally {
    submitButton.disabled = false;
    submitButton.querySelector("span:first-child").textContent = "Send my demo request";
  }
});
