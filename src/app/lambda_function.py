import logging
import os
import csv
import app.extract as extract
import boto3
import json

from app.transform import index_branches, index_products, separating_orders, count_products_ordered


LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO) 


def lambda_handler(event, context):
    LOGGER.info(event)

    file_path = "/tmp/some_file.csv"

    s3_event = event["Records"][0]["s3"]
    bucket_name = s3_event["bucket"]["name"]
    object_name = s3_event["object"]["key"] 

    #LOGGER.info(f"Triggered by file {object_name} in bucket {bucket_name}")

    s3 = boto3.client("s3")
    s3.download_file(bucket_name, object_name, file_path)



    ## EXTRACT THE DATA

    data = extract.raw_data_extract(file_path)
    
   

    branchdata = index_branches(data)
    LOGGER.info(data[0])
    print(branchdata)


    productsdata = index_products(data)

    print(productsdata)
 
    separatedorders = separating_orders(data)

    print(separatedorders)

    orders_counted_products = count_products_ordered(data)

    print(orders_counted_products)


    base_filename = os.path.splitext(object_name)[0]

    sqs = boto3.client('sqs')

    send_file(s3, sqs, branchdata, "branches", base_filename + "_branches.csv")
    send_file(s3, sqs, productsdata, "products", base_filename + "_products.csv")
    send_file(s3, sqs, separatedorders, "orders", base_filename + "_orders.csv")
    send_file(s3, sqs, orders_counted_products, "products_ordered", base_filename + "_products_ordered.csv")

    
def send_file(s3, sqs, data_set, data_type: str, bucket_key: str):
    write_csv("/tmp/output.csv", data_set)
    LOGGER.info(f"Wrote local CSV for: {data_set}")

    bucket_name = "team5-transformed-cafe-data"
    s3.upload_file("/tmp/output.csv", bucket_name, bucket_key)
    LOGGER.info(f"Uploading to S3 into bucket {bucket_name} with key {bucket_key}")

    message = {
        "bucket_name" : bucket_name,
        "bucket_key" : bucket_key,
        "data_type" : data_type
    }
    
    sqs.send_message(
        QueueUrl='https://sqs.eu-west-1.amazonaws.com/123980920791/team5jack-load-queue',
        MessageBody=json.dumps(message)
    )



def write_csv(filename: str, data: list[dict[str, str]]):
    with open(filename, 'w') as csv_file:
        dict_writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(data)



