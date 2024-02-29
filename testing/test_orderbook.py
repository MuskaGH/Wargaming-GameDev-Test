from source.orderbook import OrderBook

def test_add_order():
    ob = OrderBook()
    ob.add_order(1, "order1", 100)
    assert "order1" in ob.active_orders
    assert ob.get_current_max_price() == 100

def test_remove_order():
    ob = OrderBook()
    ob.add_order(1, "order2", 200)
    ob.add_order(2, "order3", 300)
    ob.remove_order(3, "order2")
    assert "order2" not in ob.active_orders
    assert ob.get_current_max_price() == 300

def test_time_weighted_average_highest_price():
    ob = OrderBook()
    ob.add_order(1, "order4", 400)
    ob.add_order(2, "order5", 500)
    ob.remove_order(3, "order4")
    ob.add_order(4, "order6", 600)
    expected_average = ((2-1)*400 + (4-2)*500) / (4-1)
    assert ob.calculate_time_weighted_average_highest_price() == expected_average