# VU-AMS Converter

This brief Python script provides tools for reading, extracting, and processing data from `amsdatai`, recorded using VU-AMS device (https://vu-ams.nl/). `amsdatai` are processed using the VU-DAMS software (https://vu-ams.nl/downloads/). 

This script includes functionalities for handling binary data within ZIP files, extracting specific files from ZIP archives, and parsing JSON content. Additionally, it features a specialized converter for adjusting timestamps and inter-beat intervals (IBIs) from heartbeat data. In short, you don't need to extract IBIs by opening VU-DAMS. This script automates the process and generates a similar dataframe to the VU-DAMS .txt exported IBI file.

## Features

- **Read and Extract ZIP**: Opens a ZIP file, identifies the ZIP file signature within binary data, and extracts content.
- **Extract Specific Data**: Reads a ZIP file to extract and process a specific file, assuming the content is in JSON format.
- **Timestamp and IBI Converter**: Converts and adjusts timestamps and IBIs from heartbeat data, accounting for specific year and month adjustments, as well as a consistent offset.

## Usage

1. **read_and_extract_zip(file_path)**: Provide the file path to read and attempt to extract ZIP file content. Prints the contents of the ZIP archive if successful.

2. **read_zip_and_extract_data(file_path, target_file)**: Provide the file path and the specific target file name within the ZIP archive to extract and process JSON data.

3. **ibi_and_timestamp_converter(beats_data, starts_data)**: Converts timestamp and IBI data from a given dataset. The input should include heartbeat data and starting timestamp data in a specific format.

## Requirements

- Python 3
- The `zipfile`, `io`, and `json` modules from Python's standard library.

## Installation

No additional installation is required beyond a standard Python environment.

## Example

To use the script, simply import the functions into your Python script and call them with the appropriate parameters. Ensure your data files are accessible by the script.

```python
import vuams

# Example call
file_path = 'path/to/your/amsdatai'

beats_data = vuams.read_zip_and_extract_data(file_path, 'beats.json')
starts_data = vuams.read_zip_and_extract_data(file_path, 'starts.json')

data = vuams.ibi_and_timestamp_converter (beats_data, starts_data)
```



## Contributing

Feel free to fork this repository and submit pull requests to enhance the functionalities.