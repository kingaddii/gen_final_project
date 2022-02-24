import csv
from db1 import create_tables, insert_column_values_products, insert_column_values_branches
import os
import psycopg2
from dotenv import load_dotenv

order_id = 1

orders = []

unique_products = []
unique_branches = []

items = []
existing_branches = []

prices = []

quantities = []

load_dotenv()
host = os.environ.get("pg_host")
user = os.environ.get("pg_user")
password = os.environ.get("POSTGRES_PASSWORD")
database = os.environ.get("pg_db")

def run_db(sql):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=database,
        )
        connection.autocommit=True
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        if rows != None:
            return rows
        cursor.close()
    
    except Exception:
        pass

    finally:
        connection.close()


try:
    sql = "SELECT Branch FROM Branches"
    a = run_db(sql)
    for branch in a:
        if branch[0] not in unique_branches:
            unique_branches.append(branch[0])
            existing_branches.append(branch[0])

    sql = "SELECT Product_Name, Price FROM Products"
    b = run_db(sql)
    for item in b:
        if item[0] not in unique_products:
            unique_products.append(item[0])
            prices.append(item[1])
            items.append(item[0])

    sql = """SELECT Order_ID FROM Orders
                ORDER BY Order_ID DESC"""

    all_ids = run_db(sql)
    order_id = all_ids[0][0] + 1    

except Exception:
    pass

id = order_id

with open("chesterfield_25-08-2021_09-00-00.csv", "r") as csv_file:
    reader = csv.reader(csv_file)
    for line in reader:
        final_products = []
        test_for_products = []
        products = []
        test_for_products = line[3]

        if line[1] not in unique_branches:
            unique_branches.append(line[1])

        if ', ' in test_for_products:
            test_for_products = line[3].split(', ')

        x = 0
        for product in test_for_products:
            pricess = []
            if '- ' in product:
                x =+ 1
                products = product.rsplit(' - ', 1)
                pricess.append(product.split(' - ', -2))
                products.remove(products[-1])

                if products[0] not in unique_products:
                    unique_products.append(products[0])
                    prices.append(pricess[0][-1])

                final_products.append(products[0])
                            
        for i in final_products:
            orders.append({"id" : order_id, "Date_Time" : line[0], "Branch" : unique_branches.index(line[1])+1, "Product_Name" : unique_products.index(i)+1, "Quantity" : 0, "Total_Price" : line[4]})

            product = i
            counter = 0
            for i in final_products:
                if product == i:
                    counter += 1
            quantities.append(counter)

        if x == 0:
            if '- ' in test_for_products:
                products = test_for_products.rsplit(' - ', 1)
                pricess.append(products[1])
                products.remove(products[-1])
                if products[0] not in unique_products:
                    unique_products.append(products[0])
                    prices.append(pricess[0])

                final_products.append(products[0])
                orders.append({"id" : order_id, "Date_Time" : line[0], "Branch" : unique_branches.index(line[1])+1, "Product_Name" : unique_products.index(products[0])+1, "Quantity" : 1, "Total_Price" : line[4]})
                quantities.append(1)

        order_id += 1     

for y, z in enumerate(orders):
    count = quantities[y]
    z["Quantity"] = count

unique_orders = ([i for n, i in enumerate(orders) if i not in orders[n + 1:]])


def update_db(id):
    for i in unique_orders:
        counter = 0
        for i in unique_orders:
            if counter == 0 and i["id"] == id:
                counter += 1
        
                sql = f"""
                SET datestyle = dmy;
                INSERT INTO Orders (
                Order_ID, Date_Time, Branch_ID, Total_Price)
                VALUES ({i["id"]}, '{i['Date_Time']}',
                {i["Branch"]}, {i["Total_Price"]})"""
                run_db(sql)
        id += 1

    for i in unique_orders:
        sql = f"""
        INSERT INTO Products_Ordered (
        Order_ID, Product_ID, Quantity)
        VALUES ({i["id"]}, {i["Product_Name"]},
        {i["Quantity"]})"""
        run_db(sql)


sql = create_tables()
run_db(sql)

insert_column_values_products(unique_products, prices, items, run_db)
insert_column_values_branches(unique_branches, existing_branches, run_db)

update_db(id)
