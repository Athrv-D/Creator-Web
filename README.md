# Atharv Gupta — Website Demo Request Landing Page

A responsive landing page built with HTML, CSS and vanilla JavaScript, backed by FastAPI and SQLite.

## Features
- Responsive desktop, tablet and mobile layout
- Hero section with the supplied portrait
- Benefits, considerations and three-step process sections
- Demo request form with name, email, content category and website purpose
- Server-side validation and SQLite lead storage
- Optional SMTP notification to your inbox
- Basic honeypot field for simple bot filtering

## Run locally

1. Open a terminal in this project folder.
2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   # Windows:
   .venv\\Scripts\\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the server:

   ```bash
   uvicorn main:app --reload
   ```

5. Open http://127.0.0.1:8000

## Enable email notifications

1. Copy `.env.example` to `.env`.
2. Set `LEADS_TO_EMAIL`, `EMAIL_FROM`, `SMTP_HOST`, `SMTP_PORT`, `SMTP_USERNAME` and `SMTP_PASSWORD`.
3. Restart the server.

For Gmail, use a Google App Password (with 2-Step Verification enabled), not your normal account password. For production, use a dedicated transactional email provider and store secrets in your hosting provider's environment settings.

If SMTP is not configured, requests are still saved in `leads.db`; email notification is simply skipped.

## View saved leads

The SQLite database `leads.db` is created automatically. You can inspect it using DB Browser for SQLite or the `sqlite3` command-line tool.

## Important before launch
- Replace the demo copy/contact details with your final business details.
- Configure SMTP and test delivery.
- Add a privacy policy and consent text appropriate to your location and use case.
- Deploy behind HTTPS.
- Add production-grade rate limiting, spam protection (such as Turnstile), logging and database backups.
- The form requests a demo; it does not automatically generate a custom website demo. You review the lead and send the personalized demo or follow-up yourself.
