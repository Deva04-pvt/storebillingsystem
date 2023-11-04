# Sample data: Each sub-array contains [item code, item name, rate, quantity, total amount]
items = [
    ["001", "Apples", 1.99, 2, 3.98],
    ["002", "Bananas", 0.99, 3, 2.97],
    ["003", "Milk", 2.49, 1, 2.49],
    ["004", "Bread", 2.99, 2, 5.98],
]

# Customer ID
customer_id = "12345"


# Function to format and return the bill as a single string
def generate_grocery_bill_string(customer_id, items):
    bill_string = "===========================================\n"
    bill_string += f"       GROCERY STORE BILL\n"
    bill_string += f"Customer ID: {customer_id}\n"
    bill_string += "===========================================\n"
    bill_string += "{:<10} {:<20} {:<10} {:<10} {:<10}\n".format("Item Code", "Item Name", "Rate", "Quantity", "Total")
    bill_string += "-------------------------------------------\n"

    for item in items:
        item_code, item_name, rate, quantity, total = item
        bill_string += "{:<10} {:<20} ${:<9.2f} {:<10} ${:<9.2f}\n".format(item_code, item_name, rate, quantity, total)

    bill_string += "===========================================\n"

    return bill_string


# Call the function to generate the bill as a string
bill = generate_grocery_bill_string(customer_id, items)

# You can print the bill if needed
print(bill)
