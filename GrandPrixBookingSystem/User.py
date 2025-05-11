import pickle  # For saving/loading binary data
import os  # For checking file existence

# Load users from file or return an empty list if the file does not exist
def load_users():
    if os.path.exists('users.pkl'):
        with open('users.pkl', 'rb') as file:
            return pickle.load(file)
    return []

# Save users to a binary file
def save_users(users):
    with open('users.pkl', 'wb') as file:
        pickle.dump(users, file)

# Load sales data from file or return default data structure
def load_sales_data():
    if os.path.exists('sales_data.pkl'):
        with open('sales_data.pkl', 'rb') as file:
            return pickle.load(file)
    return {"total_sales": 0, "tickets_sold": 0, "discount": 0}

# Save sales data to binary file
def save_sales_data(data):
    with open('sales_data.pkl', 'wb') as file:
        pickle.dump(data, file)

# Base class for all users
class User:
    def __init__(self, user_id, username, password, email, phone_number):
        self._userID = user_id
        self._username = username
        self._password = password
        self._email = email
        self._phoneNumber = phone_number
        self._orderHistory = []

    # Getter and setter for userID
    def get_userID(self):
        return self._userID

    def set_userID(self, user_id):
        self._userID = user_id

    # Getter and setter for username
    def get_username(self):
        return self._username

    def set_username(self, username):
        self._username = username

    # Getter and setter for password
    def get_password(self):
        return self._password

    def set_password(self, password):
        self._password = password

    # Getter and setter for email
    def get_email(self):
        return self._email

    def set_email(self, email):
        self._email = email

    # Getter and setter for phoneNumber
    def get_phoneNumber(self):
        return self._phoneNumber

    def set_phoneNumber(self, phone_number):
        self._phoneNumber = phone_number

    # Getter and setter for orderHistory
    def get_orderHistory(self):
        return self._orderHistory

    def set_orderHistory(self, order_history):
        self._orderHistory = order_history

    # Method to check login credentials
    def login(self, username, password):
        return self._username == username and self._password == password

    # Method to simulate logging out
    def logout(self):
        print(f"{self._username} has logged out.")

    # Method to update user profile using a dictionary
    def updateProfile(self, details):
        for key, value in details.items():
            if key == "userID":
                self.set_userID(value)
            elif key == "username":
                self.set_username(value)
            elif key == "password":
                self.set_password(value)
            elif key == "email":
                self.set_email(value)
            elif key == "phoneNumber":
                self.set_phoneNumber(value)

    # Method to get the order history
    def getOrderHistory(self):
        return self._orderHistory

# Customer inherits from User and can place orders
class Customer(User):
    def __init__(self, user_id, username, password, email, phone_number, first_name, last_name):
        super().__init__(user_id, username, password, email, phone_number)
        self._first_name = first_name
        self._last_name = last_name

    # Getter and setter for first_name
    def get_first_name(self):
        return self._first_name

    def set_first_name(self, first_name):
        self._first_name = first_name

    # Getter and setter for last_name
    def get_last_name(self):
        return self._last_name

    def set_last_name(self, last_name):
        self._last_name = last_name

    # Method to place an order and update sales data
    def placeOrder(self, tickets_count, payment_amount):
        order = {"tickets": tickets_count, "payment": payment_amount}
        self._orderHistory.append(order)
        sales_data = load_sales_data()
        sales_data["tickets_sold"] += tickets_count
        sales_data["total_sales"] += payment_amount
        save_sales_data(sales_data)
        return {"status": "Order successful"}

    # Method to return customer info as a string
    def get_customer_info(self):
        return f"ID: {self.get_userID()}, Username: {self.get_username()}, Name: {self._first_name} {self._last_name}, Email: {self.get_email()}, Phone: {self.get_phoneNumber()}"

# Admin inherits from User and can manage users and sales data
class Admin(User):
    def __init__(self, user_id, username, password, email, phone_number, staff_id):
        super().__init__(user_id, username, password, email, phone_number)
        self._staffID = staff_id

    # Getter and setter for staffID
    def get_staffID(self):
        return self._staffID

    def set_staffID(self, staff_id):
        self._staffID = staff_id

    # Method to view the current sales report
    def viewSalesReport(self):
        return load_sales_data()

    # Method to modify the discount rate in the sales data
    def modifyDiscounts(self, discount):
        try:
            sales_data = load_sales_data()
            sales_data["discount"] = discount
            save_sales_data(sales_data)
            return True
        except Exception as e:
            print(f"Error modifying discount: {e}")
            return False

    # Method to track number of tickets sold
    def trackTicketSales(self):
        sales_data = load_sales_data()
        return sales_data.get("tickets_sold", 0)

    # Method to return a list of all Customer users
    def viewAllCustomers(self):
        users = load_users()
        return [user for user in users if isinstance(user, Customer)]

# Example usage and testing
if __name__ == "__main__":
    # Create customer objects
    customer1 = Customer(1, "salama1", "pass123", "salama@email.com", "0501111111", "Salama", "Alneyadi")
    customer2 = Customer(2, "ghazlan1", "pass456", "ghazlan@email.com", "0502222222", "Ghazlan", "Alketbi")

    # Save users to file
    save_users([customer1, customer2])

    # Place sample orders
    customer1.placeOrder(3, 150)
    customer2.placeOrder(2, 100)

    # Create an admin user
    admin = Admin(99, "adminuser", "adminpass", "admin@email.com", "0500000000", "STAFF001")

    # View and update staff ID
    print("Initial Staff ID:", admin.get_staffID())
    admin.set_staffID("STAFF999")
    print("Updated Staff ID:", admin.get_staffID())

    # View all customers
    print("\nAll Customers:")
    for customer in admin.viewAllCustomers():
        print(customer.get_customer_info())

    # Modify discount value
    print("\nModify Discount to 10%:")
    print("Success:", admin.modifyDiscounts(10))

    # Display the full sales report
    print("\nSales Report:")
    print(admin.viewSalesReport())

    # Show total tickets sold
    print("\nTickets Sold:")
    print(admin.trackTicketSales())

    # Test login and logout
    print("\nLogin Test:")
    print("Customer1 Login Success:", customer1.login("salama1", "pass123"))
    customer1.logout()

    # Test updating customer profile
    customer1.updateProfile({"email": "newemail@example.com", "phoneNumber": "0509999999"})
    print("\nUpdated Email:", customer1.get_email())
    print("Updated Phone Number:", customer1.get_phoneNumber())

    # Display order history for customer1
    print("\nOrder History for Customer1:")
    print(customer1.getOrderHistory())