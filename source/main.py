from orderbook import OrderBook

order_book = OrderBook()
order_book.add_order(1000, 100, 10.0)
order_book.add_order(2000, 101, 13.0)
order_book.add_order(2200, 102, 13.0)

order_book.remove_order(2400, 101)
order_book.remove_order(2500, 102)
order_book.remove_order(4000, 100)

print(order_book.calculate_time_weighted_average_price())