import random

class Servicemenu:
    def __init__(self) -> None:
        self.menu = {
            1: {'food':'Pizza', 'price':3.50, 'quantity':20},
            2: {'food':'Burger', 'price':2.50, 'quantity':20},
            3: {'food':'Hotdog', 'price':2.20, 'quantity':20},
            4: {'food':'Fries', 'price':2.40, 'quantity':20},
            5: {'food':'Nuggets', 'price':4.00, 'quantity':20},
            6: {'food':'Cola', 'price':1.80, 'quantity':20},
            7: {'food':'Sprite', 'price':1.80, 'quantity':20}
        }

        self.selected_item = []
        self.total_price = 0

    def display_menu(self) -> None:
        print("-Menu-")
        for key, item in self.menu.items():
            availability = f"x{item['quantity']}" if item['quantity'] > 0 else '(The item is out of stock)'
            print(f"{key}) {item['food']} - ${item['price']:.2f} - {availability}")
        print('Press (0) to quit the menu')
        print('Press (S) to view the current ordered items')
        print('Press (C) to clear the current ordered items')
        print('Press (R) to random recommendation')
        print('Press (D) to proceed to checkout')
        print('Press (P) to open the dynamic menu')

    def increase_quantity(self, item_food, item_quantity) -> None:
        for item in self.menu.values():
            if item['food'] == item_food:
                item['quantity'] += item_quantity
                break

    def dynamic_menu(self) -> None:
        while True:
            print('Dynamic menu options:')
            print('Press (1) to add new item')
            print('Press (2) to update item')
            print('Press (3) to return to the main menu')
            choice = input('Choose an option: ')

            if choice == '1':
                self.add_new_item()
            elif choice == '2':
                self.update_quantity()
            elif choice == '3':
                confirmation = input('Press enter to return to the main menu')
                break
            else:
                print('Invalid input, you must enter number 1, 2 or 3 otherwise request will not completed')

    def add_new_item(self) -> None:
        food_name = input('Choose an item nickname: ')
        if food_name.strip() == '':
            print('Item nickname can not be empty, try again')
            return
        if food_name in [item for item in self.menu.values()]:
            print('The item nickname that you have entered is already exists in our menu system')
            return
        price = float(input('Please choose price for new item: '))
        quantity = int(input('Please choose quantity for new item: '))

        new_menu_number = max(self.menu.keys()) + 1
        new_item = {
            'food':food_name,
            'price':price,
            'quantity':quantity
        }
        self.menu[new_menu_number] = new_item
        print(f"You have added new item with name {food_name} in menu it raws in {new_menu_number}")

    def update_quantity(self) -> None:
        choice = int(input('Choose item number for update its quantity: '))
        if choice not in [item for item in self.menu.keys()]:
            print(f"Invalid input, please enter a valid item which exists in our menu system")
            return
        quantity = self.validate_ppsitive_integer('Choose the number to update quantity for selected item: ')
        selected_item = self.menu[choice]
        selected_item['quantity'] += quantity
        print(f"The quantity of an item {choice} updated to x({quantity})")

    def validate_ppsitive_integer(self, choice) -> int:
        while True:
            value = input(choice)
            if not value.replace('-', '').isdigit() or int(value) < -20 or int(value) > 20:
                print(f"The number that you selected does not correcspond at our criteriums so please choose an item between -20 and 20: ")
                return
            else:
                return int(value)
            
    def clearing_items(self) -> None:
        clear_request = input('Are you sure that you want to clear the current ordered items? (Yes(1))/(No(2))')
        if clear_request == '1':
            if len(self.selected_item) > 0:
                for item in self.selected_item:
                    self.increase_quantity(item['food'], item['quantity'])
                self.total_price = 0
                self.selected_item = []
                print('Current ordered items cleared!')
            else:
                print('To clear the current ordered items you must order at least one item')
        elif clear_request == '2':
            print('Clearing request cancelled!')
        else:
            print('To perform the request you must enter number 1 or 2 otherise request will not be able to performing')

    def food_order(self, choice) -> None:
        selected_item = self.menu[choice]
        if selected_item['quantity'] > 0:
            quantity = int(input(f"How many {selected_item['food']} you want to order: "))
            if quantity <= 0:
                print(f"Invalid input, please enter only valid numbers between 1 and 20 to execute the given request")
            elif quantity > 20:
                print('The number that you have is to much please enter between 1 and 20')
            else:
                selected_item['quantity'] -= quantity
                self.selected_item.append({'food':selected_item['food'], 'price':selected_item['price'], 'quantity':quantity})
                self.total_price += selected_item['price'] * quantity
                print(f"You have ordered x{quantity} {selected_item['food']} for each ${selected_item['price']:.2f}")
        else:
            print('The item is out of stock')

    def random_item(self) -> None:
        available_items = [item for item in self.menu.values() if item['quantity'] > 0]
        if available_items:
            random_item = random.choice(available_items)
            self.increase_quantity(random_item['food'], -1)
            self.selected_item.append({'food':random_item['food'], 'price':random_item['price'], 'quantity':1})
            self.total_price += random_item['price']
            print(f'We are recommending {random_item["food"]} for a ${random_item["price"]:.2f}')
        else:
            print('Sorry the item is out of stock')

    def view_items(self) -> None:
        if len(self.selected_item) > 0:
            item_count = {}
            for item in self.selected_item:
                item_food = item['food']
                item_count = item_count.get(item_food, 0) + item['quantity']
            for item, quantity in item_count.items():
                print(f"{item} - x{quantity}")
        else:
            print('To view the current ordered items you must order at least one item')

    def proceeding_to_checkout(self) -> bool:
        checkout_request = input("Are you sure that you want to proceeding to checkout? (Yes(1))/(No(2)): ")
        if checkout_request == '1':
            if len(self.selected_item) > 0:
                for item in self.selected_item:
                    food_name = item['food']
                    food_quantity = item['quantity']
                    print(f"{food_name} - x{food_quantity}")
                print(f"Your total payable is ${self.total_price:.2f}")
                print('Thank you for using our menu system, visit us later, goodbye :)')
                return True
            else:
                print('To proceed to checkout you must order at least one item')
                return False
        elif checkout_request == '2':
            print('Checkout request cancelled')
            return False
        else:
            print('Invalid input, you must enter number 1 or 2, please try again')
            return False

    def quit_menu(self) -> bool:
        exit_request = input('Are you sure that you want to exit the menu? (Yes(1))/(No(2)): ')
        if exit_request == '1':
            print('Menu cancelled!')
            return True
        elif exit_request == '2':
            print('Exit request cancelled!')
            return False
        else:
            print('Invalid input, you must enter number 1 or 2, please try again')
            return False
        
    def run(self) -> None:
        while True:
            self.display_menu()
            choice = input('Choose an option: ')
            if choice.isdigit():
                choice = int(choice)
                if choice == 0:
                    if self.quit_menu() == True:
                        break
                elif choice not in self.menu.keys():
                    print('The number that you have entered does not exists in our menu system')
                else:
                    self.food_order(choice)
            elif choice.lower() == 's':
                self.view_items()
            elif choice.lower() == 'r':
                self.random_item()
            elif choice.lower() == 'c':
                self.clearing_items()
            elif choice.lower() == 'd':
                self.dynamic_menu()
            elif choice.lower() == 'p':
                if self.proceeding_to_checkout() == True:
                    break
            elif choice.strip() == '':
                print('You have entered emptiness please enter the valid numbers or letters')
            else:
                print('Invalid input, please enter only valid numbers or letters ')    

if __name__ == '__main__':
    menuservice = Servicemenu()
    menuservice.run()        

