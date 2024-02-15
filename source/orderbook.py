import heapq

class OrderBook:
    def __init__(self):
        self.active_orders = {}
        self.prices_heap = [] # Heap that stores prices, it uses negative values to simulate a max heap.
        self.total_max_prices_weighted = 0 # Accumulates the total of each max price multiplied by the time it was the max.
        self.total_active_time = 0 # Tracks the total time from the first order to the last order processed.
        self.first_order_timestamp = 0 # Timestamp of the first order
        self.latest_max_price_active_timestamp = 0 # Timestamp of the latest highest order price

    def get_current_max_price(self):
        # Heap cleaning
        while self.prices_heap and self.prices_heap[0][1] not in self.active_orders:
            heapq.heappop(self.prices_heap)

        # Return the current max price if the heap is not empty
        if self.prices_heap:
            return -self.prices_heap[0][0]
        else:
            return None

    def add_order(self, timestamp, id, price):
        # In case this is the initial order, we set the appropriate value to the responsible variable
        if self.first_order_timestamp == 0:
            self.first_order_timestamp = timestamp

        # If the current max price exists, we update the total active time for the top/max orders and if the new order's price is higher than the current max/top price
        # we will update the weighted value in the appropriate variable getting the timestamp from the heap and also set the latest max price timestamp 
        # to the new order's timestamp
        if self.get_current_max_price() != None:
            self.total_active_time = timestamp - self.first_order_timestamp
            if price > self.get_current_max_price():
                self.total_max_prices_weighted += self.get_current_max_price() * (timestamp - self.prices_heap[0][2])
                self.latest_max_price_active_timestamp = timestamp

        # We push the new order data to the heap
        heapq.heappush(self.prices_heap, [-price, id, timestamp])
        # We also push the order data as a tuple into the dictionary that holds all the active orders for easy access (if needed) and for further checks
        self.active_orders[id] = (price, timestamp)
            
    def remove_order(self, timestamp, id):
        self.total_active_time = timestamp - self.first_order_timestamp # We update the total active time of max/top orders

        # If the currently being removed order id is the top/max price (meaning its on top of the heap) and is also an active order, we update the corresponding variables
        if id == self.prices_heap[0][1] and id in self.active_orders:
            self.total_max_prices_weighted += self.get_current_max_price() * (timestamp - self.latest_max_price_active_timestamp)
            self.latest_max_price_active_timestamp = timestamp
            heapq.heappop(self.prices_heap) # We pop the top/max price from the heap

        # We pop the order from our dictionary since it is no longer active order
        self.active_orders.pop(id)

    def calculate_time_weighted_average_price(self):
        # Simple calculation for avg weighted price using the variables
        return self.total_max_prices_weighted / self.total_active_time