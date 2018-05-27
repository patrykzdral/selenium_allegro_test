from datetime import datetime


class Order(object):

    def __init__(self, seller: str,
                 purchase_date: object, price: float,
                 price_with_delivery: float, number_of_elements: int = 1):
        self._seller = seller
        self._purchase_date = datetime.strptime(purchase_date, '%d.%m.%Y, '
                                                               '%H:%M')
        self._price = price
        self._delivery = price_with_delivery - price
        self._number_of_elements = number_of_elements

    def __str__(self) -> str:
        return "(sprzedawca: " + self._seller + ", data zakupu: " \
               + str(self._purchase_date) + ", cena: " + str(self._price) \
               + ", cena dostawy: " + str(round(self._delivery, 2)) \
               + ", szt.: " + str(self._number_of_elements) + ")"

    def __repr__(self) -> str:
        return "(sprzedawca: " + self._seller + ", data zakupu: " \
               + str(self._purchase_date) + ", cena: " + str(self._price) \
               + ", cena dostawy: " + str(round(self._delivery, 2)) \
               + ", szt.: " + str(self._number_of_elements) + ")"

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
