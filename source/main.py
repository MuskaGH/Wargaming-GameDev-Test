from data_processing import process_data_from_file # Imports a function that contains logic to read the data from the 'input_data.txt' file

data_file_path = '../data/input_data.txt' # Path to our .txt file with the input data

print(process_data_from_file(data_file_path)) # Function that processes the inputted data and returns time-weighted average highest price of orders