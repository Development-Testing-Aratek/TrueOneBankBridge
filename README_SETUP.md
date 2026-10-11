# True One Bank Bridge — static website with Formspree

This version runs as a static website and does not need Python, Flask, a local server, or a custom backend. The enquiry form posts to Formspree.

## 1. Create the Formspree form
1. Sign in at https://formspree.io/.
2. Create a new form named `True One Bank Bridge Enquiries`.
3. Verify the target email address and open the form's Integration page.
4. Copy the endpoint, which looks like `https://formspree.io/f/xxxxxxxx`.
5. In `index.html`, replace `https://formspree.io/f/REPLACE_WITH_YOUR_FORM_ID` in the form's `action` attribute with your real endpoint.
6. Update the hidden `_next` field to your final deployed thank-you page URL if your canonical domain differs.
7. Save the file.

The form includes named fields for full_name, mobile, loan_type, amount_range, city, callback_time, notes, consent, a subject line and a `_gotcha` spam honeypot. All form controls intended for submission have a `name`.

## 2. Turn on email notifications
In Formspree, open the form's settings/workflow and configure the Target Email/notification destination. Verify the email address if asked. Submit a test enquiry and confirm that the notification arrives. Also verify the submission appears in the Formspree dashboard.

## 3. Connect Google Sheets
Formspree supports a Google Sheets plugin/integration, but availability depends on the current plan and dashboard. Open your form's Workflow/Plugins area, select Google Sheets, connect the Google account, choose/create the destination sheet, and save. If the Google Sheets option is not available on your plan, use a supported automation integration such as Zapier/Make or upgrade only after checking the current plan pricing. Do not add Google service-account private keys to this public website.

## 4. Test
- Submit a test with dummy information.
- Verify the submission in Formspree.
- Verify email notification.
- Verify a new row appears in Google Sheets.
- Verify the thank-you page opens.
- Test on mobile and desktop.
- Do not use real customer data until privacy, business and partner disclosures are complete.

## 5. Deploy to Cloudflare Pages
This folder contains static HTML/CSS/JS and can be deployed as a static website:
1. Upload the contents of this folder (the `index.html` file must be at the deployment root) to Cloudflare Pages using Direct Upload, or commit the files to a Git repository and connect it to Pages.
2. Open the generated `*.pages.dev` address and test the form.
3. In Cloudflare Pages, add `trueonebankbridge.com` and optionally `www.trueonebankbridge.com` as custom domains. Follow the DNS records Cloudflare provides.
4. Do not guess DNS IPs or restore the old `185.158.133.1` record. Keep unrelated email MX/TXT records such as SPF and DMARC.
5. Make sure `index.html` uses the correct public `https://trueonebankbridge.com/thank-you.html` URL in `_next` after the domain is active.

## Important
This static version does not include the Flask database/admin dashboard. Formspree holds submissions and sends configured notifications; Google Sheets can act as a separate records list if integration is enabled. The privacy and terms pages are drafts and must be completed for your actual business before launch. Avoid collecting OTPs, passwords, card details, Aadhaar/PAN numbers or other sensitive identity data through this general enquiry form.
