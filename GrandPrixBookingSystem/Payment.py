from datetime import date  # Import date for handling payment dates

# Payment class definition
class Payment:
    # Constants for status values
    STATUS_PENDING = "Pending"
    STATUS_PROCESSED = "Processed"
    STATUS_REFUNDED = "Refunded"

    # Constructor to initialize payment attributes
    def __init__(self, paymentID, amount, paymentDate):
        self.setPaymentID(paymentID)
        self.setAmount(amount)
        self.setPaymentDate(paymentDate)
        self.__paymentStatus = Payment.STATUS_PENDING  # Default status

    # Setter for payment ID
    def setPaymentID(self, paymentID):
        self.__paymentID = paymentID

    # Getter for payment ID
    def getPaymentID(self):
        return self.__paymentID

    # Setter for payment amount
    def setAmount(self, amount):
        if amount < 0:
            raise ValueError("Amount cannot be negative.")
        self.__amount = amount

    # Getter for payment amount
    def getAmount(self):
        return self.__amount

    # Setter for payment date
    def setPaymentDate(self, paymentDate):
        self.__paymentDate = paymentDate

    # Getter for payment date
    def getPaymentDate(self):
        return self.__paymentDate

    # Setter for payment status
    def setPaymentStatus(self, status):
        self.__paymentStatus = status

    # Getter for payment status
    def getPaymentStatus(self):
        return self.__paymentStatus

    # Method to process the payment
    def processPayment(self):
        self.setPaymentStatus(Payment.STATUS_PROCESSED)
        return f"Payment {self.getPaymentID()} processed successfully."

    # Method to refund the payment (only if it was processed)
    def refundPayment(self):
        if self.getPaymentStatus() == Payment.STATUS_PROCESSED:
            self.setPaymentStatus(Payment.STATUS_REFUNDED)
            return f"Payment {self.getPaymentID()} refunded successfully."
        return f"Payment {self.getPaymentID()} cannot be refunded. Current status: {self.getPaymentStatus()}"

    # Method to return payment details as a dictionary
    def getPaymentDetails(self):
        return {
            "Payment ID": self.getPaymentID(),
            "Amount": self.getAmount(),
            "Payment Date": self.getPaymentDate().isoformat(),
            "Payment Status": self.getPaymentStatus()
        }

# Test case for Salama Alneyadi
salama_payment = Payment(1001, 750.0, date(2025, 5, 10))
print("Salama Alneyadi's Payment")
print(salama_payment.processPayment())  # Processing the payment
print(salama_payment.getPaymentDetails())  # Display payment details

# Test case for Ghazlan Alketbi
ghazlan_payment = Payment(1002, 400.0, date(2025, 5, 10))
print("\nGhazlan Alketbi's Payment")
print(ghazlan_payment.processPayment())  # Processing the payment
print(ghazlan_payment.refundPayment())  # Refunding the payment
print(ghazlan_payment.getPaymentDetails())  # Display payment details
