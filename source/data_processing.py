from orderbook import OrderBook

# Processes the input data from the file; accepts 1 argument, which is a path to the file that contains the data; returns time-weighted average price of all highest orders
def process_data_from_file(filename):
    order_book = OrderBook() # Create an instance of the class

    with open(filename, 'r') as file: # Opens the specified file with our data in read mode
        for line in file: # Iterates over each line within the file
            categories = line.strip().split() # Makes sure to remove any excessive whitespace and splits the line into list of substrings

            timestamp = int(categories[0]) # Accesses the first element of the list (representing timestamp of the order), converts it into integer and stores it
            operation = categories[1] # Accesses the second element (operation I/E) and stores it
            identifier = int(categories[2]) # Accesses the third element (ID), converts it into int and stores it

            if operation == 'I': # If the operation of the order is 'I', then it means we want to insert a new order
                price = float(categories[3]) # New orders also have 4th element and that is their price, so we access it and store it as integer here
                order_book.add_order(timestamp, identifier, price) # We call the function that creates/adds a new order
            elif operation == 'E': # If the operation is 'E', then it indicates that the order should be removed/deleted
                order_book.remove_order(timestamp, identifier) # We call the function that fires a logic to remove the order

    return order_book.calculate_time_weighted_average_price() # Returns time-weighted average price of all highest orders
    

