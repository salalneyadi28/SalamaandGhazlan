from datetime import date
import pickle
import os

# Discount class to apply date-based discount codes
class Discount:
    def __init__(self, discountCode, discountPercentage, validFrom, validUntil, isActive):
        self.setDiscountCode(discountCode)
        self.setDiscountPercentage(discountPercentage)
        self.setValidFrom(validFrom)
        self.setValidUntil(validUntil)
        self.setIsActive(isActive)

    def setDiscountCode(self, code):
        self.__discountCode = code

    def getDiscountCode(self):
        return self.__discountCode

    def setDiscountPercentage(self, percentage):
        if 0 <= percentage <= 100:
            self.__discountPercentage = percentage
        else:
            raise ValueError("Discount percentage must be between 0 and 100")

    def getDiscountPercentage(self):
        return self.__discountPercentage

    def setValidFrom(self, validFrom):
        self.__validFrom = validFrom

    def getValidFrom(self):
        return self.__validFrom

    def setValidUntil(self, validUntil):
        self.__validUntil = validUntil

    def getValidUntil(self):
        return self.__validUntil

    def setIsActive(self, status):
        self.__isActive = status

    def getIsActive(self):
        return self.__isActive

    def isValid(self):
        today = date.today()
        return self.getIsActive() and self.getValidFrom() <= today <= self.getValidUntil()

    def applyDiscount(self, price):
        if self.isValid():
            discount = price * (self.getDiscountPercentage() / 100)
            return price - discount
        return price

    def __str__(self):
        return f"{self.__discountCode} ({self.__discountPercentage}% off, valid from {self.__validFrom} to {self.__validUntil}, active: {self.__isActive})"

# Sample Order class with discount integration
class Order:
    def __init__(self, customerName, items, prices):
        self.customerName = customerName
        self.items = items
        self.prices = prices
        self._discount = None
        self._totalAmount = self.calculateTotal()

    def calculateTotal(self):
        return sum(self.prices)

    def applyDiscount(self, discount):
        if discount and discount.isValid():
            self._discount = discount
            discounted_total = discount.applyDiscount(self.calculateTotal())
            self._totalAmount = discounted_total
        return self._totalAmount

    def getOrderDetails(self):
        details = {
            "Customer Name": self.customerName,
            "Items": self.items,
            "Prices": self.prices,
            "Original Total": self.calculateTotal(),
            "Discount Applied": self._discount.getDiscountCode() if self._discount else "None",
            "Final Amount": self._totalAmount
        }
        return details

# Save a list of discounts to a file using pickle
def save_discounts(discounts, filename='discounts.pkl'):
    with open(filename, 'wb') as file:
        pickle.dump(discounts, file)

# Load a list of discounts from a pickle file
def load_discounts(filename='discounts.pkl'):
    if os.path.exists(filename):
        with open(filename, 'rb') as file:
            return pickle.load(file)
    return []

# Sample test code for Discount and Order
if __name__ == "__main__":
    print("Discount Test for Salama Alneyadi")
    salama_discount = Discount(
        discountCode="EID2025",
        discountPercentage=15.0,
        validFrom=date(2025, 5, 1),
        validUntil=date(2025, 5, 31),
        isActive=True
    )

    salama_order = Order(
        customerName="Salama Alneyadi",
        items=["Gold Ticket", "Food Package"],
        prices=[200.0, 50.0]
    )

    salama_order.applyDiscount(salama_discount)
    for key, value in salama_order.getOrderDetails().items():
        print(f"{key}: {value}")

    print("\nDiscount Test for Ghazlan Alketbi")
    ghazlan_discount = Discount(
        discountCode="SPRING2025",
        discountPercentage=20.0,
        validFrom=date(2025, 4, 1),
        validUntil=date(2025, 4, 30),
        isActive=True
    )

    ghazlan_order = Order(
        customerName="Ghazlan Alketbi",
        items=["Standard Ticket", "Souvenir"],
        prices=[180.0, 20.0]
    )

    ghazlan_order.applyDiscount(ghazlan_discount)
    for key, value in ghazlan_order.getOrderDetails().items():
        print(f"{key}: {value}")

    # Save discounts to file
    all_discounts = [salama_discount, ghazlan_discount]
    save_discounts(all_discounts)

    print("\nLoaded Discounts:")
    loaded = load_discounts()
    for d in loaded:
        print(f"{d.getDiscountCode()} - Valid today? {d.isValid()} - {d.getDiscountPercentage()}% off")
