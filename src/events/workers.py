from messages.messages import send_notification
from events.events import plot_coordinates, pack_metadata
from logger.logger import logger
import queue

def event_thread(event_queue: queue.Queue):
    while True:
        latest_event = event_queue.get()

        # switch and match case based on category type
        try:
            logger.info(f"Processing event: {latest_event['id']}")
            event_type = latest_event["categories"]["id"]
            match event_type:
                case "wildfires":
                    # no comma includes events outside the US, throw this out
                    # TODO: add support for world events
                    if "," not in latest_event["title"]:
                        return
                    # check if controlled burn through various 'codes'
                    if "rx" in latest_event["title"] or "Rx" in latest_event["title"] or "RX" in latest_event["title"]:
                        logger.info(f"controlled burn happening | ID: {latest_event['id']}")
                        return
                    else:
                        image = plot_coordinates(latest_event)
                        metadata = pack_metadata(latest_event, image)
                        send_notification(image, metadata)
                # default case
                case _:
                    logger.info(f"unknown weather event '{event_type}' | ID: {latest_event['id']}")

            logger.info(f"Finished processing: {latest_event['id']}")

        except Exception as e:
            logger.exception(f"Worker failed: {e}")
        finally:
            event_queue.task_done()