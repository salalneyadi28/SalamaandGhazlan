# GroupDiscount class to calculate group-based discounts

class GroupDiscount:
    def __init__(self, groupSize, discountPercentage):
        self.setGroupSize(groupSize)
        self.setDiscountPercentage(discountPercentage)

    # Setter for group size
    def setGroupSize(self, groupSize):
        self.__groupSize = groupSize

    # Getter for group size
    def getGroupSize(self):
        return self.__groupSize

    # Setter for discount percentage
    def setDiscountPercentage(self, discountPercentage):
        if 0 <= discountPercentage <= 100:
            self.__discountPercentage = discountPercentage
        else:
            raise ValueError("Discount percentage must be between 0 and 100")

    # Getter for discount percentage
    def getDiscountPercentage(self):
        return self.__discountPercentage

    # Method to calculate the discounted price for a given base price
    def calculateDiscount(self, basePrice):
        discount = basePrice * (self.getDiscountPercentage() / 100)
        return basePrice - discount

    # String representation of the discount
    def __str__(self):
        return f"Group size: {self.__groupSize}, Discount: {self.__discountPercentage}%"

# Test Code for GroupDiscount
if __name__ == "__main__":
    print("Test GroupDiscount Class\n")

    # Create a GroupDiscount object for Salama Alneyadi
    salama_discount = GroupDiscount(groupSize=5, discountPercentage=10.0)

    # Create a GroupDiscount object for Ghazlan Alketbi
    ghazlan_discount = GroupDiscount(groupSize=8, discountPercentage=15.0)

    # Base ticket price
    base_price = 100.0

    # Calculate discounted price for Salama
    salama_discounted_price = salama_discount.calculateDiscount(base_price)

    # Calculate discounted price for Ghazlan
    ghazlan_discounted_price = ghazlan_discount.calculateDiscount(base_price)

    # Output for Salama
    print("User: Salama Alneyadi")
    print("Group Size:", salama_discount.getGroupSize())
    print("Discount Percentage:", salama_discount.getDiscountPercentage(), "%")
    print("Original Price:", base_price, "AED")
    print("Discounted Price:", salama_discounted_price, "AED\n")

    # Output for Ghazlan
    print("User: Ghazlan Alketbi")
    print("Group Size:", ghazlan_discount.getGroupSize())
    print("Discount Percentage:", ghazlan_discount.getDiscountPercentage(), "%")
    print("Original Price:", base_price, "AED")
    print("Discounted Price:", ghazlan_discounted_price, "AED")
