# True One Bank Bridge — working website

Responsive loan-information website with a working EMI calculator, server-side enquiry form, SQLite storage, basic abuse protection, privacy/terms draft pages and a password-protected enquiry dashboard.

## Important before launch
- The logo in `static/assets/brand.svg` is a clean temporary brand mark because the earlier logo image was not included in this project upload. Replace it with your approved logo asset before publishing.
- The Privacy Notice and Terms of Use are drafts. Fill in the real legal entity name, official address/contact, data-sharing partners and retention period; obtain appropriate review.
- Do not describe the business as a bank, lender or authorised partner unless that is legally accurate.
- This application stores enquiry data on the server. Use HTTPS, a persistent disk/database, strong secrets, restricted administrator access, backups and a deletion/retention policy. Never collect OTPs, passwords, card details or identity-document numbers in this form.
- No email notification is configured by default. Enquiries appear at `/manage` after administrator login. Email notifications can be added using a trusted provider and server-side secrets.

## Run locally on Windows
1. Install Python 3.11 or newer from https://www.python.org/downloads/ and enable “Add Python to PATH”.
2. Extract this ZIP to a folder such as `C:\\Websites\\true_one_bank_bridge`.
3. Open PowerShell in that folder.
4. Create and activate a virtual environment:
   ```powershell
   py -m venv .venv
   .\\.venv\\Scripts\\Activate.ps1
   ```
5. Install dependencies:
   ```powershell
   python -m pip install -r requirements.txt
   ```
6. Set local environment variables (use a new random secret and your own admin password hash):
   ```powershell
   $env:APP_ENV="development"
   $env:SECRET_KEY="replace-with-a-long-random-secret-for-local-testing"
   $env:ADMIN_PASSWORD_HASH = python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('replace-this-admin-password'))"
   ```
   Replace `replace-this-admin-password` with a strong unique password. The command above stores a hash in the environment, not the plain password. Do not use this sample password.
7. Start the site:
   ```powershell
   python app.py
   ```
8. Open http://127.0.0.1:5000. Submit a test enquiry using fake/test details. The SQLite database is created at `instance/enquiries.sqlite3`.
9. Open http://127.0.0.1:5000/manage to review enquiries. Sign in with the admin password used when generating the hash.
10. Stop the server with Ctrl+C.

## Deploy to a public host
This is a Flask/Python application, so it cannot be deployed as a static-only Cloudflare Pages upload. Cloudflare can continue managing your domain/DNS, but the app must run on a Python-capable host (for example a VPS or a managed Python service). Configure a persistent disk for SQLite, or use a managed database. Do not deploy with a temporary filesystem if you need enquiry records to persist.

### Render-style deployment
1. Create a private Git repository and upload the project files (do not upload `.env`, secrets or the local database).
2. Create a Python web service from that repository and use `pip install -r requirements.txt` as the build command and `gunicorn app:app --workers 2 --bind 0.0.0.0:$PORT` as the start command.
3. Attach a persistent disk at `/var/data` and set `DATABASE_PATH=/var/data/enquiries.sqlite3`.
4. Set `APP_ENV=production`, `SECRET_KEY` to a strong random secret, and `ADMIN_PASSWORD_HASH` to a Werkzeug password hash generated locally. Keep secrets in the host's environment settings.
5. Verify `/`, `/privacy`, `/terms`, `/manage`, and a test form submission. Confirm records persist after a redeploy/restart.
6. Add `trueonebankbridge.com` and `www.trueonebankbridge.com` in the host's custom-domain settings. Follow that host's exact DNS instructions.
7. In Cloudflare DNS, remove only the conflicting old root/www records after confirming the new host's required record values. Create exactly the records the hosting provider gives you. Keep your email-related MX/TXT records, including SPF and DMARC. Do not guess an IP or CNAME target.
8. Set SSL/TLS to the host/provider's recommended secure mode and confirm HTTPS works for both root and www. Redirect one hostname to the other if desired.

## Production checklist
- [ ] Replace the temporary SVG mark with the approved logo.
- [ ] Complete and review privacy notice and terms.
- [ ] Verify business identity, address, official email/phone and lender/partner disclosures.
- [ ] Configure strong secrets and admin hash in host environment.
- [ ] Configure persistent database storage, backups, retention and access policy.
- [ ] Configure TLS/HTTPS and custom domains.
- [ ] Test form validation, CSRF rejection, rate limiting and admin access.
- [ ] Add monitoring and email notifications if required.
- [ ] Run dependency updates and a security review before accepting real customer information.
