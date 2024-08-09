import json
import pandas as pd
from datetime import datetime, timedelta
import argparse
from typing import Iterator, Dict, Any
from pydantic import BaseModel, field_validator
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TranslationEvent(BaseModel):
    """Data model for a translation event, with validation."""
    timestamp: datetime
    translation_id: str
    source_language: str
    target_language: str
    client_name: str
    event_name: str
    duration: int
    nr_words: int

    @field_validator('event_name')
    def check_event_name(cls, v):
        """Validate that the event name is 'translation_delivered'."""
        if v != 'translation_delivered':
            raise ValueError('Invalid event_name')
        return v

def parse_json_stream(file_path: str) -> Iterator[Dict[str, Any]]:
    """Parse JSON objects from a file, one per line."""
    with open(file_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            try:
                event_dict = json.loads(line)
                TranslationEvent(**event_dict)  # Validate the event
                yield event_dict
            except (json.JSONDecodeError, ValueError) as e:
                logger.warning(f"Error processing line {line_num}: {e}")

def process_events_stream(input_file: str, window_size: int):
    """Process events in a streaming fashion and calculate moving averages."""
    window = pd.DataFrame(columns=['timestamp', 'duration'])  # DataFrame to hold events within the window
    current_minute = None  # Track the current minute being processed
    last_event_minute = None  # Track the last event's minute

    for event in parse_json_stream(input_file):
        event_time = pd.to_datetime(event['timestamp'])
        event_minute = event_time.floor('min')  # Round down to the nearest minute

        if current_minute is None:
            current_minute = event_minute

        last_event_minute = event_minute

        # Process each minute up to the current event's minute
        while current_minute <= event_minute:
            # Filter events within the window
            window = window[window['timestamp'] >= current_minute - pd.Timedelta(minutes=window_size)]
            avg_delivery_time = window['duration'].mean() if not window.empty else 0

            # Yield the result for the current minute
            yield {
                'date': current_minute.strftime('%Y-%m-%d %H:%M:%S'),
                'average_delivery_time': round(float(avg_delivery_time), 1)
            }

            current_minute += timedelta(minutes=1)

        # Append the current event to the window using pd.concat
        new_row = pd.DataFrame({'timestamp': [event_time], 'duration': [event['duration']]})
        window = pd.concat([window, new_row], ignore_index=True)

    # Continue processing for the remaining minutes after the last event
    while current_minute <= last_event_minute + timedelta(minutes=window_size):
        # Filter events within the window
        window = window[window['timestamp'] >= current_minute - pd.Timedelta(minutes=window_size)]
        avg_delivery_time = window['duration'].mean() if not window.empty else 0

        # Yield the result for the current minute
        yield {
            'date': current_minute.strftime('%Y-%m-%d %H:%M:%S'),
            'average_delivery_time': round(float(avg_delivery_time), 1)
        }

        current_minute += timedelta(minutes=1)

def main():
    """Main function to parse arguments and process events."""
    parser = argparse.ArgumentParser(description='Calculate moving average of translation delivery times.')
    parser.add_argument('--input_file', required=True, help='Path to the input JSON file')
    parser.add_argument('--window_size', type=int, required=True, help='Window size in minutes')
    args = parser.parse_args()

    # Process events and print results
    for result in process_events_stream(args.input_file, args.window_size):
        print(json.dumps(result))

if __name__ == "__main__":
    main()
