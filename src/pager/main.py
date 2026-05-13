from logger import logger
import requests
import time


base_url = "https://eonet.gsfc.nasa.gov/api/v3/events"

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

last_event_id = None

while True:
    try:
        get_event = requests.get(url=base_url, headers=headers, timeout=10)
        get_event.raise_for_status()
        event_data = get_event.json()

        events = event_data.get("events", [])

        if not events:
            logger.info("No new event")
            time.sleep(10)
            continue

        latest_event = events[0]
        current_event_id = latest_event["id"]

        # first run
        if last_event_id is None:
            last_event_id = current_event_id
            logger.info(f"Tracking started with: {current_event_id}")

        # detect new event
        elif current_event_id != last_event_id:
            logger.info("NEW EVENT DETECTED")
            logger.info(latest_event)

            last_event_id = current_event_id

        else:
            logger.info("No new event")

    except requests.RequestException as e:
        logger.info(f"Request failed: {e}")

    except Exception as e:
        logger.info(f"Unexpected error: {e}")

    # avoid hammering API
    time.sleep(20)