import time
from imapclient import IMAPClient
import pyzmail

from config import (
    GMAIL_ADDRESS,
    GMAIL_APP_PASSWORD,
    IMAP_SERVER,
)
from agent import handle_question
from mailer import send_email


# =========================
# Constants
# =========================

AUTO_REPLY_HEADER = (
    "⚠️ This is an auto-generated email.\n\n"
)


# =========================
# Filters & Helpers
# =========================

def is_no_reply(sender: str) -> bool:
    """Ignore automated/system emails."""
    sender = sender.lower()
    blocked_keywords = [
        "no-reply",
        "noreply",
        "do-not-reply",
        "mailer-daemon",
        "postmaster",
        "accounts.google.com",
    ]
    return any(k in sender for k in blocked_keywords)


def extract_text(message: pyzmail.PyzMessage) -> str:
    """Extract plain text body safely."""
    if message.text_part:
        return message.text_part.get_payload().decode(
            message.text_part.charset or "utf-8",
            errors="ignore",
        )
    return ""


# =========================
# Main Mailbox Logic
# =========================

def check_mailbox():
    with IMAPClient(IMAP_SERVER) as server:
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.select_folder("INBOX")

        # Fetch unread emails only
        messages = server.search(["UNSEEN"])

        for uid in messages:
            raw = server.fetch(uid, ["RFC822"])[uid][b"RFC822"]
            msg = pyzmail.PyzMessage.factory(raw)

            sender = msg.get_addresses("from")[0][1]
            subject = msg.get_subject() or ""
            body = extract_text(msg).strip()

            # ❌ Skip auto/system emails
            if is_no_reply(sender):
                print(f"Skipping automated email from {sender}")
                server.add_flags(uid, ["\\Seen"])
                continue

            # ❌ Skip empty or very short emails
            if not body or len(body) < 10:
                print(f"Skipping short/empty email from {sender}")
                server.add_flags(uid, ["\\Seen"])
                continue

            # ❌ Skip link-only emails
            if body.startswith("http"):
                print(f"Skipping link-only email from {sender}")
                server.add_flags(uid, ["\\Seen"])
                continue

            print(f"Processing email from {sender}")

            try:
                answer = handle_question(sender, body)

                final_answer = AUTO_REPLY_HEADER + answer

                send_email(
                    to_address=sender,
                    subject=f"Re: {subject}",
                    body=final_answer,
                )

            except Exception as e:
                print(f"Error processing email from {sender}: {e}")

            # Mark as read after processing
            server.add_flags(uid, ["\\Seen"])


# =========================
# Runner
# =========================

if __name__ == "__main__":
    print("📬 Email agent started. Polling inbox every 5 minutes...")

    while True:
        check_mailbox()
        time.sleep(300)
