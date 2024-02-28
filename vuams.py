from datetime import datetime, timezone, timedelta
import pandas as pd
import numpy as np 
import os 
import zipfile
import io
import json

def read_and_extract_zip(file_path):
    try:
        # Open the file in binary mode and read its content
        with open(file_path, 'rb') as file:
            content = file.read()
        
        # Search for the ZIP file header in the content
        zip_header_index = content.find(b'PK\x03\x04')
        if zip_header_index == -1:
            print("ZIP file signature not found.")
            return
        
        # Extract the ZIP file from the binary data
        zip_data = content[zip_header_index:]
        
        if zip_data:
            # Use BytesIO to treat the ZIP data as a file-like object
            zip_file = zipfile.ZipFile(io.BytesIO(zip_data), 'r')
            # List files contained within the ZIP archive
            zip_file_contents = zip_file.namelist()
            print("Files in the ZIP archive:", zip_file_contents)
        else:
            print("No ZIP content could be extracted.")
    except Exception as e:
        print(f"Error reading or extracting the file: {e}")

def read_zip_and_extract_data(file_path, target_file):
    try:
        # Open the file in binary mode and read its content
        with open(file_path, 'rb') as file:
            content = file.read()
            #  Find the start of the ZIP data and extract it
            zip_data = content[content.find(b'PK\x03\x04'):]
            # Use BytesIO to treat the ZIP data as a file-like object
            zip_file = zipfile.ZipFile(io.BytesIO(zip_data), 'r')
            # Extract the specific file's content
            extracted_content = zip_file.read(target_file)
            # Assuming the content is JSON, parse it
            data = json.loads(extracted_content)
            # Now, you can process the data as needed
            return data
    except Exception as e:
        print(f"Error extracting or processing {target_file}: {e}")
        return None

def ibi_and_timestamp_converter (beats_data, starts_data):
    
    start_info = starts_data[0]['tStamp']
    # Adjust year
    year_corrected = 1900 + start_info['year']
    # Adjust month 
    month_corrected = 1 + start_info['mon']  
    # If the month was December (12), it becomes January (1)
    if month_corrected == 13:
        month_corrected = 1
    
    # Convert the start time to a datetime object
    session_start_datetime = datetime(year_corrected, month_corrected, start_info['mday'], start_info['hour'], start_info['min'], start_info['sec'])
    
    # Prepare a list to hold adjusted timestamps and IBIs
    adjusted_data = []
    
    # Calculate the offset to adjust RPeakTime based on the first dwClockTick_ms value
    offset_ms = starts_data[0]['dwClockTick_ms']
    base_time = session_start_datetime - timedelta(milliseconds=offset_ms)
    
    # Account for the 500 ms consistent difference observed
    consistent_offset_ms = 500
    
    for i, beat in enumerate(beats_data):
        # Adjust RPeakTime using the offset and convert from microseconds to the correct time format
        # Including the consistent offset to account for the 50 ms difference
        rpeak_time_corrected = base_time + timedelta(milliseconds=(beat['RPeakTime'] / 1000.0) + consistent_offset_ms)
        if i == 0:
            ibi = 0  # The first beat has no preceding beat, so its IBI is 0
        else:
            ibi = (beats_data[i]['RPeakTime'] - beats_data[i-1]['RPeakTime']) / 1000.0
        
        adjusted_data.append((rpeak_time_corrected.strftime('%y-%m-%d/%H:%M:%S.%f')[:-3], ibi))
    
    return adjusted_data




    