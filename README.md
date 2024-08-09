# Unbabel Backend Engineering Challenge - Streaming Processing Approach

This project implements a streaming processing approach to calculate the moving average of translation delivery times. It processes events in a streaming fashion, suitable for real-time data handling.

## Features

- **Streaming Processing**: Handles events as they arrive, maintaining a dynamic window for real-time data handling.
- **Data Validation**: Uses Pydantic for event validation to ensure data integrity.
- **Robust Error Handling**: Manages parsing errors gracefully and logs them.
- **Detailed Logging**: Provides logging to track execution flow and identify potential issues.

## Requirements

- Python 3.7 or higher
- pandas
- pydantic

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/komalparakh05/backend-engineering-challenge.git
   cd backend-engineering-challenge


2. Create a virtual environment and install dependencies:

	```bash
 	python -m venv venv
	.\venv\Scripts\activate  # On Windows
	# source venv/bin/activate  # On macOS/Linux
	pip install -r requirements.txt


## Usage

Run the script with the following command:

	
	python unbabel_cli.py --input_file <path_to_input_file> --window_size <window_size_in_minutes> [--chunk_size <chunk_size>]

Example:

	
	python unbabel_cli.py --input_file events.json --window_size 10 --chunk_size 50000


## Testing

To test the code, you can create unit tests using a framework like unittest or pytest. Ensure your tests cover key functionalities such as parsing input, calculating averages, and handling errors. Here's how to set up pytest:

Install pytest:
	
	pip install pytest

Run tests using:

	pytest

**Refer to the `test_unbabel_cli.py` script located in the tests directory for details on how to use `pytest`.**


## Design Considerations

1. **Memory Efficiency**: The solution uses streaming data processing to handle large datasets without consuming excessive memory.
2. **Real-time Capabilities**: Designed to process data in real-time, suitable for live data streams.
3. **Data Integrity and Validation**: Implements data validation using Pydantic to ensure data integrity.
4. **Error Resilience**: Incorporates error handling to ensure robust execution.
5. **Extensibility**: Easily extendable to include AWS S3 integration and API implementation.
6. **Transparency**: Provides logging to help understand the processing flow and diagnose issues.


## Main Solution

The main solution that works on Sequential Processing Approach, is available in the `main_solution` branch. 

To explore the main solution, check out the `main_solution` branch:
  
  git checkout main_solution
