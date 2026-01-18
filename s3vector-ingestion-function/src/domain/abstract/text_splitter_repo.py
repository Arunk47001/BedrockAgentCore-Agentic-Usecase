# importing the libraries
import abc


class TextSplitterEngineRepo(abc.ABC):

    def list_all_documents(self):
        raise  NotImplementedError

    def chunking_data_split(self, doc: str ):
        raise NotImplementedError