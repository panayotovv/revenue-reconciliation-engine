import requests

def send_slack_alert(message, webhook_url):
    payload = {
        "text": message
    }

    response = requests.post(webhook_url, json=payload)

    if response.status_code != 200:
        print("Slack error:", response.text)

def analyze_and_alert(results, logger, webhook_url=None):
    low_confidence = []
    missing = []

    for r in results:
        if r["confidence"] < 0.5:
            low_confidence.append(r)

        if r["status"] == "missing":
            missing.append(r)

    message = ""

    if len(low_confidence) > 0:
        message += f"Low confidence matches: {len(low_confidence)}\n"

    if len(missing) >= 3:
        message += f"CRITICAL: {len(missing)} missing payments\n"

    if message:
        if webhook_url:
            send_slack_alert(message, webhook_url)

    return {
        "low_confidence": len(low_confidence),
        "missing": len(missing)
    }