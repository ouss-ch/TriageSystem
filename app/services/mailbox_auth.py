"""Verify IMAP credentials for a mailbox before it's persisted as a sweep target."""

import imaplib

# TODO: extend/override via config for providers not covered here.
_KNOWN_IMAP_HOSTS = {
    "gmail.com": "imap.gmail.com",
    "outlook.com": "imap-mail.outlook.com",
    "hotmail.com": "imap-mail.outlook.com",
    "yahoo.com": "imap.mail.yahoo.com",
}


def _resolve_imap_host(email: str) -> str:
    domain = email.rsplit("@", 1)[-1].lower()
    return _KNOWN_IMAP_HOSTS.get(domain, f"imap.{domain}")


def verify_imap_credentials(email: str, password: str, port: int = 993) -> bool:
    """Attempt a real IMAP login. Returns False on any auth or connection failure."""
    host = _resolve_imap_host(email)
    try:
        conn = imaplib.IMAP4_SSL(host, port)
        try:
            conn.login(email, password)
        finally:
            conn.logout()
        return True
    except (imaplib.IMAP4.error, OSError):
        return False
