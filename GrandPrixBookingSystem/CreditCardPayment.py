from datetime import date  # Importing date class from datetime module to work with dates

# Define the base Payment class
class Payment:
    def __init__(self, paymentID, amount, paymentDate, paymentStatus="Pending"):
        # Initialize attributes using setter methods for encapsulation
        self.setPaymentID(paymentID)
        self.setAmount(amount)
        self.setPaymentDate(paymentDate)
        self.setPaymentStatus(paymentStatus)

    # Setter for paymentID
    def setPaymentID(self, paymentID):
        self.__paymentID = paymentID  # Private attribute

    # Getter for paymentID
    def getPaymentID(self):
        return self.__paymentID

    # Setter for amount
    def setAmount(self, amount):
        self.__amount = amount

    # Getter for amount
    def getAmount(self):
        return self.__amount

    # Setter for paymentDate
    def setPaymentDate(self, paymentDate):
        self.__paymentDate = paymentDate

    # Getter for paymentDate
    def getPaymentDate(self):
        return self.__paymentDate

    # Setter for paymentStatus
    def setPaymentStatus(self, status):
        self.__paymentStatus = status

    # Getter for paymentStatus
    def getPaymentStatus(self):
        return self.__paymentStatus

    # Process the payment and update the status to "Processed"
    def processPayment(self):
        self.setPaymentStatus("Processed")
        return f"Payment of {self.getAmount()} processed successfully."

    # Return payment details as a dictionary
    def getPaymentDetails(self):
        return {
            "Payment ID": self.getPaymentID(),
            "Amount": self.getAmount(),
            "Payment Date": self.getPaymentDate().isoformat(),
            "Payment Status": self.getPaymentStatus()
        }

# Define the CreditCardPayment class, inheriting from Payment
class CreditCardPayment(Payment):
    def __init__(self, paymentID, amount, paymentDate, cardNumber, cardholderName, expiryDate, cvv):
        # Call constructor of the base class
        super().__init__(paymentID, amount, paymentDate)
        # Initialize credit card-specific attributes
        self.setCardNumber(cardNumber)
        self.setCardholderName(cardholderName)
        self.setExpiryDate(expiryDate)
        self.setCVV(cvv)

    # Setter for card number
    def setCardNumber(self, cardNumber):
        self.__cardNumber = cardNumber

    # Getter for card number
    def getCardNumber(self):
        return self.__cardNumber

    # Setter for cardholder name
    def setCardholderName(self, name):
        self.__cardholderName = name

    # Getter for cardholder name
    def getCardholderName(self):
        return self.__cardholderName

    # Setter for expiry date
    def setExpiryDate(self, expiryDate):
        self.__expiryDate = expiryDate

    # Getter for expiry date
    def getExpiryDate(self):
        return self.__expiryDate

    # Setter for CVV
    def setCVV(self, cvv):
        self.__cvv = cvv

    # Getter for CVV
    def getCVV(self):
        return self.__cvv

    # Validate credit card details (length, digit check, expiry)
    def validateCard(self):
        return (
            len(self.getCardNumber()) == 16 and self.getCardNumber().isdigit() and
            len(self.getCVV()) == 3 and self.getCVV().isdigit() and
            self.getExpiryDate() > date.today()
        )

    # Override processPayment to include validation
    def processPayment(self):
        if self.validateCard():
            self.setPaymentStatus("Processed")
            return f"Payment of {self.getAmount()} processed successfully for {self.getCardholderName()}."
        else:
            self.setPaymentStatus("Failed")
            return f"Payment failed: Invalid card details for {self.getCardholderName()}."

    # Extend base getPaymentDetails with card info
    def getPaymentDetails(self):
        details = super().getPaymentDetails()
        details.update({
            "Card Number": self.getCardNumber(),
            "Cardholder Name": self.getCardholderName(),
            "Expiry Date": self.getExpiryDate().isoformat(),
            "CVV": self.getCVV()
        })
        return details

# Test Case: Salama Alneyadi's Payment
salama_payment = CreditCardPayment(
    paymentID=1001,
    amount=150.0,
    paymentDate=date(2025, 5, 10),
    cardNumber="1234567812345678",
    cardholderName="Salama Alneyadi",
    expiryDate=date(2026, 6, 1),
    cvv="123"
)

print("Salama Alneyadi's Payment")
print(salama_payment.processPayment())
print(salama_payment.getPaymentDetails())

# Test Case: Ghazlan Alketbi's Payment
ghazlan_payment = CreditCardPayment(
    paymentID=1002,
    amount=200.0,
    paymentDate=date(2025, 5, 10),
    cardNumber="8765432187654321",
    cardholderName="Ghazlan Alketbi",
    expiryDate=date(2025, 12, 31),
    cvv="456"
)

print("\nGhazlan Alketbi's Payment")
print(ghazlan_payment.processPayment())
print(ghazlan_payment.getPaymentDetails())
