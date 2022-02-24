import boto3
import os
import psycopg2
from psycopg2.extras import execute_batch

import logging


LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO) 



def get_ssm_parameters_under_path(path: str) -> dict:
    ssm_client = boto3.client("ssm", region_name="eu-west-1")
    response = ssm_client.get_parameters_by_path(
        Path=path,
        Recursive=True,
        WithDecryption=True
    )
    formatted_response = {os.path.basename(x["Name"]):x["Value"] for x in response["Parameters"]}
    return formatted_response


def run_db(sql, val, creds):
    try:
        connection = psycopg2.connect(
            host=creds["host"],
            user=creds["user"],
            password=creds["password"],
            database=creds["db"],
            port = creds["port"]
        )
        LOGGER.info("Established redshift connection")
        connection.autocommit=True
        cursor = connection.cursor()


        cursor.execute(sql, val)
        #connection.commit()
        cursor.close()
    
    except Exception:
        pass

    finally:
        connection.close()



def execute_multiple_db(statements: list[str], creds):
    try:
        connection = psycopg2.connect(
            host=creds["host"],
            user=creds["user"],
            password=creds["password"],
            database=creds["db"],
            port = creds["port"]
        )
        LOGGER.info("Established redshift connection")
        #connection.autocommit=True
        cursor = connection.cursor()

        for statement in statements:
            cursor.execute(statement)
        connection.commit()
        cursor.close()
    
    except Exception as ex:
        #database error
        
        LOGGER.error("Database error")
        LOGGER.error(ex)
        raise ex

    finally:
        connection.close()



# def test_sql(creds):
#     sql = "INSERT INTO branches(branch_id, branch) VALUES (123, 'Chelsea')"
#     run_db(sql, creds)




def loading_branches(data, creds):
    LOGGER.info(f"Saving {len(data)} branches")
    statements = ["CREATE TEMP TABLE branches_staging (LIKE branches);"]
    for item in data:
        branch_id = item['id']
        branch = item['branch']



        sql = f"INSERT INTO branches_staging (branch_id, branch) VALUES ({branch_id}, '{branch}')" 
        statements.append(sql)
        
    sql = """DELETE FROM branches_staging USING branches WHERE branches_staging.branch_id = branches.branch_id;
    INSERT INTO branches SELECT * FROM branches_staging"""
    statements.append(sql)
    
    execute_multiple_db(statements, creds)


def loading_products(data, creds):
    LOGGER.info(f"Saving {len(data)} products")
    statements = ["CREATE TEMP TABLE products_staging (LIKE products);"]
    for item in data:
        product_id = item['id']
        product = item['product']
        price = item['price']



        sql = f"INSERT INTO products_staging (product_id, product_name, price) VALUES ({product_id}, '{product}', {price})" 
        statements.append(sql)
        
    sql = """DELETE FROM products_staging USING products WHERE products_staging.product_id = products.product_id;
    INSERT INTO products SELECT * FROM products_staging"""
    statements.append(sql)
        
        #LOGGER.info(sql)
    
    execute_multiple_db(statements, creds)

def loading_orders(data, creds):
    LOGGER.info(f"Saving {len(data)} ")
    statements = ["CREATE TEMP TABLE orders_staging (LIKE orders);", "SET datestyle = dmy"]
    for item in data:
        #{'order_id': '1533161305', 'date_time': '25/08/2021 09:00', 'branch_id': '2895903154', 'total_price': '5.2'}
        order_id = item['order_id']
        date_time = item['date_time']
        branch_id = item['branch_id']
        price = item['total_price']
        payment_method = item['method']
        

        sql = f"INSERT INTO orders_staging (order_id, date_time, branch_id, total_price, payment_method) VALUES ({order_id}, '{date_time}', {branch_id} ,{price}, '{payment_method}')" 
        statements.append(sql)
        
    sql = """DELETE FROM orders_staging USING orders WHERE orders_staging.order_id = orders.order_id;
    INSERT INTO orders SELECT * FROM orders_staging"""
    statements.append(sql)
        
        #LOGGER.info(sql)
    
    execute_multiple_db(statements, creds)    

def loading_order_quantities(data, creds):
    LOGGER.info(f"Saving {len(data)} ")
    statements = ["CREATE TEMP TABLE products_ordered_staging (LIKE products_ordered);"]
    for item in data:
        
        order_id = item['order_id']
        product_id = item['product_id']
        quantity = item['quantity']

        

        sql = f"INSERT INTO products_ordered_staging (order_id, product_id, quantity) VALUES ({order_id}, {product_id}, {quantity})" 
        statements.append(sql)
        
    sql = """DELETE FROM products_ordered_staging USING products_ordered WHERE products_ordered_staging.order_id = products_ordered.order_id;
    INSERT INTO products_ordered SELECT * FROM products_ordered_staging"""
    statements.append(sql)
        
        #LOGGER.info(sql)
    
    execute_multiple_db(statements, creds)   