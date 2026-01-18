# importing the libraries
from usecase.vector_ingestion import ingestion


def vector_etl():
    try:
        ingestion()
    except Exception as e:
        print(f"An error occurred during the ETL process: {e}")
        raise ValueError("ETL process failed")