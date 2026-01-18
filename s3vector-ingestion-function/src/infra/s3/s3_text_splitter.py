# importing the libraries
import os
import fitz
from langchain_text_splitters import TokenTextSplitter
from langchain.schema import Document

from domain.abstract.text_splitter_repo import TextSplitterEngineRepo
from infra.s3.s3 import S3Connect
from domain.vector_config import VectorConfig


class S3TextSplitterEngine(TextSplitterEngineRepo):
    def __init__(self):
        self.SRC_BUCKET = VectorConfig.src_bucket

    def _load_documents(self, doc: str):
        try:
            s3 = S3Connect(self.SRC_BUCKET)
            stream = s3.s3_get(doc)
            data = fitz.open(stream=stream, filetype='pdf')
            return "\n".join(page.get_text() for page in data)
        except Exception as err:
            print(err)
            raise ValueError("Error in Loading the Documents")

    def list_all_documents(self):
        try:
            s3 = S3Connect(self.SRC_BUCKET)
            docs = s3.s3_list_pdfs()
            return docs
        except Exception as err:
            print(err)
            raise ValueError("Error in list_all_documents")


    def chunking_data_split(self, doc: str):
        try:
            print("chunkingData_CharacterSplit Started:")
            docs = self._load_documents(doc)
            text_splitter = TokenTextSplitter(chunk_size=512, chunk_overlap=int(512 * 0.2))
            chunks = text_splitter.split_text(docs)
            return [Document(page_content=chunk) for chunk in chunks]
        except Exception as err:
            print(err)
            raise ValueError("Error in chunkingData_Character")
