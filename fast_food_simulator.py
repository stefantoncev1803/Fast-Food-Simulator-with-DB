import sqlite3

mydb = sqlite3.connect("fast_food_db.db")

mycursor = mydb.cursor()

try:
    mycursor.execute("CREATE TABLE products(id INTEGER PRIMARY KEY NOT NULL, name VARCHAR(255) NOT NULL, price FLOAT NOT NULL, quantity INTEGER NOT NULL)")
except:
    NameError()
    #print("Table with such name exists...")

def show_products():
    mycursor.execute("SELECT * FROM products")
    all_products = mycursor.fetchall()
    for item in all_products:
        print(f"{item[1]} , price: {item[2]}, available quantity: {item[3]}")

def check_product(product_name):
    mycursor.execute("SELECT rowid FROM products WHERE name = ?", (product_name,))
    data = mycursor.fetchone()
    if data is None:
        return False
    else:
        return True

def add_product():
    while True:
        input_yn = input("Do you want to add a product? - y or n ").lower()
        if input_yn == "n" or input_yn == "no":
            print("Adding of products finished...")
            print("Current product list: ")
            show_products()
            break
        elif input_yn == "y" or input_yn == "yes":
            product_name = input("Please enter product name: ")
            product_price = float(input("Please enter product price: "))
            product_quantity = int(input("Please enter product quantity: "))
            sql = "INSERT INTO products(name, price, quantity) VALUES (?, ?, ?)"
            val = (product_name, product_price, product_quantity)
            mycursor.execute(sql, val)
            mydb.commit()
            print(f"{product_quantity} of product {product_name} added in database...")
        else:
            continue

def add_quantity():
    while True:
        input_yn = input("Do you want to add quantity to a product? - y or n ").lower()
        if input_yn == "n" or input_yn == "no":
            print("Adding of products finished...")
            print("Current product list: ")
            show_products()
            break
        elif input_yn == "y" or input_yn == "yes":
            product_name = input("Please enter product name: ")
            if check_product(product_name):
                add_quantity = int(input("Please enter quantity to add: "))
                mycursor.execute("SELECT quantity FROM products WHERE name = ?", (product_name,))
                current_quantity = mycursor.fetchone()
                print(current_quantity)
                new_quantity = add_quantity + current_quantity[0]
                mycursor.execute("UPDATE products SET quantity = ? WHERE name = ?",  (new_quantity, product_name,))
                mydb.commit()
                print(f"{add_quantity} of product {product_name} added in database...")
            else:
                print("Product not found, please try again...")
                continue

        else:
            continue



def delete_product():
    temp_string = ""
    while True:
        input_yn = input("Do you want to delete a product? - y or n ").lower()
        if input_yn == "n" or input_yn == "no":
            print("Deleting of products finished...")
            print("Current product list: ")
            show_products()
            break
        elif input_yn == "y" or input_yn == "yes":
            product_name = input("Please enter product name to DELETE: ")
            if check_product(product_name):
                try:
                    mycursor.execute('DELETE FROM products WHERE name = ?', (product_name,))
                    mydb.commit()
                    print("Current product list: ")
                    show_products()
                except:
                    print("Error occurred...")
                    continue
            else:
                 print("Product not found, please try again...")
                 continue
        else:
            print("Invalid asnwer, please try again...")
            continue


def place_order():
    print("")
    print("Available products for the order are: ")
    show_products()
    list_order = {}
    order_price = 0
    while True:
        input_yn = input("Do you want to add a product to the order? - y or n ").lower()
        if input_yn == "n" or input_yn == "no":
            print(f"Your total order list is: {list_order} and total cost: {order_price} $ ")
            given_money = float(input("Money given: "))
            change = given_money - order_price
            print(f"Your change is: {change:.2f} $ ")
            print("Thank you and goodbye! ")
            break
        elif input_yn == "y" or input_yn == "yes":
            product_name = input("Please enter product name: ")
            if check_product(product_name):
                        quantity = input("Please enter quantity: ")
                        mycursor.execute("SELECT * FROM products WHERE name = ?", (product_name,))
                        ordered = mycursor.fetchone()
                        new_quantity = ordered[3] - 1 * int(quantity)
                        print(new_quantity)
                        mycursor.execute("UPDATE products SET quantity = ? WHERE name = ?",  (new_quantity, product_name,))
                        mydb.commit()
                        list_order.update({quantity + " x " + ordered[1]:ordered[2]})
                        order_price += ordered[2] * int(quantity)
                        print(f"Your order so far: {list_order} and total cost: {order_price} $ ")
            else:
                print("Product not matching, please try again...")
                continue
        else:
            print("Invalid asnwer, please try again...")
            continue

def finish_order():
    pass



while True:
    print('''             =========================
             Welcome to fast food Stefy
             ==========================
             Please choose an option:
             1. Show avaialble products
             2. Add product
             3. Add quantity
             4. Delete product
             5. Place order
             6. Exit

            ''')
    choose_option = input("Please choose option 1,2,3,4,5 or 6 : ")
    if choose_option == "6":
        print("Goodbye!")
        mydb.close()
        break
    elif choose_option == "1":
        print("Avaialble products: ")
        show_products()
    elif choose_option == "2":
        add_product()
    elif choose_option == "3":
        add_quantity()
    elif choose_option == "4":
        delete_product()
    elif choose_option == "5":
        place_order()
    else:
        print("Invalid option, please try again...")
        continue
