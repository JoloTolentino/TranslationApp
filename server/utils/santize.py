import re
import html

def clean_username(username: str) -> str:
    """Strip and remove non-alphanumeric characters (except underscores)."""
    username = username.strip()
    return re.sub(r'[^\w]', '', username)

def clean_email(email: str) -> str:
    """Lowercase and strip whitespace from email."""
    return email.strip().lower()

def clean_name(name: str) -> str:
    """Capitalize and strip name input."""
    return name.strip().title()

def clean_text(text: str) -> str:
    """Remove script tags or suspicious HTML."""
    text = text.strip()
    return re.sub(r'<.*?>', '', text)

def escape_html(text: str) -> str:
    """Replaces < to &lt and > to &gt"""
    return html.escape(text.strip())  