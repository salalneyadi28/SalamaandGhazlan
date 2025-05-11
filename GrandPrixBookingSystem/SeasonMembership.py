from datetime import date
import pickle  # For saving/loading ticket objects

# Base Ticket class
class Ticket:
    def __init__(self, ticketID, basePrice, eventDate, isAvailable=True):
        self._ticketID = ticketID
        self._basePrice = basePrice
        self._eventDate = eventDate
        self._isAvailable = isAvailable

    # Getters and setters
    def get_ticketID(self):
        return self._ticketID

    def set_ticketID(self, ticketID):
        self._ticketID = ticketID

    def get_basePrice(self):
        return self._basePrice

    def set_basePrice(self, basePrice):
        self._basePrice = basePrice

    def get_eventDate(self):
        return self._eventDate

    def set_eventDate(self, eventDate):
        self._eventDate = eventDate

    def get_isAvailable(self):
        return self._isAvailable

    def set_isAvailable(self, isAvailable):
        self._isAvailable = isAvailable

    # Calculates price (default to base price)
    def calculatePrice(self):
        return self._basePrice

    # Checks if the ticket is still valid
    def isValid(self):
        return self._isAvailable and self._eventDate >= date.today()

    # Returns ticket information as a dictionary
    def getTicketDetails(self):
        return {
            "Ticket ID": self._ticketID,
            "Base Price": self._basePrice,
            "Event Date": self._eventDate.isoformat(),
            "Available": self._isAvailable,
            "Valid": self.isValid()
        }

# SeasonMembership subclass inheriting from Ticket
class SeasonMembership(Ticket):
    def __init__(self, ticketID, basePrice, eventDate, validFrom, validUntil, membershipLevel, isAvailable=True):
        super().__init__(ticketID, basePrice, eventDate, isAvailable)
        self.validFrom = validFrom                # Start date of membership validity
        self.validUntil = validUntil              # End date of membership validity
        self.membershipLevel = membershipLevel    # Membership level: "Standard" or "VIP"

    # Calculate total season price based on membership level and duration
    def calculatePrice(self):
        duration_months = (self.validUntil.year - self.validFrom.year) * 12 + (self.validUntil.month - self.validFrom.month) + 1
        multiplier = 1.5 if self.membershipLevel.lower() == "vip" else 1.2
        return round(self._basePrice * duration_months * multiplier, 2)

    # Returns a list of upcoming events within the membership validity period
    def getRemainingEvents(self, allEvents):
        return [event for event in allEvents if self.validFrom <= event["date"] <= self.validUntil and event["date"] >= date.today()]

    # Extends base ticket details with membership-specific info
    def getTicketDetails(self):
        details = super().getTicketDetails()
        details.update({
            "Valid From": self.validFrom.isoformat(),
            "Valid Until": self.validUntil.isoformat(),
            "Membership Level": self.membershipLevel,
            "Final Price": self.calculatePrice()
        })
        return details

# --- Testing the SeasonMembership class ---

# Sample upcoming events
upcoming_events = [
    {"name": "Race 1", "date": date(2025, 6, 1)},
    {"name": "Race 2", "date": date(2025, 7, 15)},
    {"name": "Race 3", "date": date(2025, 10, 5)},
    {"name": "Race 4", "date": date(2026, 1, 10)}
]

# Create SeasonMembership for Salama (VIP level)
salama_ticket = SeasonMembership(
    ticketID=3001,
    basePrice=100.0,
    eventDate=date(2025, 5, 20),
    validFrom=date(2025, 6, 1),
    validUntil=date(2025, 12, 31),
    membershipLevel="VIP"
)

# Create SeasonMembership for Ghazlan (Standard level)
ghazlan_ticket = SeasonMembership(
    ticketID=3002,
    basePrice=100.0,
    eventDate=date(2025, 5, 20),
    validFrom=date(2025, 6, 1),
    validUntil=date(2025, 10, 31),
    membershipLevel="Standard"
)

# Print ticket details and remaining events
print("Salama Alneyadi's Season Membership:")
print(salama_ticket.getTicketDetails())
print("Remaining Events:", salama_ticket.getRemainingEvents(upcoming_events))

print("\nGhazlan Alketbi's Season Membership:")
print(ghazlan_ticket.getTicketDetails())
print("Remaining Events:", ghazlan_ticket.getRemainingEvents(upcoming_events))

# Save both tickets to a pickle file
with open("season_tickets.pkl", "wb") as file:
    pickle.dump([salama_ticket, ghazlan_ticket], file)

# Load tickets back from pickle file
with open("season_tickets.pkl", "rb") as file:
    loaded_tickets = pickle.load(file)

# Display loaded ticket details
print("\nLoaded Season Membership Tickets from Pickle File:")
for ticket in loaded_tickets:
    print(ticket.getTicketDetails())
