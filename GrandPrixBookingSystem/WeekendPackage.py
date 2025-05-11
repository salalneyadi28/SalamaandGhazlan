from datetime import date
from Ticket import Ticket  # Import the base Ticket class


class WeekendPackage(Ticket):
    def __init__(self, ticketID, basePrice, eventDate, includedDays, packageType, isAvailable=True):
        # Initialize attributes from the Ticket parent class
        super().__init__(ticketID, basePrice, eventDate, isAvailable)
        self.includedDays = includedDays  # List of included race days (e.g., ['Friday', 'Saturday'])
        self.packageType = packageType  # Type of package (e.g., 'Standard', 'Premium')

    def calculatePrice(self):
        # Start with base price
        price = self._basePrice
        # Apply 20% markup for Premium packages
        if self.packageType.lower() == 'premium':
            price *= 1.2
        # Add 50 for each extra day beyond the first
        price += 50 * (len(self.includedDays) - 1)
        return price

    def getTicketDetails(self):
        # Get base ticket details from parent class
        details = super().getTicketDetails()
        # Add WeekendPackage-specific details
        details["Included Days"] = self.includedDays
        details["Package Type"] = self.packageType
        details["Final Price"] = self.calculatePrice()
        return details


# Test the class with two sample users
if __name__ == "__main__":
    # Salama chooses a Premium weekend package with 3 days
    salama_ticket = WeekendPackage(
        ticketID=2001,
        basePrice=300.0,
        eventDate=date(2025, 12, 1),
        includedDays=["Friday", "Saturday", "Sunday"],
        packageType="Premium"
    )

    # Ghazlan chooses a Standard package with 2 days
    ghazlan_ticket = WeekendPackage(
        ticketID=2002,
        basePrice=300.0,
        eventDate=date(2025, 12, 1),
        includedDays=["Saturday", "Sunday"],
        packageType="Standard"
    )

    # Print ticket details for both users
    print("Salama Alneyadi's Weekend Package:")
    print(salama_ticket.getTicketDetails())

    print("\nGhazlan Alketbi's Weekend Package:")
    print(ghazlan_ticket.getTicketDetails())

    # --- Persistence using pickle ---
    import pickle
    import os


    # Function to save a list of WeekendPackage tickets to a pickle file
    def save_weekend_packages(packages, filename='weekend_packages.pkl'):
        with open(filename, 'wb') as file:
            pickle.dump(packages, file)


    # Function to load a list of WeekendPackage tickets from a pickle file
    def load_weekend_packages(filename='weekend_packages.pkl'):
        if os.path.exists(filename):
            with open(filename, 'rb') as file:
                return pickle.load(file)
        return []


    # Save the created weekend tickets
    weekend_list = [salama_ticket, ghazlan_ticket]
    save_weekend_packages(weekend_list)
    print("\nWeekend packages saved to weekend_packages.pkl")

    # Load and display them to verify
    loaded_packages = load_weekend_packages()
    print("\n--- Loaded Weekend Packages ---")
    for pkg in loaded_packages:
        print(pkg.getTicketDetails())
