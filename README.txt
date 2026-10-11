TRUE ONE BANK BRIDGE — LOCAL WEBSITE STARTER
=============================================

WHAT IS INCLUDED
- index.html: responsive loan information website
- styles.css: responsive design and visual styling
- script.js: EMI calculator and mobile menu
- Google Forms enquiry form: embedded in index.html and completed directly on the page
- assets/true-one-logo.jpeg: your supplied logo
- privacy.html and terms.html: draft templates that must be reviewed/customised

RUN LOCALLY (Windows)
1. Extract true_one_bank_bridge.zip to a folder such as:
   C:\Websites\true_one_bank_bridge
2. Open the folder and double-click index.html.
3. Edit index.html with VS Code or Notepad. Edit styles.css for design and
   script.js for calculator/mobile-menu behaviour. The enquiry form is embedded
   from Google Forms in index.html.
4. Refresh the browser to view changes.

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
7. Test the domain on mobile and desktop, links, calculator, embedded Google
   Form, and privacy/terms.

IMPORTANT PRODUCTION SECURITY CHECKLIST
- The enquiry form is embedded from Google Forms. Visitors complete it directly
   on the page; responses are handled by Google Forms, not stored by this website.
- The form URL is set in index.html. To replace it, update the iframe src with
   the form's Google Forms embed URL. Manage questions, response collection and
   access in Google Forms.
- Ensure the Google Form is published and accepts responses. Review its response
   destination and access permissions, and update the privacy notice to describe
   the information collected and Google's role in processing submissions.
- Never request passwords, OTPs, card details or sensitive identity numbers in
   the enquiry form.
- Use a privacy notice and consent flow that accurately reflect actual practices.
- Use a verified business email, phone, legal entity/address, and accurate
  lender/partner disclosures. Remove placeholder contact details.
- Do not claim to be a bank, regulated lender, or loan approver unless accurate
  and legally authorised. Confirm all applicable Indian financial/regulatory
  requirements with qualified counsel/compliance professionals.
- EMI estimates are illustrative; validate calculator results before business use.

Useful official docs:
Cloudflare Pages: https://developers.cloudflare.com/pages/
Custom domains: https://developers.cloudflare.com/pages/configuration/custom-domains/
GitHub: https://github.com/
