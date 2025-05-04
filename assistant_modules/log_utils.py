import json
import logging
from datetime import datetime

from config import RUN_TIME_TABLE_LOG_JSON

logger = logging.getLogger(__name__)


def log_runtime(function_or_name: str, duration: float):
    time_record = {
        "timestamp": datetime.now().isoformat(),
        "function": function_or_name,
        "duration": f"{duration:.4f}",
    }
    with open(RUN_TIME_TABLE_LOG_JSON, "a") as file:
        json.dump(time_record, file)
        file.write("\n")

    logger.info(f"⏰ {function_or_name}() took {duration:.4f} seconds")


def log_ws_event(direction: str, event: dict):
    event_type = event.get("type", "Unknown")
    icon = "⬆️ - Out" if direction.lower() == "outgoing" else "⬇️ - In"
    logger.info(f"{icon} {event_type}")
