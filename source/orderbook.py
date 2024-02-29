import heapq # Imports priority queue to efficinelty handle accessing the highest price at any time

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class OrderBook:
    def __init__(self):
        self.active_orders = set() # Set that stores all currently active order IDs (should be more efficient than a list for our purpose)
        self.prices_heap = [] # Heap array which utilizes the heapq library to always have access to the highest price quickly and efficiently
        self.total_highest_prices_weighted = 0 #  Time weighted total highest prices
        self.total_active_time = 0 # Tracks the total time from the first order to the last order (exludes time with no active orders)
        self.latest_highest_price_timestamp = 0 # Timestamp of the latest highest order
        self.total_no_orders_time = 0 # Total time with no active orders
        self.last_order_before_no_order_timestamp = 0 # Timestamp of the last order before no active orders

    def get_current_max_price(self):
        # Heap cleaning; checks whether the highest price (top of the heap) is still active order and if not, we pop it from the heap
        self.clear_prices_heap()

        # Return the current max price if the heap is not empty
        # The reason we need to make it negative is that heapq library provides min-heap by default, but we want to max-heap, thus when we add new order to it, we 
        # always put it as a negative number, which basically simulates the max-heap behavior - and when we return the top of it, we need to convert it back to the
        # positive number by negating it once more
        if self.prices_heap:
            return -self.prices_heap[0][0]
        else:
            return None

    def add_order(self, timestamp, id, price):
        # logger.debug(f'Adding order: {id} at {timestamp} with price {price}')
        current_max_price = self.get_current_max_price() # Stores the current max price into variable to prevent redundant calls to the function down below

        # If the current max price exists, we update the total active time for the highest orders and if the new order's price is higher than the current highest price
        # we will update the weighted value in the appropriate variable getting the timestamp from the heap and also set the latest highest price timestamp 
        # to the new order's timestamp
        if id not in self.active_orders: # Makes sure the order id doesn't exist already
            if current_max_price != None:
                self.total_active_time = (timestamp - self.total_no_orders_time)
                if price > current_max_price:
                    self.total_highest_prices_weighted += current_max_price * (timestamp - self.latest_highest_price_timestamp)
                    self.latest_highest_price_timestamp = timestamp
            else: # If no max price exists, that means there were no orders before this one
                self.total_no_orders_time += (timestamp - self.last_order_before_no_order_timestamp)
                self.latest_highest_price_timestamp = timestamp

            # We push the new order data to the heap
            heapq.heappush(self.prices_heap, [-price, id, timestamp])
            # We also push the order data as a tuple into the dictionary that holds all the active orders for easy access (if needed) and for further checks
            self.active_orders.add(id)
    
    def remove_order(self, timestamp, id):
        # Makes sure we are not trying to remove non-existant order
        if id in self.active_orders:
            self.total_active_time = (timestamp - self.total_no_orders_time) # We update the total active time of highests orders
            self.active_orders.discard(id) # We remove the order id from our list since it is no longer active order

            # If the currently being removed order id is the highest price (meaning its on top of the heap), we update the corresponding variables
            if id == self.prices_heap[0][1]:
                self.total_highest_prices_weighted += (-self.prices_heap[0][0]) * (timestamp - self.latest_highest_price_timestamp)
                if self.prices_heap:
                    self.latest_highest_price_timestamp = timestamp

            # This is true in case we removed the last active order
            if len(self.active_orders) == 0:
                self.last_order_before_no_order_timestamp = timestamp

            # Makes sure the heap is reflecting only active orders
            self.clear_prices_heap()

    def calculate_time_weighted_average_highest_price(self):
        # Simple calculation for avg weighted price using the variables
        if self.total_active_time: # Avoids division by zero
            return self.total_highest_prices_weighted / self.total_active_time
        else:
            return 0
    
    def clear_prices_heap(self):
        # Checks whether there are any redundant orders in the heap that are no longer available
        while self.prices_heap and self.prices_heap[0][1] not in self.active_orders:
            heapq.heappop(self.prices_heap)