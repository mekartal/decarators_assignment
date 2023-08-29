from ast import literal_eval

def load_inventory(file_name):
    try:
        with open(file_name,'r') as file:
            return literal_eval(file.read())
    except FileNotFoundError:
        print("File does not exist! creating a new file")
        return {}
    
def save_inventory(file_name,inventory):
    with open(file_name,'w') as file:
        file.write(str(inventory))