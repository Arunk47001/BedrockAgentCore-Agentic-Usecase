# importing the libraries
from abc import ABC


class VectorStoreEngineRepo(ABC):

    def create_index(self):
        raise NotImplementedError

    def add_document(self, documents:list):
        raise NotImplementedError

    def retrieval_document(self, query:str, top_k:int):
        raise NotImplementedError
