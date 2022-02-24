import boto3
import os
import psycopg2
#from app.transform import load_from_db, transform_data, quantities_added
# import app.transform


def get_ssm_parameters_under_path(path: str) -> dict:
    ssm_client = boto3.client("ssm", region_name="eu-west-1")
    response = ssm_client.get_parameters_by_path(
        Path=path,
        Recursive=True,
        WithDecryption=True
    )
    formatted_response = {os.path.basename(x["Name"]):x["Value"] for x in response["Parameters"]}
    return formatted_response

# def connect_to_redshift():  
#     creds = get_ssm_parameters_under_path("/team5/redshift")


def run_db(sql, creds):
    try:
        connection = psycopg2.connect(
            host=creds["host"],
            user=creds["user"],
            password=creds["password"],
            database=creds["db"],
            port = creds["port"]
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

def insert_column_values_products(products123, price_for_product, items, run_db):    
    
    for prices, item in enumerate(products123):
        price = price_for_product[prices]
        price = float(price)
        
        if item not in items:    
            sql = f"""
            INSERT INTO Products
            VALUES (
            DEFAULT, '{item}', {price}
            )
            ON CONFLICT DO NOTHING
            """
            items.append(item)
            run_db(sql, creds)
    
def insert_column_values_branches(Branchess, current_branches, run_db):
    for Branch in Branchess:
        if Branch not in current_branches:    
            sql = f"""
            INSERT INTO Branches(
            Branch_ID, Branch)
            VALUES
            (DEFAULT, '{Branch}')
            ON CONFLICT DO NOTHING
            """
            current_branches.append(Branch)
            run_db(sql, creds)  

            
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
                run_db(sql, creds)
        id += 1

    for i in unique_orders:
        sql = f"""
        INSERT INTO Products_Ordered (
        Order_ID, Product_ID, Quantity)
        VALUES ({i["id"]}, {i["Product_Name"]},
        {i["Quantity"]})"""
        run_db(sql, creds)