from datetime import date
import pickle

# Base class for users of the system
class User:
    def __init__(self, username, password):
        self.__username = username
        self.__password = password

    def getUsername(self):
        return self.__username

    def setUsername(self, username):
        self.__username = username

    def getPassword(self):
        return self.__password

    def setPassword(self, password):
        self.__password = password

# Customer inherits from User and adds email attribute
class Customer(User):
    def __init__(self, username, password, email):
        super().__init__(username, password)
        self.__email = email

    def getEmail(self):
        return self.__email

    def setEmail(self, email):
        self.__email = email

# Represents an event in the system
class Event:
    def __init__(self, eventID, eventName, eventDate, location, totalCapacity, soldTickets):
        self.__eventID = eventID
        self.__eventName = eventName
        self.__eventDate = eventDate
        self.__location = location
        self.__totalCapacity = totalCapacity
        self.__soldTickets = soldTickets

    def getEventID(self):
        return self.__eventID

    def setEventID(self, eventID):
        self.__eventID = eventID

    def getEventName(self):
        return self.__eventName

    def setEventName(self, name):
        self.__eventName = name

    def getEventDate(self):
        return self.__eventDate

    def setEventDate(self, eventDate):
        self.__eventDate = eventDate

    def getLocation(self):
        return self.__location

    def setLocation(self, location):
        self.__location = location

    def getTotalCapacity(self):
        return self.__totalCapacity

    def setTotalCapacity(self, capacity):
        self.__totalCapacity = capacity

    def getSoldTickets(self):
        return self.__soldTickets

    def setSoldTickets(self, sold):
        self.__soldTickets = sold

    def getAvailableTickets(self):
        return self.__totalCapacity - self.__soldTickets

    def updateSoldTickets(self, count):
        self.__soldTickets += count
        return self.__soldTickets

    def getEventDetails(self):
        return {
            "eventID": self.__eventID,
            "eventName": self.__eventName,
            "eventDate": self.__eventDate,
            "location": self.__location,
            "totalCapacity": self.__totalCapacity,
            "soldTickets": self.__soldTickets
        }

# Represents a customer's order for an event
class Order:
    def __init__(self, event, ticketType, customer):
        self.__event = event
        self.__ticketType = ticketType
        self.__customer = customer

    def getEvent(self):
        return self.__event

    def getTicketType(self):
        return self.__ticketType

    def getCustomer(self):
        return self.__customer

    def getOrderDetails(self):
        return {
            "event": self.__event.getEventDetails(),
            "ticketType": self.__ticketType,
            "customer": self.__customer.getUsername()
        }

# Represents payment made for an order
class Payment:
    def __init__(self, amount, paymentMethod):
        self.__amount = amount
        self.__paymentMethod = paymentMethod

    def getAmount(self):
        return self.__amount

    def getPaymentMethod(self):
        return self.__paymentMethod

    def getPaymentInfo(self):
        return {
            "amount": self.__amount,
            "paymentMethod": self.__paymentMethod
        }

