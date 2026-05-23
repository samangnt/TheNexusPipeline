import requests

WEBHOOK_URL = ""

def send_notification(message: str, *args, **kwargs) -> None:
    
    # Build base payload
    payload = {
        "message": message,
        "extras": list(args)
    }
    
    # kwargs lets us add flexible extra fields
    if "priority" in kwargs:
        payload["priority"] = kwargs["priority"]
    
    if "channel" in kwargs:
        payload["channel"] = kwargs["channel"]
    
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        if response.status_code == 200:
            print("Notification sent!")
        else:
            print(f"Webhook failed: {response.status_code}")
    except Exception as e:
        print(f"Webhook error: {e}")