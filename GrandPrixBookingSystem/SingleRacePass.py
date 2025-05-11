from datetime import date  # Import the 'date' class from the 'datetime' module to handle dates
from Ticket import Ticket  # Import the 'Ticket' class from the Ticket module

class SingleRacePass(Ticket):  # Define a new class SingleRacePass that inherits from the Ticket class
    def __init__(self, ticketID, basePrice, eventDate, raceDay, seatLocation, isAvailable=True):
        # Call the parent class (Ticket) constructor using super() to initialize ticketID, basePrice, eventDate, and isAvailable
        super().__init__(ticketID, basePrice, eventDate, isAvailable)
        # Initialize additional attributes specific to SingleRacePass
        self._raceDay = raceDay  # Store the race day (e.g., 'Friday')
        self._seatLocation = seatLocation  # Store the seat location (e.g., 'VIP', 'Standard')

    def calculatePrice(self):
        # Method to calculate the final ticket price based on the seat location
        if self._seatLocation.lower() == "vip":  # If the seat location is 'VIP'
            return self._basePrice * 1.2  # Increase price by 20% for VIP
        elif self._seatLocation.lower() == "premium":  # If the seat location is 'premium'
            return self._basePrice * 1.1  # Increase price by 10% for premium
        else:  # For any other seat location (e.g., 'Standard')
            return self._basePrice  # Return the base price (no adjustment)

    def getTicketDetails(self):
        # Method to return all ticket details as a dictionary
        base_details = super().getTicketDetails()  # Get the base ticket details from the parent class
        # Update the dictionary with additional details specific to SingleRacePass
        base_details.update({
            "Race Day": self._raceDay,  # Add race day to the details
            "Seat Location": self._seatLocation,  # Add seat location to the details
            "Final Price": self.calculatePrice()  # Add the calculated final price to the details
        })
        return base_details  # Return the updated dictionary with all details

#test code
if __name__ == "__main__":
    # Salama Alneyadi
    salama_ticket = SingleRacePass(1001, 200.0, date(2025, 12, 1), "Friday", "VIP")
    # Print the ticket details for Salama Alneyadi
    print("Salama Alneyadi's Ticket:")
    print(salama_ticket.getTicketDetails())  # Print all the details including final price

    # Ghazlan Alketbi
    ghazlan_ticket = SingleRacePass(1002, 200.0, date(2025, 12, 1), "Saturday", "Standard")
    # Print the ticket details for Ghazlan Alketbi
    print("\nGhazlan Alketbi's Ticket:")
    print(ghazlan_ticket.getTicketDetails())  # Print all the details including final price
