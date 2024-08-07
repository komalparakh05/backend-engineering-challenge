import json
import pandas as pd
from datetime import datetime, timedelta
import argparse
from typing import Iterator, Dict, Any
from pydantic import BaseModel, validator
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TranslationEvent(BaseModel):
    timestamp: datetime
    translation_id: str
    source_language: str
    target_language: str
    client_name: str
    event_name: str
    duration: int
    nr_words: int

    @validator('event_name')
    def check_event_name(cls, v):
        if v != 'translation_delivered':
            raise ValueError('Invalid event_name')
        return v

def parse_json_stream(file_path: str) -> Iterator[Dict[str, Any]]:
    """Parse JSON objects from a file, one per line."""
    with open(file_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            try:
                event_dict = json.loads(line)
                TranslationEvent(**event_dict)
                yield event_dict
            except (json.JSONDecodeError, ValueError) as e:
                logger.warning(f"Error processing line {line_num}: {e}")

def process_events_stream(input_file: str, window_size: int):
    """Process events in a streaming fashion and calculate moving averages."""
    window = pd.DataFrame()
    current_minute = None

    for event in parse_json_stream(input_file):
        event_time = pd.to_datetime(event['timestamp'])
        event_minute = event_time.floor('T')

        if current_minute is None:
            current_minute = event_minute

        while current_minute <= event_minute:
            window = window[window.index >= current_minute - pd.Timedelta(minutes=window_size)]
            avg_delivery_time = window['duration'].mean()
            yield {
                'date': current_minute.strftime('%Y-%m-%d %H:%M:%S'),
                'average_delivery_time': round(float(avg_delivery_time), 1) if not pd.isna(avg_delivery_time) else 0
            }
            current_minute += timedelta(minutes=1)

        window = window.append(pd.Series(event, name=event_time))

def main():
    parser = argparse.ArgumentParser(description='Calculate moving average of translation delivery times.')
    parser.add_argument('--input_file', required=True, help='Path to the input JSON file')
    parser.add_argument('--window_size', type=int, required=True, help='Window size in minutes')
    args = parser.parse_args()

    for result in process_events_stream(args.input_file, args.window_size):
        print(json.dumps(result))

if __name__ == "__main__":
    main()