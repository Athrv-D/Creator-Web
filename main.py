import os
import re
import sqlite3
import smtplib
from email.message import EmailMessage
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr, Field

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = os.getenv("DATABASE_PATH", str(BASE_DIR / "leads.db"))

app = FastAPI(title="Atharv Gupta — Website Demo Requests")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                category TEXT NOT NULL,
                website_for TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)


init_db()


class LeadRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    category: Literal[
        "Entertainment", "Lifestyle", "Fashion", "Fitness & Health",
        "Travel", "Food & Cooking", "Education", "Technology", "Gaming",
        "Beauty", "Music", "Sports", "Business & Entrepreneurship", "Other"
    ]
    website_for: Literal["Personal Brand", "Business", "Both"]
    website: str = ""  # Honeypot field; should remain empty.


def send_email(to_address: str, subject: str, body: str):
    host = os.getenv("SMTP_HOST")
    username = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")
    sender = os.getenv("EMAIL_FROM", username or "")
    port = int(os.getenv("SMTP_PORT", "587"))

    if not all([host, username, password, sender]):
        return False

    message = EmailMessage()
    message["From"] = sender
    message["To"] = to_address
    message["Subject"] = subject
    message.set_content(body)

    with smtplib.SMTP(host, port, timeout=15) as server:
        server.starttls()
        server.login(username, password)
        server.send_message(message)
    return True


@app.get("/")
def homepage():
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.post("/api/leads", status_code=201)
def create_lead(lead: LeadRequest, request: Request):
    # Basic bot trap. Real visitors never see or fill this field.
    if lead.website.strip():
        raise HTTPException(status_code=400, detail="Invalid submission.")

    name = re.sub(r"\s+", " ", lead.name).strip()
    email = str(lead.email).strip().lower()

    with get_connection() as conn:
        cursor = conn.execute(
            """INSERT INTO leads (name, email, category, website_for)
               VALUES (?, ?, ?, ?)""",
            (name, email, lead.category, lead.website_for),
        )
        lead_id = cursor.lastrowid

    owner_email = os.getenv("LEADS_TO_EMAIL")
    email_status = "not_configured"

    if owner_email:
        body = (
            f"New website demo request (#{lead_id})\n\n"
            f"Name: {name}\nEmail: {email}\n"
            f"Content category: {lead.category}\n"
            f"Website for: {lead.website_for}\n"
        )
        try:
            sent = send_email(owner_email, f"New website demo request from {name}", body)
            email_status = "sent" if sent else "smtp_not_configured"
        except Exception:
            # Keep the lead saved even if email delivery is temporarily unavailable.
            email_status = "failed"

    return {
        "ok": True,
        "message": "Your request has been received. We'll review your details and send the next steps to your email.",
        "lead_id": lead_id,
        "email_status": email_status,
    }


@app.get("/api/health")
def health():
    return {"status": "ok"}
