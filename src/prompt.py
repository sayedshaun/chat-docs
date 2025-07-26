# prompts.py
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from functools import lru_cache
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
)
from langchain.schema import SystemMessage, HumanMessage, AIMessage

def document_executor_prompt() -> PromptTemplate:
    template="""Answer the question based only on the following context:

    Context: 
    {context}
    ---------
    Question:
    {question}
    ---------

    If you don't find the answer in the context, say "I don't know"
    """
    return PromptTemplate(
        input_variables=["context", "question"],
        template=template
    )

@lru_cache(maxsize=1)
def general_prompt() -> ChatPromptTemplate:
    template = """Your are a helpful assistant that answers user's questions.
    You are designed to do conversion with users and provide accurate information.
    if user asks about any specific topic, you should provide detailed information from the context.
    otherwise, you should provide general information. If user ask any question that is not related to the context, you should say "I don't know"
    """

    system_message = SystemMessagePromptTemplate.from_template(template)    
    example_human = HumanMessagePromptTemplate.from_template("Hi, what can you do?")
    example_ai = AIMessagePromptTemplate.from_template("I can answer Gigatech HR questions!")
    human_message = HumanMessagePromptTemplate.from_template("{question}")

    prompt = ChatPromptTemplate.from_messages(
        messages=[
            system_message,
            example_human,
            example_ai,
            human_message,
        ]
    )
    return prompt


DOCUMENT_EXECUTOR_PROMPT = document_executor_prompt()
GENERAL_PROMPT = general_prompt