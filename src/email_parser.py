import base64

MAX_BODY_CHARS = 3000   # SAFE LIMIT


def get_header(headers, name):
    for h in headers:
        if h["name"].lower() == name.lower():
            return h["value"]
    return ""


def decode_body(encoded):
    if not encoded:
        return ""
    decoded = base64.urlsafe_b64decode(encoded)
    return decoded.decode("utf-8", errors="ignore")


def extract_email_data(message):
    payload = message.get("payload", {})
    headers = payload.get("headers", [])

    from_email = get_header(headers, "From")
    subject = get_header(headers, "Subject")
    date = get_header(headers, "Date")

    body = ""

    # Simple email
    if payload.get("body", {}).get("data"):
        body = decode_body(payload["body"]["data"])

    # Multipart email
    elif payload.get("parts"):
        for part in payload["parts"]:
            if part.get("mimeType") == "text/plain":
                body = decode_body(part["body"].get("data"))
                break

    body = body.strip()

    if len(body) > MAX_BODY_CHARS:
        body = body[:MAX_BODY_CHARS] + "\n\n[TRUNCATED]"

    return {
        "from": from_email,
        "subject": subject,
        "date": date,
        "body": body
    }
