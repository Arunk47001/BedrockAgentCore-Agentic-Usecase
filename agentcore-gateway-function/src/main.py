# importing the libraries
from controller.etl import etl_method


def handler(event, context):
    return etl_method(event, context)