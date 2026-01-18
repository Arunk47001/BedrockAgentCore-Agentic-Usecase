# importing the libraries
from controller.etl import vector_etl


def handler(event, context):
    if "TYPE" in event:
        if event['TYPE'] == 'VECTOR_ETL':
            vector_etl()
