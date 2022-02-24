import logging
from app.load import get_ssm_parameters_under_path, loading_branches, loading_products, loading_orders, loading_order_quantities
import boto3
import csv
import json

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO) 

def load_handler(event, context):
    ## LOAD INTO AWS REDSHIFT

    creds = get_ssm_parameters_under_path("/team5/redshift")
    # LOGGER.info(creds)
    # LOGGER.info(event)
    file_path = "/tmp/some_file.csv"

    s3_event = event["Records"][0]["body"]

    # LOGGER.info(s3_event)
    s3_event = json.loads(s3_event)

    bucket_name = s3_event["bucket_name"]
    object_name = s3_event["bucket_key"]
    file_type = s3_event["data_type"]


    s3 = boto3.client("s3")
    s3.download_file(bucket_name, object_name, file_path)

    def load_csv_file(file_path):
        data = []
        with open(file_path) as csv_file:
            reader = csv.DictReader(csv_file)
            for line in reader:
                data.append(line)
        return data

    data = load_csv_file(file_path)


    if file_type == 'branches':
        LOGGER.info(data)
        loading_branches(data, creds)

    if file_type == 'products':
        LOGGER.info(data)
        loading_products(data, creds)

    if file_type == 'orders':
        LOGGER.info(data)
        loading_orders(data, creds)

    if file_type == 'products_ordered':
        LOGGER.info(data)
        loading_order_quantities(data, creds)
