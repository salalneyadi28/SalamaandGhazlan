from datetime import date  # Import date class to handle payment dates
import pickle  # Import pickle for saving and loading objects

# Define the base class Payment
class Payment:
    def __init__(self, paymentID, amount, paymentDate, paymentStatus="Processed"):
        self.setPaymentID(paymentID)  # Set payment ID
        self.setAmount(amount)  # Set payment amount
        self.setPaymentDate(paymentDate)  # Set payment date
        self.setPaymentStatus(paymentStatus)  # Set payment status

    # Setter for paymentID
    def setPaymentID(self, paymentID):
        self.__paymentID = paymentID  # Store as private attribute

    # Getter for paymentID
    def getPaymentID(self):
        return self.__paymentID

    # Setter for amount
    def setAmount(self, amount):
        self.__amount = amount  # Store as private attribute

    # Getter for amount
    def getAmount(self):
        return self.__amount

    # Setter for paymentDate
    def setPaymentDate(self, paymentDate):
        self.__paymentDate = paymentDate  # Store as private attribute

    # Getter for paymentDate
    def getPaymentDate(self):
        return self.__paymentDate

    # Setter for paymentStatus
    def setPaymentStatus(self, status):
        self.__paymentStatus = status  # Store as private attribute

    # Getter for paymentStatus
    def getPaymentStatus(self):
        return self.__paymentStatus

    # Method to process the payment and update the status
    def processPayment(self):
        self.setPaymentStatus("Processed")  # Mark payment as processed
        return f"Payment of {self.getAmount()} processed successfully."  # Return confirmation message

    # Method to return payment details as a dictionary
    def getPaymentDetails(self):
        return {
            "Payment ID": self.getPaymentID(),  # Include payment ID
            "Amount": self.getAmount(),  # Include amount
            "Payment Date": self.getPaymentDate().isoformat(),  # Convert date to string
            "Payment Status": self.getPaymentStatus()  # Include status
        }

# Define the DigitalWalletPayment class, which inherits from Payment
class DigitalWalletPayment(Payment):
    def __init__(self, paymentID, amount, paymentDate, walletID, provider, paymentStatus="Processed"):
        super().__init__(paymentID, amount, paymentDate, paymentStatus)  # Initialize base class attributes
        self.setWalletID(walletID)  # Set wallet ID
        self.setProvider(provider)  # Set provider name

    # Setter for walletID
    def setWalletID(self, walletID):
        self.__walletID = walletID  # Store as private attribute

    # Getter for walletID
    def getWalletID(self):
        return self.__walletID

    # Setter for provider
    def setProvider(self, provider):
        self.__provider = provider  # Store as private attribute

    # Getter for provider
    def getProvider(self):
        return self.__provider

    # Override method to process digital wallet payment
    def processPayment(self):
        self.setPaymentStatus("Processed")  # Update status to processed
        return f"Digital wallet payment of {self.getAmount()} processed successfully via {self.getProvider()}."  # Message

    # Extend the payment details with wallet information
    def getPaymentDetails(self):
        details = super().getPaymentDetails()  # Get base payment details
        details.update({
            "Wallet ID": self.getWalletID(),  # Add wallet ID
            "Provider": self.getProvider()  # Add wallet provider
        })
        return details

# Create a DigitalWalletPayment object for Salama Alneyadi
salama_wallet_payment = DigitalWalletPayment(
    paymentID=2001,  # Payment ID
    amount=150.0,  # Payment amount
    paymentDate=date(2025, 5, 10),  # Payment date
    walletID="wallet123456",  # Wallet ID
    provider="PayPal"  # Provider name
)

# Create a DigitalWalletPayment object for Ghazlan Alketbi
ghazlan_wallet_payment = DigitalWalletPayment(
    paymentID=2002,  # Payment ID
    amount=200.0,  # Payment amount
    paymentDate=date(2025, 5, 10),  # Payment date
    walletID="wallet654321",  # Wallet ID
    provider="Apple Pay"  # Provider name
)

# Print Salama's payment result
print(f"Salama Alneyadi's Digital Wallet Payment:")  # Header
print(salama_wallet_payment.processPayment())  # Print processing message
print(salama_wallet_payment.getPaymentDetails())  # Print payment details

# Print Ghazlan's payment result
print(f"\nGhazlan Alketbi's Digital Wallet Payment:")  # Header
print(ghazlan_wallet_payment.processPayment())  # Print processing message
print(ghazlan_wallet_payment.getPaymentDetails())  # Print payment details

# Save the payment objects to a pickle file
with open("wallet_payments.pkl", "wb") as file:
    pickle.dump([salama_wallet_payment, ghazlan_wallet_payment], file)

# Load the payment objects back from the pickle file
with open("wallet_payments.pkl", "rb") as file:
    loaded_payments = pickle.load(file)

# Print loaded payment details to verify
print("\nLoaded Payment Details from Pickle File:")
for payment in loaded_payments:
    print(payment.getPaymentDetails())
