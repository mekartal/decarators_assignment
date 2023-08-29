from ast import literal_eval


class Manager:
    def __init__(self):
        self.account_balance = 0
        self.inventory = {}
        self.actions = {}


    def assign(self, task_name):
        def decorator(func):
            self.actions[task_name] = func
            return func
        return decorator
    
    def execute(self,name,*args,**kwargs):
        if name not in self.actions:
            print("Not in storage")
            return
        else:
            return self.actions[name](self,*args,**kwargs)
        
    def save_file(self):
        
        data = {
        'inventory': self.inventory,
        'account': self.balance
        }
        
        with open(file_name, 'w') as file:
            file.write(str(data))

        
    def load_file (self , file_name):
        try:
            with open(file_name, 'r') as file:
                try:
                    data=literal_eval(file.read())
                except SyntaxError:
                    print("invalid file content")
                    exit()
                self.inventory = data.get("inventory",{})
                self.balance = data.get("account",0)
        except FileNotFoundError:
            print("File does not exist! Creating a new file.")
            self.inventory={}


manager = Manager()
file_name = input("Please provide a name of a file (including extension, e.g., txt): ")
manager.load_file(file_name)
review = []

@manager.assign("sale")
def sale(manager):
    product_name = input ("Product name :")
    product_quantity = int(input ( "Product quantity :"))
    product_price= int(input("product price : "))


    if product_name in manager.inventory and manager.inventory[product_name] >= product_quantity:
        revenue = product_price * product_quantity
        manager.account_balance += revenue
        manager.inventory[product_name] -= product_quantity
        print(f"Sold {product_quantity} {product_name}(s) for {revenue}")
        review.append(f"{product_name} {product_quantity}(s) sold")
        save_inventory(file_name, manager.inventory,manager.account_balance)  
    else:
        print(f"Insufficient inventory for {product_name}")

@manager.assign("purchase")
def purchase(manager):
    product_name_purchase = input("What is the product?: ")
    product_price_purchase = float(input("How much does the product cost?: "))
    product_quantity_purchase = int(input("How many products do you want to purchase?: "))
    total_cost = product_price_purchase * product_quantity_purchase

    if manager.account_balance >= total_cost:
        manager.account_balance -= total_cost
        if product_name_purchase in manager.inventory:
            manager.inventory[product_name_purchase] += product_quantity_purchase
        else:
            manager.inventory[product_name_purchase] = product_quantity_purchase
        print("Account balance and inventory have been updated")
        review.append(f"{product_quantity_purchase} {product_name_purchase}(s) purchased")
        save_inventory(file_name, manager.inventory,manager.account_balance)  
    else:
        print("Account balance is not enough for this purchase")

@manager.assign("account_balance")
def account_balance_func(manager):
    print("Your balance is:", manager.account_balance)


@manager.assign("balance")
def balance_func(manager):
        command_for_balance = input("Add money or subtract money from the account: ")

        if command_for_balance == "add":
            balance_add = float(input("How much money do you want to add to your account?: "))
            manager.account_balance += balance_add
            print("Money is added")
            review.append(f"{balance_add} is added to the account")

        elif command_for_balance == "subtract":
            balance_subtract = float(input("How much money do you want to subtract from your account?: "))
            manager.account_balance -= balance_subtract
            print("Money is subtracted")
            review.append(f"{balance_subtract} is subtracted from the account")

@manager.assign("warehouse")
def warehouse_func(manager):
        warehouse_product_detail = input("Enter the name of the product for details: ")
        if warehouse_product_detail in manager.inventory:
            print("Product:", warehouse_product_detail)
            print("Quantity:", manager.inventory[warehouse_product_detail])
        else:
            print("Product not found in the warehouse.")

@manager.assign("inventory")
def inventory_func(manager):
        print("Total inventory in the warehouse:")
        for product, quantity in manager.inventory.items():
            print("Product:", product)
            print("Quantity:", quantity)
            print("--------")

@manager.assign("review")
def review_func(manager):
        print("History of operations:")

        for operation in review:
            print(operation)
            print("--------")


def load_inventory(file_name):
    try:
        with open(file_name, 'r') as file:
            return literal_eval(file.read())
    except FileNotFoundError:
        print("File does not exist! Creating a new file.")
        return {}

def save_inventory(file_name, inventory, account):
    data = {
        'inventory': inventory,
        'account': account
    }
    with open(file_name, 'w') as file:
        file.write(str(data))

# file_name = input("Please provide a name of a file (including extension, e.g., txt): ")
# inventory_data = load_inventory(file_name)

# inventory = inventory_data.get('inventory', {})
# account_balance = inventory_data.get('account', 0)
# review = []

print("Available commands: balance - add or subtract, purchase, sale, inventory, warehouse, review, account_balance, quit")

while True:
    command = input("Please enter a command: ")

    if command == "quit":
        print("Quitting program")
        save_inventory(file_name,manager.inventory , manager.account_balance)
        break
    
    elif command == "balance":
        manager.execute("balance")
     
    elif command == "purchase":
        manager.execute("purchase")

    elif command == "sale":
        manager.execute("sale")

    elif command == "warehouse":
        manager.execute("warehouse")


    elif command == "inventory":
        manager.execute("inventory")


    elif command == "account_balance":
        manager.execute("account_balance")

        
    elif command == "review":
        manager.execute("review")

