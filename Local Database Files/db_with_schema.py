def create_tables():
    sql = """  
    CREATE TABLE IF NOT EXISTS Products (
        Product_ID SMALLSERIAL PRIMARY KEY,
        Product_Name VARCHAR(255) NOT NULL,
        Price FLOAT(2) NOT NULL,
        UNIQUE (Product_Name)
    );
    CREATE TABLE IF NOT EXISTS Branches (
        Branch_ID SMALLSERIAL PRIMARY KEY,
        Branch VARCHAR(255) NOT NULL,
        UNIQUE (Branch)
    );
    CREATE TABLE IF NOT EXISTS Orders(
        Order_ID INT NOT NULL PRIMARY KEY,
        Date_Time timestamp NOT NULL,
        Branch_ID INT NOT NULL REFERENCES Branches (Branch_ID),
        Total_Price FLOAT(2) NOT NULL
    );
    CREATE TABLE IF NOT EXISTS Products_Ordered (
        Order_ID INT NOT NULL REFERENCES Orders (Order_ID),
        Product_ID INT NOT NULL REFERENCES Products (Product_ID),
        Quantity INT NOT NULL
    );
    """
    return sql


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
            run_db(sql)
    
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
            run_db(sql)
