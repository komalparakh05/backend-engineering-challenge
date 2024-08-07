# Unbabel Backend Engineering Challenge Solution - Streaming Approach

This project implements an optimized solution for calculating the moving average of translation delivery times, focusing on streaming processing and real-time data handling.

## Features

- Streaming data processing for memory efficiency
- Real-time data handling capabilities
- Enhanced error handling and data validation
- AWS S3 integration for cloud-based data processing
- API implementation for job submission and result retrieval

## Requirements

- Python 3.7 or higher
- pandas
- pydantic

## Installation

1. Clone the repository:

git clone https://github.com/YOUR_USERNAME/backend-engineering-challenge.git
cd backend-engineering-challenge
text

2. Create a virtual environment and install dependencies:

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
text

## Usage

Run the script with the following command:


python unbabel_cli.py --input_file <path_to_input_file> --window_size <window_size_in_minutes>
text

Example:


python unbabel_cli.py --input_file events.json --window_size 10
text

## Design Considerations

1. **Memory Efficiency**: The solution uses streaming data processing to handle large datasets without consuming excessive memory.
2. **Real-time Capabilities**: Designed to process data in real-time, suitable for live data streams.
3. **Data Validation**: Implements data validation using Pydantic to ensure data integrity.
4. **Error Handling**: Robust error handling and logging for production-ready code.
5. **Extensibility**: Easily extendable to include AWS S3 integration and API implementation.

## Main Solution

The main solution that handles large data, uses parallel processing, and includes error handling is available in the `main_solution` branch. This solution demonstrates:

1. Parallel processing for improved performance
2. Chunked data processing for handling large files
3. Error handling and logging
4. Configurable chunk size for optimization

To explore the main solution, check out the `main_solution` branch:


git checkout main_solution
text

This main solution showcases additional data engineering skills and provides a comprehensive approach to the challenge.