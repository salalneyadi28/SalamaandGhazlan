import pickle
import os
from datetime import date
from typing import List, Dict

# Define the Customer class
class Customer:
    def __init__(self, customerID: int, name: str):
        self._customerID = customerID
        self._name = name

    def getCustomerID(self) -> int:
        return self._customerID

    def setCustomerID(self, customerID: int):
        self._customerID = customerID

    def getName(self) -> str:
        return self._name

    def setName(self, name: str):
        self._name = name

    def __str__(self):
        return f"Customer[{self._customerID}] {self._name}"

# Define the Ticket class
class Ticket:
    def __init__(self, ticketID: int, price: float):
        self._ticketID = ticketID
        self._price = price

    def getTicketID(self) -> int:
        return self._ticketID

    def setTicketID(self, ticketID: int):
        self._ticketID = ticketID

    def getPrice(self) -> float:
        return self._price

    def setPrice(self, price: float):
        self._price = price

    def __str__(self):
        return f"Ticket[{self._ticketID}]: ${self._price:.2f}"

# Define the Payment class
class Payment:
    def __init__(self, paymentID: int, amount: float, paymentDate: date, paymentStatus: str = "Pending"):
        self._paymentID = paymentID
        self._amount = amount
        self._paymentDate = paymentDate
        self._paymentStatus = paymentStatus

    def getPaymentID(self) -> int:
        return self._paymentID

    def setPaymentID(self, paymentID: int):
        self._paymentID = paymentID

    def getAmount(self) -> float:
        return self._amount

    def setAmount(self, amount: float):
        self._amount = amount

    def getPaymentDate(self) -> date:
        return self._paymentDate

    def setPaymentDate(self, paymentDate: date):
        self._paymentDate = paymentDate

    def getPaymentStatus(self) -> str:
        return self._paymentStatus

    def setPaymentStatus(self, paymentStatus: str):
        self._paymentStatus = paymentStatus

    def getPaymentDetails(self) -> Dict[str, str]:
        return {
            "Payment ID": self.getPaymentID(),
            "Amount": self.getAmount(),
            "Payment Date": self.getPaymentDate().isoformat(),
            "Payment Status": self.getPaymentStatus()
        }

    def __str__(self):
        return f"Payment[{self._paymentID}]: ${self._amount:.2f}, Status: {self._paymentStatus}"

# Define the Order class
class Order:
    def __init__(self, orderID: int, customer: Customer, orderDate: date, paymentMethod: Payment):
        self._orderID = orderID
        self._customer = customer
        self._tickets: List[Ticket] = []
        self._totalAmount: float = 0.0
        self._orderDate = orderDate
        self._status = "Pending"
        self._paymentMethod = paymentMethod

    def getOrderID(self) -> int:
        return self._orderID

    def setOrderID(self, orderID: int):
        self._orderID = orderID

    def getCustomer(self) -> Customer:
        return self._customer

    def setCustomer(self, customer: Customer):
        self._customer = customer

    def getTickets(self) -> List[Ticket]:
        return self._tickets

    def setTickets(self, tickets: List[Ticket]):
        self._tickets = tickets

    def getTotalAmount(self) -> float:
        return self._totalAmount

    def setTotalAmount(self, totalAmount: float):
        self._totalAmount = totalAmount

    def getOrderDate(self) -> date:
        return self._orderDate

    def setOrderDate(self, orderDate: date):
        self._orderDate = orderDate

    def getStatus(self) -> str:
        return self._status

    def setStatus(self, status: str):
        self._status = status

    def getPaymentMethod(self) -> Payment:
        return self._paymentMethod

    def setPaymentMethod(self, paymentMethod: Payment):
        self._paymentMethod = paymentMethod

    def calculateTotal(self) -> float:
        self._totalAmount = sum(ticket.getPrice() for ticket in self._tickets)
        self._paymentMethod.setAmount(self._totalAmount)
        return self._totalAmount

    def addTicket(self, ticket: Ticket) -> "Order":
        if ticket.getTicketID() not in [t.getTicketID() for t in self._tickets]:
            self._tickets.append(ticket)
            self.calculateTotal()
        return self

    def removeTicket(self, ticketID: int) -> "Order":
        original_len = len(self._tickets)
        self._tickets = [t for t in self._tickets if t.getTicketID() != ticketID]
        if len(self._tickets) < original_len:
            self.calculateTotal()
        return self

    def updateStatus(self, status: str) -> str:
        self.setStatus(status)
        return self.getStatus()

    def getOrderDetails(self) -> Dict:
        return {
            "Order ID": self.getOrderID(),
            "Customer": self.getCustomer().getName(),
            "Tickets": [ticket.getTicketID() for ticket in self.getTickets()],
            "Total Amount": self.getTotalAmount(),
            "Order Date": self.getOrderDate().isoformat(),
            "Status": self.getStatus(),
            "Payment": self.getPaymentMethod().getPaymentDetails()
        }

    def __str__(self):
        return f"Order[{self._orderID}] for {self._customer.getName()}, Status: {self._status}, Total: ${self._totalAmount:.2f}"

# Function to save orders to a pickle file
def save_orders(order_list: List[Order], filename: str = "orders.pkl"):
    with open(filename, "wb") as file:
        pickle.dump(order_list, file)

# Function to load orders from a pickle file
def load_orders(filename: str = "orders.pkl") -> List[Order]:
    if os.path.exists(filename):
        with open(filename, "rb") as file:
            return pickle.load(file)
    else:
        return []

# Sample usage
if __name__ == "__main__":
    # Create customer and order for Salama
    salama = Customer(1, "Salama Alneyadi")
    payment_salama = Payment(101, 0.0, date.today())
    order_salama = Order(5001, salama, date.today(), payment_salama)
    order_salama.addTicket(Ticket(201, 100.0))
    order_salama.addTicket(Ticket(202, 150.0))
    order_salama.updateStatus("Confirmed")

    # Create customer and order for Ghazlan
    ghazlan = Customer(2, "Ghazlan Alketbi")
    payment_ghazlan = Payment(102, 0.0, date.today())
    order_ghazlan = Order(5002, ghazlan, date.today(), payment_ghazlan)
    order_ghazlan.addTicket(Ticket(301, 120.0))
    order_ghazlan.addTicket(Ticket(302, 80.0))
    order_ghazlan.removeTicket(301)
    order_ghazlan.updateStatus("Paid")

    # Print orders
    print("Salama Alneyadi's Order:")
    print(order_salama.getOrderDetails())

    print("\nGhazlan Alketbi's Order:")
    print(order_ghazlan.getOrderDetails())

    # Save orders to file
    save_orders([order_salama, order_ghazlan])
    print("\nOrders have been saved to 'orders.pkl'.")
