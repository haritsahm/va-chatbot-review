from typing import Any

import deeplake
import streamlit as st

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import DeepLake as DeepLakeVS
from langchain.vectorstores.base import VectorStoreRetriever
from langchain.chains.base import Chain
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.memory.chat_memory import BaseChatMemory
from langchain.chat_models import ChatOpenAI

import logging

from prompt_templates import ASSISTANT_PROMPT_1


class AssistantBot(object):
    def __init__(self, dataset_path: str) -> None:
        pass

        self._retriever: VectorStoreRetriever = None
        self._chain: Chain = None
        self._memory: BaseChatMemory = None

        self._dataset_path = dataset_path
        self.initialize_retriever(dataset_path=self._dataset_path)
        self.initialize_memory()
        self.initialize_chain()

    def initialize_retriever(self, dataset_path: str) -> None:
        if not deeplake.exists(dataset_path):
            raise RuntimeError(f"Path to {dataset_path} is not valid")

        embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

        db = DeepLakeVS(dataset_path=dataset_path, embedding=embeddings, num_workers=4, read_only=True)
        self._retriever = db.as_retriever()
        self._retriever.search_kwargs['distance_metric'] = 'cos'
        self._retriever.search_kwargs['fetch_k'] = 10
        self._retriever.search_kwargs['maximal_marginal_relevance'] = True
        self._retriever.search_kwargs['k'] = 5

    def update_retriever(self, dataset_path: str) -> bool:
        try:
            self.initialize_retriever(dataset_path)
        except Exception as ex:
            logging.error(ex)
            return False
        return True

    def initialize_memory(self) -> None:
        self._memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            k=5,
            output_key='answer',
            return_messages=True)

    def initialize_chain(self) -> bool:
        if self._retriever is None or self._memory is None:
            raise RuntimeError("Retriever or memory aren't valid.")

        try:
            self._chain = ConversationalRetrievalChain.from_llm(
                llm=ChatOpenAI(model='gpt-3.5-turbo-1106', temperature=0),
                chain_type="stuff",
                memory=self._memory,
                retriever=self._retriever,
                combine_docs_chain_kwargs={
                    'prompt': ASSISTANT_PROMPT_1,
                },
                verbose=False
            )
        except Exception as ex:
            logging.error(ex)
            return False

        return True

    def process(self, *args: Any, **kwds: Any) -> Any:
        return self._chain.run(*args, **kwds)

@st.cache_resource
def initialize_bot(dataset_path):
    return AssistantBot(dataset_path=dataset_path)