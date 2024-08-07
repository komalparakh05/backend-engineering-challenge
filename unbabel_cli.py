#!/usr/bin/env python3

import argparse
import json
from datetime import datetime, timedelta
from collections import deque

def parse_arguments():
    parser = argparse.ArgumentParser(description='Calculate moving average of translation delivery times.')
    parser.add_argument('--input_file', required=True, help='Path to the input JSON file')
    parser.add_argument('--window_size', type=int, required=True, help='Window size in minutes')
    return parser.parse_args()

def parse_timestamp(timestamp_str):
    return datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")

def calculate_moving_average(input_file, window_size):
    window = deque()
    current_minute = None
    
    with open(input_file, 'r') as f:
        for line in f:
            event = json.loads(line)
            timestamp = parse_timestamp(event['timestamp'])
            minute = timestamp.replace(second=0, microsecond=0)
            
            if current_minute is None:
                current_minute = minute
            
            while current_minute <= minute:
                # Remove events outside the window
                while window and (current_minute - parse_timestamp(window[0]['timestamp'])).total_seconds() / 60 >= window_size:
                    window.popleft()
                
                # Calculate average delivery time
                if window:
                    avg_delivery_time = sum(e['duration'] for e in window) / len(window)
                else:
                    avg_delivery_time = 0
                
                # Output result
                print(json.dumps({
                    "date": current_minute.strftime("%Y-%m-%d %H:%M:%S"),
                    "average_delivery_time": round(avg_delivery_time, 1)
                }))
                
                current_minute += timedelta(minutes=1)
            
            window.append(event)

def main():
    args = parse_arguments()
    calculate_moving_average(args.input_file, args.window_size)

if __name__ == "__main__":
    main()