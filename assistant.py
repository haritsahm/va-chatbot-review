import logging
from typing import Any

import streamlit as st
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.base import Chain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.memory.chat_memory import BaseChatMemory
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.vectorstores import DeepLake as DeepLakeVS
from langchain.vectorstores.base import VectorStoreRetriever

import deeplake
from prompt_templates import ASSISTANT_PROMPT_1


class AssistantBot:
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
        """Initialize Retriever from Deep Lake Vector Store.

        This method will load from a local dataset

        Parameters
        ----------
        dataset_path : str
            Path to deeplake vector store dataset.

        Raises
        ------
        RuntimeError
            If given path is not valid.
        RuntimeError
            If dataset is empty.
        """
        if not deeplake.exists(dataset_path):
            raise RuntimeError(f'Path to {dataset_path} is not valid')

        embeddings = OpenAIEmbeddings(model='text-embedding-ada-002')

        db = DeepLakeVS(dataset_path=dataset_path, embedding=embeddings, num_workers=4, read_only=True)

        if len(db.vectorstore) == 0:
            raise RuntimeError('Dataset is empty. Please generate a new vector dataset.')

        self._retriever = db.as_retriever()
        self._retriever.search_kwargs['distance_metric'] = 'cos'
        self._retriever.search_kwargs['fetch_k'] = 15
        self._retriever.search_kwargs['maximal_marginal_relevance'] = True
        self._retriever.search_kwargs['k'] = 15

    def update_retriever(self, dataset_path: str) -> bool:
        """Update the current vector store with a new vector store.

        NOTE: Experimental feature for offline loading of datasets.

        Parameters
        ----------
        dataset_path : str
            Path to deeplake vector store dataset.

        Returns
        -------
        bool
            If the process was successful.
        """
        try:
            self.initialize_retriever(dataset_path)
        except Exception as ex:
            logging.error(ex)
            return False
        return True

    def initialize_memory(self) -> None:
        """Initialize the memory buffer."""
        self._memory = ConversationBufferWindowMemory(
            memory_key='chat_history',
            k=5,
            input_key='question',
            output_key='answer',
            return_messages=True)

    def initialize_chain(self) -> bool:
        """Initialize LLM Chain.

        The system uses ConversationalRetrievalChain from Langchain.
        By default it uses the GPT-3.5 with 16k token size.

        Returns
        -------
        bool
            If the process was successful.

        Raises
        ------
        RuntimeError
            If the retriever or memory aren't valid.
        """
        if self._retriever is None or self._memory is None:
            raise RuntimeError("Retriever or memory aren't valid.")

        try:
            # create compressor for the retriever
            compressor = LLMChainExtractor.from_llm(OpenAI(model='gpt-3.5-turbo-instruct', temperature=0))
            compression_retriever = ContextualCompressionRetriever(
                base_compressor=compressor,
                base_retriever=self._retriever
            )

            self._chain = ConversationalRetrievalChain.from_llm(
                llm=ChatOpenAI(model='gpt-3.5-turbo-1106', temperature=0),
                chain_type='stuff',
                memory=self._memory,
                retriever=compression_retriever,
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
        """Process given input from user to chain."""
        return self._chain.run(*args, **kwds)


@st.cache_resource
def initialize_bot(dataset_path) -> AssistantBot:
    """Initialize bot and enable caching.

    NOTE: Need to use additional function because streamlit doesn't support caching class object.
    """
    return AssistantBot(dataset_path=dataset_path)
