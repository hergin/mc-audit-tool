This small tool is to add audit trail entries faster (with more accurate times)
Imap is also doing it in an automated way checking a specific email for messages, extracting the content and adding to the audit trail.

Python requirements:

Install selenium: pip install selenium

Install chrome driver: https://sites.google.com/a/chromium.org/chromedriver/home
add the executable to the PATH

For the imap part:

Install imap client: pip install imapclient


Notes
-----

Seems to be working now but while extracting body text of the mail email, there seems to be extra new lines. Check that.