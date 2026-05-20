from utils.utils import subscribe_by_state, subscribe_by_event, available_states, available_weather_events
from events.events import check_if_subscribed
from logger.logger import logger
from events.workers import event_thread
import requests
import threading
import time

base_url = "https://eonet.gsfc.nasa.gov/api/v3/events"

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

last_event_id = None
states = subscribe_by_state(available_states)
events = subscribe_by_event(available_weather_events)

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
            last_event_id = current_event_id
            logger.info(f"New event detected with ID: {current_event_id}")
            
            # check if user is subscribed to either state or weather event 
            state_sub, event_sub = check_if_subscribed(states, events, latest_event)
            if state_sub and event_sub:
                threading.Thread(
                    target=event_thread,
                    args=(latest_event,),
                    daemon=True
                )
        else:
            logger.info("No new event")

    except requests.RequestException as e:
        logger.info(f"Request failed: {e}")

    except Exception as e:
        logger.info(f"Unexpected error: {e}")

    # avoid hammering API
    time.sleep(60)