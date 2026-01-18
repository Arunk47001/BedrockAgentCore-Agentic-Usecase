# importing the libraries
from abc import ABC


class VectorStoreEngineRepo(ABC):

    def retrieval_document(self, query:str, top_k:int):
        raise NotImplementedError
