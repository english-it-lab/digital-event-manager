import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

os.environ.setdefault("EMAIL_PASSWORD", "test-password")
os.environ.setdefault("EMAIL_LOGIN", "test@example.com")
os.environ.setdefault("SMTP_SERVER", "smtp.example.com")
