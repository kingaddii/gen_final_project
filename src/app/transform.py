from hashlib import sha256
import logging

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO) 


def hash(s: str) -> str:
        return str(int(sha256(s.encode('utf-8')).hexdigest(), 16))[:10]

#remove payment details from data
def remove_payment_details(data):
    for item in data:
        keys_to_remove = ['pay_method', 'card_no']
        for key in keys_to_remove:
            del item[key]

    return data 

#Extract payment details
def extract_payment_method(data):
    payments_data = []
    for item in data:
        order_id = hash(item['customer'])
        method = item['pay_method']

        payment_dict = {"id": order_id, "pay_method": method}
        payments_data.append(payment_dict)

    return payments_data    

#index the branches of the fast food outlet
def index_branches(data):
    branches = []
    for item in data:
        branch = item['location']
        branchhash = hash(branch)
        branch_dict = {"id": branchhash, "branch" : branch}

        branches.append(branch_dict)
        uniqueBranches = list({object['id']:object for object in branches}.values())


    return uniqueBranches    


#index the products
def index_products(data):
    products = []
    for item in data:
        product = item['products']    
        product = product.split(', ')
        products.append(product)

        flatproducts=[]
        for sublist in products:
            for element in sublist:
                flatproducts.append(element)

        uniqueProducts = set(flatproducts)
        uniqueProducts = list(uniqueProducts)   

        result = []
        for item in uniqueProducts:
            val = item.rsplit(" - ", 1)
            #print (val)
            productdict = {}
            productdict['id'] = hash(val[0])
            productdict['product'] = val[0]
            productdict['price'] = val[1]
            #print(productdict)
            result.append(productdict)
            
   
       
    return result

        

#create data for orders table
def separating_orders(data):
    cleaned_orders = []
    for item in data:
        order_id = hash(item['customer'])
        date_time = item['date']
        branch_id = hash(item['location'])
        total_price = item['total_cost']
        # LOGGER.info(item)
        method = item['pay_method']

        new_item = {"order_id" : order_id, "date_time": date_time, "branch_id": branch_id, "total_price": total_price, "method": method}

        cleaned_orders.append(new_item)

    return cleaned_orders    


def count_products_ordered(data):
    custinfo = []
    for item in data:
        
      
        order_id = hash(item['customer'])
        product = item['products']    
        products = product.split(', ')
    
     
        for p in products:
         
            val = p.rsplit(" - ", 1)

            product_id = hash(val[0])
            product_id = int(product_id)
            k = products.count(p)
            result = {'order_id':order_id, 'product_id':product_id, 'quantity': k}
    
            custinfo.append(result)


        unique_products_purchased=[]

        for i in custinfo:
            if i not in unique_products_purchased:
                unique_products_purchased.append(i) 
    
    return unique_products_purchased

