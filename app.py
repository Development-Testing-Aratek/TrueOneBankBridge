import os
import re
import hmac
import secrets
import sqlite3
import time
from datetime import datetime, timezone
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session, abort, make_response
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.middleware.proxy_fix import ProxyFix

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.environ.get("DATABASE_PATH", os.path.join(BASE_DIR, "instance", "enquiries.sqlite3"))
SECRET_KEY = os.environ.get("SECRET_KEY")
ADMIN_PASSWORD_HASH = os.environ.get("ADMIN_PASSWORD_HASH")
APP_ENV = os.environ.get("APP_ENV", "development").lower()

app = Flask(__name__)
app.secret_key = SECRET_KEY or "dev-only-change-this-before-deployment"
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=(APP_ENV == "production"),
    MAX_CONTENT_LENGTH=32 * 1024,
    PERMANENT_SESSION_LIFETIME=1800,
)
# Only enable this behind a trusted reverse proxy you control.
if os.environ.get("TRUST_PROXY", "0") == "1":
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def connect_db():
    db = sqlite3.connect(DB_PATH, timeout=10)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with connect_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS enquiries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                full_name TEXT NOT NULL,
                mobile TEXT NOT NULL,
                loan_type TEXT NOT NULL,
                amount_range TEXT,
                city TEXT NOT NULL,
                callback_time TEXT NOT NULL,
                notes TEXT,
                consent INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'New'
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS rate_limits (
                client_key TEXT NOT NULL,
                bucket INTEGER NOT NULL,
                count INTEGER NOT NULL,
                PRIMARY KEY (client_key, bucket)
            )
        """)
init_db()

def rate_limited():
    # Simple persistent limit: up to 5 form posts per IP per rolling 15-minute bucket.
    client = request.headers.get("CF-Connecting-IP") or request.remote_addr or "unknown"
    # Store a keyed digest, not the raw IP address.
    key = hmac.new(app.secret_key.encode(), client.encode(), "sha256").hexdigest()
    bucket = int(time.time() // 900)
    with connect_db() as db:
        row = db.execute("SELECT count FROM rate_limits WHERE client_key=? AND bucket=?", (key, bucket)).fetchone()
        if row and row["count"] >= 5:
            return True
        db.execute("""
            INSERT INTO rate_limits(client_key, bucket, count) VALUES(?,?,1)
            ON CONFLICT(client_key,bucket) DO UPDATE SET count=count+1
        """, (key, bucket))
        db.execute("DELETE FROM rate_limits WHERE bucket < ?", (bucket - 4,))
    return False

@app.after_request
def security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; style-src 'self'; script-src 'self'; "
        "img-src 'self' data:; font-src 'self'; connect-src 'self'; "
        "form-action 'self'; frame-ancestors 'none'; base-uri 'self'"
    )
    if APP_ENV == "production":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

def csrf_token():
    if "_csrf" not in session:
        session["_csrf"] = secrets.token_urlsafe(32)
    return session["_csrf"]
app.jinja_env.globals["csrf_token"] = csrf_token

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/enquiry", methods=["POST"])
def submit_enquiry():
    submitted_token = request.form.get("_csrf", "")
    if not submitted_token or not hmac.compare_digest(submitted_token, session.get("_csrf", "")):
        abort(400, description="Your session expired. Please refresh the page and try again.")
    # Honeypot field. Real users should leave it blank.
    if request.form.get("website", "").strip():
        return redirect(url_for("home") + "#contact")
    if rate_limited():
        flash("Too many attempts. Please wait a little and try again.", "error")
        return redirect(url_for("home") + "#contact")

    name = " ".join(request.form.get("full_name", "").split())
    mobile = re.sub(r"[\s()+-]", "", request.form.get("mobile", ""))
    loan_type = request.form.get("loan_type", "")
    amount = request.form.get("amount_range", "")
    city = " ".join(request.form.get("city", "").split())
    callback = request.form.get("callback_time", "")
    notes = " ".join(request.form.get("notes", "").split())[:1000]
    consent = request.form.get("consent") == "yes"

    errors = []
    if not 2 <= len(name) <= 100 or not re.fullmatch(r"[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ .'-]*", name):
        errors.append("Enter a valid full name.")
    if not re.fullmatch(r"(?:91)?[6-9]\d{9}", mobile):
        errors.append("Enter a valid Indian mobile number.")
    if loan_type not in {"Personal Loan", "Home Loan", "Both / Not sure"}:
        errors.append("Choose a loan type.")
    if amount not in {"", "Below ₹5 lakh", "₹5–10 lakh", "₹10–25 lakh", "₹25–50 lakh", "Above ₹50 lakh", "Not decided"}:
        errors.append("Choose a valid amount range.")
    if not 2 <= len(city) <= 80 or not re.fullmatch(r"[A-Za-zÀ-ÿ0-9 .,'-]+", city):
        errors.append("Enter a valid city.")
    if callback not in {"Any convenient time", "Morning (9 AM–12 PM)", "Afternoon (12 PM–4 PM)", "Evening (4 PM–7 PM)"}:
        errors.append("Choose a callback time.")
    if not consent:
        errors.append("Consent is required before submitting.")
    if errors:
        for error in errors:
            flash(error, "error")
        return redirect(url_for("home") + "#contact")

    with connect_db() as db:
        db.execute("""
            INSERT INTO enquiries (created_at, full_name, mobile, loan_type, amount_range, city, callback_time, notes, consent)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
        """, (datetime.now(timezone.utc).isoformat(timespec="seconds"), name, mobile, loan_type, amount, city, callback, notes))
    session.pop("_csrf", None)
    flash("Thank you. Your enquiry has been received. Our team can follow up using the contact details you provided.", "success")
    return redirect(url_for("home") + "#contact")

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login"))
        return fn(*args, **kwargs)
    return wrapper

@app.route("/manage/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        token = request.form.get("_csrf", "")
        if not token or not hmac.compare_digest(token, session.get("_csrf", "")):
            abort(400)
        password = request.form.get("password", "")
        if ADMIN_PASSWORD_HASH and check_password_hash(ADMIN_PASSWORD_HASH, password):
            session.clear()
            session["admin_logged_in"] = True
            session.permanent = True
            return redirect(url_for("admin_dashboard"))
        time.sleep(0.6)
        flash("Login failed. Check your credentials.", "error")
    return render_template("admin_login.html")

@app.route("/manage")
@admin_required
def admin_dashboard():
    with connect_db() as db:
        rows = db.execute("SELECT * FROM enquiries ORDER BY id DESC LIMIT 500").fetchall()
    response = make_response(render_template("admin.html", enquiries=rows))
    response.headers["Cache-Control"] = "no-store"
    return response

@app.route("/manage/logout", methods=["POST"])
@admin_required
def admin_logout():
    session.clear()
    return redirect(url_for("home"))

@app.errorhandler(400)
def bad_request(error):
    return render_template("error.html", code=400, message=getattr(error, "description", "Invalid request.")), 400

@app.errorhandler(413)
def too_large(error):
    return render_template("error.html", code=413, message="The submitted form is too large."), 413

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5000")), debug=False)
