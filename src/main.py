from src.gmail_service import (
    get_gmail_service,
    fetch_unread_emails,
    get_email_message,
    mark_email_as_read
)
from src.email_parser import extract_email_data
from src.sheets_service import (
    get_sheets_service,
    ensure_header_row,
    append_email_row
)
from src.state_manager import load_state, save_state, is_processed, mark_processed


def main():
    gmail_service = get_gmail_service()
    sheets_service = get_sheets_service()

    ensure_header_row(sheets_service)

    state = load_state()

    messages = fetch_unread_emails(gmail_service)

    if not messages:
        print("No unread emails found.")
        return

    for msg in messages:
        message_id = msg["id"]

        
        if is_processed(message_id, state):
            print("Skipped duplicate email")
            continue

        full_message = get_email_message(gmail_service, message_id)
        email_data = extract_email_data(full_message)

        append_email_row(sheets_service, email_data)
        mark_email_as_read(gmail_service, message_id)

        mark_processed(message_id, state)
        print("Added:", email_data["subject"])

    save_state(state)
    print("🎉 All emails processed successfully!")


if __name__ == "__main__":
    main()
