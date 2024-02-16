import os
from data_processing import process_data_from_file

script_directory = os.path.dirname(os.path.abspath(__file__)) # Absolute path to the script's directory
data_file_path = os.path.join(script_directory, '..', 'data', 'input_data.txt') # Forms the file path to the input data

try:
    weighted_average_highest_price = process_data_from_file(data_file_path)
    print(f'Average highest price (weighted by time) is {weighted_average_highest_price}')
except Exception as e:
    print(f'Error has occured: {e}')