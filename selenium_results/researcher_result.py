from selenium_results.order import Order


class OrdersHistory(object):
    def __init__(self):
        self._oldest_order = Order
        self._orders = []

    @property
    def orders(self):
        return self._orders

    @orders.setter
    def orders(self, new_order):
        self._orders.append(new_order)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
