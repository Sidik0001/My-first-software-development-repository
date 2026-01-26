'''
Unit 4 Software Development

Inventory Management System
'''

products_details = {
                    'monitor':{'Quantity':25,'Price':270},
                    'keyboard':{'Quantity':40, 'Price':31},
                    'mouse':{'Quantity':40, 'Price':25},
                    'laptop':{'Quantity':42, 'Price':480}
                    }

print(f'Please see the product details below:\n\n{products_details}', sep='\n')

print(products_details['monitor'])

class Inventory:
    def __init__(self, name, quantity, price):
        self.name = name
        self.quantity = quantity
        self.price = price
    
    def update (self, detail, new_value):
        ''' This method updates inventories details such as quantity and price '''
        if detail == 'Quantity':
            self.quantity = new_value
        elif detail == 'Price':
            self.price = new_value
        print(f'\n{detail} has been updated to {new_value} for {self.name}\n')

hard_drive = Inventory('hard_drive', 15, 75)

print(f'\nHere are the inventory details of the hard drive (object) below:{hard_drive.__dict__}')

hard_drive.update('Quantity', 45)

print(hard_drive.__dict__, hard_drive.quantity)

hard_drive.update('Price', 89.67)


summary=hard_drive.__dict__

product_dict= {}

print('Inventory summary:\n')

for g,h in summary.items():
    product_dict.update({g.capitalize():h})
    if isinstance(h,str):
        product_dict[g.capitalize()]=h.capitalize()
print(product_dict)

with open('inventory.csv', 'w') as f:
    f.write('Inventory summary:\n\n')
    for key in product_dict.keys():
        f.write('{0},{1}\n'.format(key, product_dict[key]))

