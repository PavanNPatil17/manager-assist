from langsmith import Client
from langchain_core.output_parsers import StrOutputParser
from configuration import get_shared_llm
llm = get_shared_llm()
client = Client()
prompt = client.pull_prompt("rlm/rag-prompt")

generation_chain = prompt | llm | StrOutputParser()