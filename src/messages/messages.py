from dotenv import load_dotenv
from datetime import datetime
from io import BytesIO
import requests
import os

load_dotenv("../../.env")
api_token = os.getenv("PUSHOVER_API_KEY")
user_key = os.getenv("PUSHOVER_USER_KEY")

def send_notification(image: BytesIO, metadata: dict):
    url = "https://api.pushover.net/1/messages.json"

    # image buffer
    files = {
        "attachment": ("event.png", image.getvalue(), "image/png")
    }

    formatted_date, area_rounded = reconstruct_date_float_values(metadata["Date"], metadata["Area"])

    # check if magnitudeValue is null
    if metadata['Area'] is None:
        area_affected = 'Unknown amount of acreage'
    else:
        area_affected = f"{area_rounded} acres"

    message_lines = [
        "NEW WEATHER EVENT",
        "",
        f"Description: {metadata['Title']}",
        f"Date: {formatted_date}",
        f"Area Affected: {area_affected}"
    ]

    message_lines.append("")
    message_lines.append("Map attached.")

    data = {
        "token": api_token,
        "user": user_key,
        "message": {message_lines}
    }

    requests.post(url, data=data, files=files, timeout=30)

def reconstruct_date_float_values(date: str, value: float):
    # convert UTC date into human readable format
    dt = datetime.fromisoformat(date.replace("Z", "+00:00"))
    formatted_date = dt.strftime("%b %d %Y %I:%M %p UTC")

    # round affected area to 2 places
    affected_area = round(value, 2)
    return formatted_date, affected_area