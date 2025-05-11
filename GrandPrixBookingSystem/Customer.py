import pickle  # Used for saving and loading objects in binary format
import os      # Used to check if the file exists


# User class defines basic user information
class User:
   def __init__(self, user_id, username, password, email, phone_number):
       self._userID = user_id               # Unique user ID
       self._username = username            # Username
       self._password = password            # Password
       self._email = email                  # Email address
       self._phoneNumber = phone_number     # Phone number


   # Getter methods
   def get_userID(self):
       return self._userID


   def get_username(self):
       return self._username


   def get_password(self):
       return self._password


   def get_email(self):
       return self._email


   def get_phoneNumber(self):
       return self._phoneNumber


   # Setter methods
   def set_userID(self, user_id):
       self._userID = user_id


   def set_username(self, username):
       self._username = username


   def set_password(self, password):
       self._password = password


   def set_email(self, email):
       self._email = email


   def set_phoneNumber(self, phone_number):
       self._phoneNumber = phone_number


# Function to load users from binary file
def load_users():
   if os.path.exists('users.pkl'):  # Check if file exists
       with open('users.pkl', 'rb') as file:  # Open file in read-binary mode
           return pickle.load(file)           # Load and return user list
   return []  # Return empty list if file does not exist


# Function to save user list to binary file
def save_users(users):
   with open('users.pkl', 'wb') as file:  # Open file in write-binary mode
       pickle.dump(users, file)           # Save the users list


# Customer class extends User and adds more attributes
class Customer(User):
   def __init__(self, user_id, username, password, email, phone_number, first_name, last_name):
       super().__init__(user_id, username, password, email, phone_number)  # Call parent constructor
       self._first_name = first_name      # Customer's first name
       self._last_name = last_name        # Customer's last name
       self._order_history = []           # List to store order history


   # Getter methods for Customer class
   def get_first_name(self):
       return self._first_name


   def get_last_name(self):
       return self._last_name


   def get_order_history(self):
       return self._order_history


   # Setter methods for Customer class
   def set_first_name(self, first_name):
       self._first_name = first_name


   def set_last_name(self, last_name):
       self._last_name = last_name


   def set_order_history(self, order_history):
       self._order_history = order_history


   # Method to create and save a new account
   def createAccount(self, details):
       try:
           self.set_email(details.get('email', self._email))  # Update email if provided
           self.set_phoneNumber(details.get('phone_number', self._phoneNumber))  # Update phone number if provided
           self.set_first_name(details.get('first_name', self._first_name))  # Update first name if provided
           self.set_last_name(details.get('last_name', self._last_name))  # Update last name if provided


           users = load_users()  # Load current users
           users.append(self)    # Add this customer
           save_users(users)     # Save updated users list
           return True
       except Exception as e:
           print(f"Error creating account: {e}")  # Print error message
           return False


   # Method to view account details
   def viewAccount(self):
       return {
           'user_id': self.get_userID(),              # Return user ID
           'username': self.get_username(),           # Return username
           'email': self.get_email(),                 # Return email
           'phone_number': self.get_phoneNumber(),    # Return phone number
           'first_name': self.get_first_name(),       # Return first name
           'last_name': self.get_last_name()          # Return last name
       }


   # Method to update account details
   def modifyAccount(self, details):
       try:
           self.set_email(details.get('email', self._email))  # Update email
           self.set_phoneNumber(details.get('phone_number', self._phoneNumber))  # Update phone number
           self.set_password(details.get('password', self._password))  # Update password
           self.set_first_name(details.get('first_name', self._first_name))  # Update first name
           self.set_last_name(details.get('last_name', self._last_name))  # Update last name


           users = load_users()  # Load all users
           for i, user in enumerate(users):  # Loop to find this user
               if user.get_userID() == self.get_userID():
                   users[i] = self  # Replace with updated user
                   break
           save_users(users)  # Save updated list
           return True
       except Exception as e:
           print(f"Error modifying account: {e}")  # Print error message
           return False


   # Method to delete the current account
   def deleteAccount(self):
       try:
           users = load_users()  # Load current users
           users = [user for user in users if user.get_userID() != self.get_userID()]  # Remove this user
           save_users(users)  # Save updated users list
           return True
       except Exception as e:
           print(f"Error deleting account: {e}")  # Print error message
           return False


   # Method to return all past orders
   def viewOrderHistory(self):
       return self.get_order_history()  # Return list of orders


   # Method to place a new order (simulated)
   def placeOrder(self, tickets, payment):
       try:
           order_id = len(self.get_order_history()) + 1  # Generate order ID
           order = {
               'order_id': order_id,  # Order ID
               'user_id': self.get_userID(),  # User ID
               'tickets': tickets,  # Tickets list
               'payment': payment  # Payment method
           }
           self.set_order_history(self.get_order_history() + [order])  # Add to order history


           users = load_users()  # Load all users
           for i, user in enumerate(users):  # Find and update this user
               if user.get_userID() == self.get_userID():
                   users[i] = self  # Update user
                   break
           save_users(users)  # Save updated list
           return order
       except Exception as e:
           print(f"Error placing order: {e}")  # Print error message
           return None


# Test code runs only when this file is executed directly
if __name__ == "__main__":
   # Create first customer: Salama Alneyadi
   salama = Customer(
       user_id=1,
       username="salama",
       password="1234",
       email="salama@example.com",
       phone_number="0501111111",
       first_name="Salama",
       last_name="Alneyadi"
   )
   print("Creating Salama's account...")
   print("Account created:", salama.createAccount({
       'email': "salama@example.com",
       'phone_number': "0501111111",
       'first_name': "Salama",
       'last_name': "Alneyadi"
   }))
   print("Account info:", salama.viewAccount())


   # Create second customer: Ghazlan Alketbi
   ghazlan = Customer(
       user_id=2,
       username="ghazlan",
       password="abcd",
       email="ghazlan@example.com",
       phone_number="0502222222",
       first_name="Ghazlan",
       last_name="Alketbi"
   )
   print("\nCreating Ghazlan's account...")
   print("Account created:", ghazlan.createAccount({
       'email': "ghazlan@example.com",
       'phone_number': "0502222222",
       'first_name': "Ghazlan",
       'last_name': "Alketbi"
   }))
   print("Account info:", ghazlan.viewAccount())


   # Salama places an order
   print("\nSalama places an order...")
   order = salama.placeOrder(tickets=["Standard Ticket"], payment="Credit Card")
   print("Order:", order)


   # View Salama’s order history
   print("\nSalama's order history:")
   print(salama.viewOrderHistory())


   # Ghazlan places an order
   print("\nGhazlan places an order...")
   order2 = ghazlan.placeOrder(tickets=["VIP Ticket", "Standard Ticket"], payment="Apple Pay")
   print("Order:", order2)


   # View Ghazlan’s order history
   print("\nGhazlan's order history:")
   print(ghazlan.viewOrderHistory())