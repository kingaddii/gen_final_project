import csv
from msilib.schema import Class
from hashlib import sha256
from src.app.extract import raw_data_extract
from src.app.transform import remove_payment_details, extract_payment_method, index_branches, hash
from src.app.transform import separating_orders, count_products_ordered, index_products

#EXTRACT UNIT TEST
# extract data
def test_raw_data_extract():
#ARRANGE
    expected = [{'date': '25/09/2021 10:00', 'location': 'Brighton', 'customer': 'John Smith', 'products': 'Hamburger - 2.75, Large Fries - 2.30', 'total_cost': '5.05', 'pay_method': 'CARD', 'card_no': '5494177586996740'}]
#ACTUAL
    try:
        result = raw_data_extract("extra_data.csv")
# ASSERT
        assert expected == result
    except FileNotFoundError as fnfd:
        print("File not found" + str(fnfd))
    except Exception as e:
        print("Something went wrong" + str(e))
    return result

# TRANSFORM UNIT TEST
# remove payment details from data
def test_remove_payment_details():
#ARRANGE
    expected = [{'date': '25/09/2021 10:00', 'location': 'Brighton', 'customer': 'John Smith', 'products': 'Hamburger - 2.75, Large Fries - 2.30', 'total_cost': '5.05'}]
    new_data =  []
#ACTUAL
    try:
        result = raw_data_extract("extra_data.csv")
        result = remove_payment_details(result)
        new_data.append(result)
# ASSERT
        assert expected == result
    except FileNotFoundError as fnfd:
        print("File not found" + str(fnfd))
    except Exception as e:
        print("Something went wrong" + str(e))
    return result
test_remove_payment_details()

# hash order ids and extract payment method
def test_extract_payment_method():
#ARRANGE
    expected = [{"id": '5631983019', "pay_method": 'CASH'}]
#ACTUAL
    raw_data = [{'date': '25/09/2021 09:20', 'location': 'Cornwall', 'customer': 'Lewis Hamilton', 'products': 'Chapatti - 5.75, Mash Potato - 2.30', 'total_cost': '8.05', 'pay_method': 'CASH'}]
    result = extract_payment_method(raw_data)
#ASSERT
    assert expected == result
    return
test_extract_payment_method()

# hash branch ids
def test_index_branches():
#ARRANGE
    expected = [{"id": '3080742112', "branch": 'Cornwall'}]
#ACTUAL
    raw_data = [{'date': '25/09/2021 09:20', 'location': 'Cornwall', 'customer': 'Lewis Hamilton', 'products': 'Chapatti - 5.75, Mash Potato - 2.30', 'total_cost': '8.05', 'pay_method': 'CASH'}]
    result = index_branches(raw_data)
#ASSERT
    assert expected == result
    return
test_index_branches()

# index for products
def test_index_products():
#ARRANGE
    expected = [{'id': '1784391626', 'product': 'Chapatti', 'price': '5.75'}, {'id': '7192174250', 'product': 'Mash Potato', 'price': '2.30'}]
#ACTUAL
    raw_data = [{'date': '25/09/2021 09:20', 'location': 'Cornwall', 'customer': 'Lewis Hamilton', 'products': 'Chapatti - 5.75, Mash Potato - 2.30', 'total_cost': '8.05', 'pay_method': 'CASH'}]
    result = index_products(raw_data)
# ASSERT
    assert expected == result
test_index_products()


# create data for orders table
def test_separating_orders():
    # ARRANGE
    expected = [{'order_id': '5631983019', 'date_time': '25/09/2021 09:20', 'branch_id': '3080742112', 'total_price': '8.05', 'method': 'CASH'}]
# ACTUAL
    raw_data = [{'date': '25/09/2021 09:20', 'location': 'Cornwall', 'customer': 'Lewis Hamilton', 'products': 'Chapatti - 5.75, Mash Potato - 2.30', 'total_cost': '8.05', 'pay_method': 'CASH'}]
    result = separating_orders(raw_data)
# ASSERT
    assert result == expected
test_separating_orders()  

# counting products ordered
def test_count_products_ordered():
# ARRANGE
    expected = [{'order_id': '5631983019', 'product_id': 1784391626, 'quantity': 1}, {'order_id': '5631983019', 'product_id': 7192174250, 'quantity': 1}] 
# ACTUAL
    raw_data = [{'date': '25/09/2021 09:20', 'location': 'Cornwall', 'customer': 'Lewis Hamilton', 'products': 'Chapatti - 5.75, Mash Potato - 2.30', 'total_cost': '8.05', 'pay_method': 'CASH'}]
    result = count_products_ordered(raw_data)
# ASSERT
    assert expected == result
test_count_products_ordered()