from enum import Enum
from datetime import datetime
from abc import ABC, abstractmethod


class PaymentType(Enum):
    CREDIT = "CREDIT CARD"
    CASH = "CASH"
    CHECK = "CHECK"
    OTHER = "OTHER"


class CustomerType(Enum):
    REG = "REGULAR"
    VIP = "V.I.P"


class Gift(ABC):

    @abstractmethod
    def open_gift(self):
        pass


class CustomerGift(Gift):
    def open_gift(self):
        print("Congratulations! you got a new gift! Enjoy!")


class OrderItem:

    used_ids = set()

    def __init__(self, id, item_name, item_price):
        if id in self.used_ids:
            raise ValueError("ID already used.")
        self.used_ids.add(id)
        self._id = id
        self._item_name = item_name
        self._item_price = item_price

        # Getters

    def get_id(self):
        return self._id

    def get_name(self):
        return self._item_name

    def get_price(self):
        return self._item_price

    # Setters
    def set_name(self, name):
        if not name:
            raise ValueError("Item name cannot be empty")
        self._item_name = name

    def set_price(self, price):
        if price < 0:
            raise ValueError("Price cannot be negative")
        self._item_price = price


class Customer:

    used_ids = set()

    def __init__(
        self,
        id: str,
        first_name: str,
        last_name: str,
        email: str,
        delivery_address: str,
        customer_type: CustomerType,
        customer_discount: float,
        customer_gift: CustomerGift,
    ):
        if id in self.used_ids:
            raise ValueError("ID already used.")
        self.used_ids.add(id)
        self._id = id
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._delivery_address = delivery_address
        self._customer_type = customer_type
        self._customer_discount = customer_discount
        self._list_of_favorite_items: list[OrderItem] = []
        self._customer_gift = customer_gift

    def is_vip(self) -> bool:
        return self._customer_type == CustomerType.VIP

    # Getters
    def get_id(self):
        return self._id

    def get_first_name(self):
        return self._first_name

    def get_last_name(self):
        return self._last_name

    def get_email(self):
        return self._email

    def get_address(self):
        return self._delivery_address

    def get_customer_type(self):
        return self._customer_type

    def get_discount(self):
        return self._customer_discount

    def get_favorites(self):
        return self._list_of_favorite_items

    def get_gift(self):
        return self._customer_gift

    # Setters
    def set_first_name(self, name):
        if not name:
            raise ValueError("First name cannot be empty")
        self._first_name = name

    def set_last_name(self, name):
        if not name:
            raise ValueError("Last name cannot be empty")
        self._last_name = name

    def set_email(self, email):
        if "@" not in email:
            raise ValueError("Invalid email")
        self._email = email

    def set_address(self, address):
        if not address:
            raise ValueError("Address cannot be empty")
        self._delivery_address = address

    def set_discount(self, discount):
        if discount < 0:
            raise ValueError("Discount cannot be negative")
        self._customer_discount = discount

    def take_gift(self, gift):
        self._customer_gift = gift

    def open_gift(self):
        if self._customer_gift:
            self._customer_gift.open_gift()
            self._customer_gift = None
        else:
            print("No gift available.")

    def _find_favorite_by_name(self, item_name: str) -> OrderItem | None:
        for fav in self._list_of_favorite_items:
            if fav._item_name == item_name:
                return fav
        return None

    def add_to_favorites(self, item: OrderItem):
        if self._find_favorite_by_name(item._item_name) is None:
            self._list_of_favorite_items.append(item)
            print(f"{item._item_name} was added to favorites!")
        else:
            print(f"{item._item_name} is already in favorites.")

    def add_items_to_favorites(self, items: list[OrderItem]):
        for item in items:
            self.add_to_favorites(item)

    def remove_from_favorites(self, item: OrderItem):
        found = self._find_favorite_by_name(item._item_name)
        if found:
            self._list_of_favorite_items.remove(found)
            print(f"{item._item_name} was removed from favorites.")
        else:
            print(f"{item._item_name} is not in favorites.")


class Order:

    used_ids = set()

    def __init__(
        self,
        id: str,
        name: str,
        delivery_address: str,
        items: list[OrderItem],
        order_customer: Customer,
        payment_type: PaymentType,
    ):
        if id in self.used_ids:
            raise ValueError("ID already used.")
        self.used_ids.add(id)
        self._id = id
        self._name = name
        self._delivery_address = delivery_address
        self._items = items
        self._order_customer = order_customer
        self._order_total_price: float = self.calculate_total()
        self._payment_type = payment_type
        self._order_date: datetime = datetime.now()
        print("Order created successfully.")
        order_customer.add_items_to_favorites(items)

        # Getters

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_address(self):
        return self._delivery_address

    def get_items(self):
        return self._items

    def get_customer(self):
        return self._order_customer

    def get_total_price(self):
        return self._order_total_price

    def get_payment_type(self):
        return self._payment_type

    def get_order_date(self):
        return self._order_date

    # Setters
    def set_name(self, name):
        if not name:
            raise ValueError("Order name cannot be empty")
        self._name = name

    def set_address(self, address):
        if not address:
            raise ValueError("Address cannot be empty")
        self._delivery_address = address

    def set_payment_type(self, payment_type):
        if not isinstance(payment_type, PaymentType):
            raise ValueError("Invalid payment type")
        self._payment_type = payment_type

    def set_items(self, items):
        if not items:
            raise ValueError("Order must have items")
        self._items = items

        # Recalculate price after changing items
        self._order_total_price = self.calculate_total()

    def calculate_total(self) -> float:
        total = sum(o._item_price for o in self._items)
        return total


class VIPOrder(Order):

    def calculate_total(self) -> float:
        if not self._order_customer.is_vip():
            raise ValueError("Customer is not a V.I.P customer")
        total = (1 - self._order_customer.get_discount()) * sum(
            o._item_price for o in self._items
        )
        return total