# Main ticketing system manager
class TicketingSystem:
    def __init__(self):
        self.users = []   # List of all users
        self.events = []  # List of all events
        self.orders = []  # List of all orders

    def registerCustomer(self, details):
        customer = Customer(details["username"], details["password"], details["email"])
        self.users.append(customer)
        return customer

    def loginUser(self, username, password):
        for user in self.users:
            if user.getUsername() == username and user.getPassword() == password:
                return user
        return None

    def searchEvents(self, criteria):
        results = []
        for event in self.events:
            if criteria.get("name") and criteria["name"].lower() in event.getEventDetails()["eventName"].lower():
                results.append(event)
        return results

    def bookTicket(self, event, ticketType, customer):
        if event.getAvailableTickets() > 0:
            event.updateSoldTickets(1)
            order = Order(event, ticketType, customer)
            self.orders.append(order)
            return order
        else:
            return None

    def processPayment(self, order, paymentDetails):
        amount = paymentDetails.get("amount")
        method = paymentDetails.get("method")
        payment = Payment(amount, method)
        return payment

    def generateSalesReport(self):
        report = {}
        for order in self.orders:
            eventName = order.getOrderDetails()["event"]["eventName"]
            if eventName in report:
                report[eventName] += 1
            else:
                report[eventName] = 1
        return report

    def saveSystem(self, filename="ticketing_system.pkl"):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)
        print(f"\nSystem saved to '{filename}'")

    @staticmethod
    def loadSystem(filename="ticketing_system.pkl"):
        try:
            with open(filename, 'rb') as f:
                system = pickle.load(f)
                print(f"\nSystem loaded from '{filename}'")
                return system
        except FileNotFoundError:
            print("\nNo saved system found. Starting a new system.")
            return TicketingSystem()

    def isUserRegistered(self, username):
        return any(user.getUsername() == username for user in self.users)

    def addEvent(self, event):
        for e in self.events:
            if e.getEventID() == event.getEventID():
                return False  # Avoid duplicate event
        self.events.append(event)
        return True

# Run a test scenario if this file is the main script
if __name__ == "__main__":
    system = TicketingSystem.loadSystem()

    # Register or get existing users
    if not system.isUserRegistered("Salama Alneyadi"):
        salama = system.registerCustomer({
            "username": "Salama Alneyadi",
            "password": "pass123",
            "email": "salama.alneyadi@example.com"
        })
    else:
        salama = next(u for u in system.users if u.getUsername() == "Salama Alneyadi")

    if not system.isUserRegistered("Ghazlan Alketbi"):
        ghazlan = system.registerCustomer({
            "username": "Ghazlan Alketbi",
            "password": "pass456",
            "email": "ghazlan.alketbi@example.com"
        })
    else:
        ghazlan = next(u for u in system.users if u.getUsername() == "Ghazlan Alketbi")

    # Add some events (only if not already added)
    system.addEvent(Event(1, "Grand Prix Final", date(2025, 12, 1), "Yas Marina", 100, 0))
    system.addEvent(Event(2, "Qualifiers Day", date(2025, 11, 30), "Yas Marina", 80, 0))

    # Attempt to login
    user = system.loginUser("Salama Alneyadi", "pass123")
    print(f"\nLogin {'successful' if user else 'failed'} for: Salama Alneyadi")

    # Search for events containing "Grand Prix"
    matching_events = system.searchEvents({"name": "Grand Prix"})
    print("\nMatching Events:")
    for event in matching_events:
        print(f"- {event.getEventName()} | {event.getEventDate()} | {event.getLocation()}")

    # Book a ticket if an event was found
    if matching_events:
        event_to_book = matching_events[0]
        order = system.bookTicket(event_to_book, "Standard", user)
        if order:
            print("\nTicket Booked:")
            print(order.getOrderDetails())
            payment = system.processPayment(order, {"amount": 300.0, "method": "Credit Card"})
            print("\nPayment Info:")
            print(payment.getPaymentInfo())
        else:
            print("\nNo tickets available.")
    else:
        print("\nNo events found to book.")

    # Display summary info
    print("\nRegistered Users:")
    for u in system.users:
        print(f"- {u.getUsername()} ({u.getEmail()})")

    print("\nAll Events:")
    for e in system.events:
        print(f"- {e.getEventName()} | {e.getEventDate()} | Sold: {e.getSoldTickets()}/{e.getTotalCapacity()}")

    print("\nAll Orders:")
    for o in system.orders:
        print(f"- {o.getCustomer().getUsername()} booked {o.getEvent().getEventName()} [{o.getTicketType()}]")

    print("\nSales Report:")
    for event, count in system.generateSalesReport().items():
        print(f"- {event}: {count} tickets sold")

    # Save the current system state to a file
    system.saveSystem()
