TRUE ONE BANK BRIDGE — LOCAL WEBSITE STARTER
=============================================

WHAT IS INCLUDED
- index.html: responsive loan information website
- styles.css: responsive design and visual styling
- script.js: EMI calculator, mobile menu, and demo enquiry validation
- assets/true-one-logo.jpeg: your supplied logo
- privacy.html and terms.html: draft templates that must be reviewed/customised

RUN LOCALLY (Windows)
1. Extract true_one_bank_bridge.zip to a folder such as:
   C:\Websites\true_one_bank_bridge
2. Open the folder and double-click index.html.
3. Edit index.html with VS Code or Notepad. Edit styles.css for design and
   script.js for calculator/form behaviour.
4. Refresh the browser to view changes.

OPTIONAL LOCAL HTTP SERVER
Install Python 3, open PowerShell in this folder and run:
   py -m http.server 8000
Then browse to:
   http://localhost:8000
Stop it with Ctrl+C. This is a local preview server, not public hosting.

PUBLISH STATIC SITE (example: Cloudflare Pages + GitHub)
1. Create a GitHub repository and upload index.html, styles.css, script.js,
   privacy.html, terms.html and the assets folder.
2. In Cloudflare Dashboard, open Workers & Pages and create a Pages project
   by importing that repository.
3. For this plain HTML site use no build command (or `exit 0`, if required)
   and set the build output directory to `/` (repository root).
4. Deploy and test the provider's temporary *.pages.dev URL.
5. In Pages > Custom domains, add your domain and follow the exact DNS
   instructions Cloudflare provides. For an apex/root domain, Cloudflare may
   require moving authoritative DNS/nameservers to Cloudflare. Copy the exact
   nameservers provided; do not guess.
6. If changing nameservers at GoDaddy, preserve/recreate existing MX, TXT,
   and other DNS records needed for email and verification. Wait for DNS and
   HTTPS setup to finish.
7. Test the domain on mobile and desktop, links, calculator, and privacy/terms.

IMPORTANT PRODUCTION SECURITY CHECKLIST
- The enquiry form is intentionally DEMO ONLY. It does not send or save anything.
  Do not advertise it as a working enquiry form until you connect a backend.
- Never put API keys, database passwords, SMTP credentials, or private keys in
  HTML/JS. Browser code is public.
- For real enquiries, use HTTPS and a server-side endpoint with validation,
  rate limiting, spam protection, CSRF protection where appropriate, restricted
  access, secure storage, retention/deletion policy, backups and monitoring.
- Do not store enquiries in a public GitHub repository or in client-side code.
- Use a privacy notice and consent flow that accurately reflect actual practices.
- Use a verified business email, phone, legal entity/address, and accurate
  lender/partner disclosures. Remove placeholder contact details.
- Do not claim to be a bank, regulated lender, or loan approver unless accurate
  and legally authorised. Confirm all applicable Indian financial/regulatory
  requirements with qualified counsel/compliance professionals.
- EMI estimates are illustrative; validate calculator results before business use.
- Logo file is the supplied image as-is. Replace with an approved transparent
  PNG/SVG if you have a higher-resolution official logo.

Useful official docs:
Cloudflare Pages: https://developers.cloudflare.com/pages/
Custom domains: https://developers.cloudflare.com/pages/configuration/custom-domains/
GitHub: https://github.com/
