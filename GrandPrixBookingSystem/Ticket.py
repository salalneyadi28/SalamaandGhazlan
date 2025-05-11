from datetime import date

class Ticket:
    def __init__(self, ticketID, basePrice, eventDate, isAvailable=True):
        self._ticketID = ticketID
        self._basePrice = basePrice
        self._eventDate = eventDate
        self._isAvailable = isAvailable

    # Getter and Setter for ticketID
    def get_ticketID(self):
        return self._ticketID

    def set_ticketID(self, ticketID):
        self._ticketID = ticketID

    # Getter and Setter for basePrice
    def get_basePrice(self):
        return self._basePrice

    def set_basePrice(self, basePrice):
        self._basePrice = basePrice

    # Getter and Setter for eventDate
    def get_eventDate(self):
        return self._eventDate

    def set_eventDate(self, eventDate):
        self._eventDate = eventDate

    # Getter and Setter for isAvailable
    def get_isAvailable(self):
        return self._isAvailable

    def set_isAvailable(self, isAvailable):
        self._isAvailable = isAvailable

    # Method to calculate ticket price (can be extended later)
    def calculatePrice(self):
        return self._basePrice

    # Check if the ticket is valid
    def isValid(self):
        return self._isAvailable and self._eventDate >= date.today()

    # Return ticket details as a dictionary
    def getTicketDetails(self):
        return {
            "Ticket ID": self._ticketID,
            "Base Price": self._basePrice,
            "Event Date": self._eventDate.isoformat(),
            "Available": self._isAvailable,
            "Valid": self.isValid()
        }
if __name__ == "__main__":
    from datetime import date

    # Create ticket instances
    ticket1 = Ticket(101, 100.0, date(2025, 5, 15))
    ticket2 = Ticket(102, 75.0, date(2024, 5, 1), False)

    # Use setters to update ticket2 basePrice
    ticket2.set_basePrice(80.0)

    # Use getters to access values
    print("Ticket 1 ID:", ticket1.get_ticketID())
    print("Ticket 1 Price:", ticket1.calculatePrice())
    print("Ticket 1 Valid:", ticket1.isValid())
    print("Ticket 1 Details:", ticket1.getTicketDetails())

    print("\nTicket 2 ID:", ticket2.get_ticketID())
    print("Ticket 2 Updated Price:", ticket2.get_basePrice())
    print("Ticket 2 Valid:", ticket2.isValid())
    print("Ticket 2 Details:", ticket2.getTicketDetails())

import pickle
import os

# Function to save list of tickets to a pickle file
def save_tickets(tickets, filename='tickets.pkl'):
    with open(filename, 'wb') as file:
        pickle.dump(tickets, file)

# Function to load list of tickets from a pickle file
def load_tickets(filename='tickets.pkl'):
    if os.path.exists(filename):
        with open(filename, 'rb') as file:
            return pickle.load(file)
    return []

# Run this block to create the pickle file
if __name__ == "__main__":
    from datetime import date

    # Create ticket instances
    ticket1 = Ticket(101, 100.0, date(2025, 5, 15))
    ticket2 = Ticket(102, 80.0, date(2024, 5, 1), isAvailable=False)
    ticket3 = Ticket(103, 120.0, date(2025, 6, 10))

    # Save tickets to pickle file
    ticket_list = [ticket1, ticket2, ticket3]
    save_tickets(ticket_list)
    print("Tickets saved to tickets.pkl")

    # Load tickets back (optional check)
    loaded_tickets = load_tickets()
    for t in loaded_tickets:
        print(t.getTicketDetails())
