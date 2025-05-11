from datetime import date
import pickle
import os

# Event class to manage event information and ticket sales
class Event:
    def __init__(self, eventID, eventName, eventDate, location, totalCapacity, soldTickets=0):
        # Initialize the event details using setters
        self.setEventID(eventID)
        self.setEventName(eventName)
        self.setEventDate(eventDate)
        self.setLocation(location)
        self.setTotalCapacity(totalCapacity)
        self.setSoldTickets(soldTickets)

    # Setters and getters for encapsulated event attributes
    def setEventID(self, eventID):
        self.__eventID = eventID

    def getEventID(self):
        return self.__eventID

    def setEventName(self, eventName):
        self.__eventName = eventName

    def getEventName(self):
        return self.__eventName

    def setEventDate(self, eventDate):
        self.__eventDate = eventDate

    def getEventDate(self):
        return self.__eventDate

    def setLocation(self, location):
        self.__location = location

    def getLocation(self):
        return self.__location

    def setTotalCapacity(self, totalCapacity):
        self.__totalCapacity = totalCapacity

    def getTotalCapacity(self):
        return self.__totalCapacity

    def setSoldTickets(self, soldTickets):
        self.__soldTickets = soldTickets

    def getSoldTickets(self):
        return self.__soldTickets

    # Returns the number of tickets still available
    def getAvailableTickets(self):
        return self.getTotalCapacity() - self.getSoldTickets()

    # Updates sold ticket count if within capacity, otherwise prints an error
    def updateSoldTickets(self, count):
        if self.getSoldTickets() + count <= self.getTotalCapacity():
            self.setSoldTickets(self.getSoldTickets() + count)
        else:
            print("Not enough tickets available!")  # Error message for exceeding capacity
        return self.getSoldTickets()

    # Returns event details in a dictionary format for easy access
    def getEventDetails(self):
        return {
            "Event ID": self.getEventID(),
            "Event Name": self.getEventName(),
            "Event Date": self.getEventDate().strftime('%Y-%m-%d'),  # Format date to string
            "Location": self.getLocation(),
            "Total Capacity": self.getTotalCapacity(),
            "Sold Tickets": self.getSoldTickets(),
            "Available Tickets": self.getAvailableTickets()
        }

# Function to save list of events to a pickle file
def save_events(events, filename='events.pkl'):
    with open(filename, 'wb') as file:  # Open file in binary write mode
        pickle.dump(events, file)  # Save the event list using pickle

# Function to load list of events from a pickle file
def load_events(filename='events.pkl'):
    if os.path.exists(filename):  # Check if the file exists
        with open(filename, 'rb') as file:  # Open file in binary read mode
            return pickle.load(file)  # Load the event list from the file
    return []  # Return an empty list if the file doesn't exist

# Test block for Event functionality
if __name__ == "__main__":
    print("\n--- Event Test for Salama Alneyadi ---")
    # Create an event instance
    salama_event = Event(
        eventID=101,
        eventName="Grand Prix Abu Dhabi",
        eventDate=date(2025, 11, 15),
        location="Yas Marina Circuit",
        totalCapacity=5000,
        soldTickets=1200
    )
    print("Before Purchase:", salama_event.getAvailableTickets(), "tickets left")
    salama_event.updateSoldTickets(3)  # Purchase 3 tickets
    print("After Purchase:", salama_event.getAvailableTickets(), "tickets left")
    print("Event Details:", salama_event.getEventDetails())  # Print event details

    print("\n--- Event Test for Ghazlan Alketbi ---")
    # Another event instance
    ghazlan_event = Event(
        eventID=102,
        eventName="Desert Music Festival",
        eventDate=date(2025, 12, 20),
        location="Liwa Oasis",
        totalCapacity=3000,
        soldTickets=2900
    )
    print("Before Purchase:", ghazlan_event.getAvailableTickets(), "tickets left")
    ghazlan_event.updateSoldTickets(50)  # Try purchasing 50 tickets (will fail)
    print("After Attempted Purchase:", ghazlan_event.getAvailableTickets(), "tickets left")
    print("Event Details:", ghazlan_event.getEventDetails())  # Print event details

    print("\n--- Saving and Loading Sample Events ---")
    # Create more sample events
    event1 = Event(201, "AI Conference 2025", date(2025, 10, 1), "Dubai Expo Center", 2000, 150)
    event2 = Event(202, "Winter Gala", date(2025, 12, 5), "Emirates Palace", 1000, 750)

    save_events([event1, event2])  # Save events to file
    print("Events saved to events.pkl")

    loaded_events = load_events()  # Load events from file
    for e in loaded_events:  # Print the details of the loaded events
        print(e.getEventDetails())
