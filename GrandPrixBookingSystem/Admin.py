#Base User Class

class User:
    """Base class for all users."""
    def __init__(self, user_id, username, password, email, phone_number):
        self._userID = user_id
        self._username = username
        self._password = password
        self._email = email
        self._phoneNumber = phone_number

    def get_userID(self): return self._userID
    def set_userID(self, user_id): self._userID = user_id

    def get_username(self): return self._username
    def set_username(self, username): self._username = username

    def get_password(self): return self._password
    def set_password(self, password): self._password = password

    def get_email(self): return self._email
    def set_email(self, email): self._email = email

    def get_phoneNumber(self): return self._phoneNumber
    def set_phoneNumber(self, phone_number): self._phoneNumber = phone_number

# === Customer Class ===

class Customer(User):
    """Customer class that extends User with additional info."""
    def __init__(self, user_id, username, password, email, phone_number, first_name, last_name):
        super().__init__(user_id, username, password, email, phone_number)
        self._first_name = first_name
        self._last_name = last_name
        self._order_history = []
        self._discount = 0  # Default discount

    def get_first_name(self): return self._first_name
    def set_first_name(self, first_name): self._first_name = first_name

    def get_last_name(self): return self._last_name
    def set_last_name(self, last_name): self._last_name = last_name

    def get_order_history(self): return self._order_history
    def set_order_history(self, history): self._order_history = history

    def set_discount(self, discount): self._discount = discount
    def get_discount(self): return self._discount

    def placeOrder(self, tickets_count, payment_amount):
        """Place an order, apply discount, and save order."""
        discounted_amount = payment_amount * (1 - self._discount / 100)
        self._order_history.append({
            "tickets": tickets_count,
            "payment": discounted_amount
        })
        return {"status": "Order successful", "paid": discounted_amount}

    def get_customer_info(self):
        return f"ID: {self.get_userID()}, Username: {self.get_username()}, Name: {self._first_name} {self._last_name}, Email: {self.get_email()}, Phone: {self.get_phoneNumber()}"

    def __str__(self):
        return self.get_customer_info()

# === Admin Class ===

class Admin(User):
    """Admin class with staff privileges."""
    def __init__(self, user_id, username, password, email, phone_number, staff_id):
        super().__init__(user_id, username, password, email, phone_number)
        self._staffID = staff_id
        self._discount = 0
        self._customers = []
        self._total_sales = 0
        self._tickets_sold = 0

    def get_staffID(self): return self._staffID
    def set_staffID(self, staff_id): self._staffID = staff_id

    def add_customer(self, customer):
        self._customers.append(customer)

    def viewAllCustomers(self):
        return self._customers

    def modifyDiscounts(self, discount):
        self._discount = discount
        for customer in self._customers:
            customer.set_discount(discount)
        return True

    def trackTicketSales(self):
        self._tickets_sold = sum(sum(order["tickets"] for order in c.get_order_history()) for c in self._customers)
        return self._tickets_sold

    def viewSalesReport(self):
        self._total_sales = sum(sum(order["payment"] for order in c.get_order_history()) for c in self._customers)
        return {
            "total_sales": self._total_sales,
            "tickets_sold": self._tickets_sold,
            "discount": self._discount
        }

# === Main Test Code ===

if __name__ == "__main__":
    # Create customers
    customer1 = Customer(1, "salama1", "pass123", "salama@email.com", "0501111111", "Salama", "Alneyadi")
    customer2 = Customer(2, "ghazlan1", "pass456", "ghazlan@email.com", "0502222222", "Ghazlan", "Alketbi")

    # Create admin and register customers
    admin = Admin(99, "adminuser", "adminpass", "admin@email.com", "0500000000", "STAFF001")
    admin.add_customer(customer1)
    admin.add_customer(customer2)

    # Place orders
    customer1.placeOrder(3, 150)
    customer2.placeOrder(2, 100)

    # Admin modifies discount
    print("\nModify Discount to 10%:")
    admin.modifyDiscounts(10)

    # Place more orders after discount
    customer1.placeOrder(1, 50)
    customer2.placeOrder(1, 70)

    # Show and modify admin staff ID
    print("\nInitial Staff ID:", admin.get_staffID())
    admin.set_staffID("STAFF999")
    print("Updated Staff ID:", admin.get_staffID())

    # Display all customer info
    print("\nAll Customers:")
    for c in admin.viewAllCustomers():
        print(c)

    # Display sales report
    print("\nSales Report:")
    print(admin.viewSalesReport())

    # Display number of tickets sold
    print("\nTickets Sold:")
    print(admin.trackTicketSales())
