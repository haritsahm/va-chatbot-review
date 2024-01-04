from langchain.prompts import PromptTemplate

assistant_template_1 = """
You're a helpful assistant, please answer the following question correctly \
using only the information from the provided context. Do not invent stuff \
and simply say that you don't know to the answer because it is irrelevant with the provided context below:

{context}

This was our previous chat history:
{chat_history}

Question: {question}

Answer:
"""

ASSISTANT_PROMPT_1 = PromptTemplate(
    input_variables=['context', 'question'],
    template=assistant_template_1,
)
