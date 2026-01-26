from pydantic import BaseModel, Field
from langsmith import Client
from pydantic import BaseModel, Field
from configuration import get_shared_llm
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnableSequence

client = Client()
prompt = client.pull_prompt(
    "pavan-n-patil/cortex-save-or-retreive",
)
llm = get_shared_llm()
class SaveRetrieveIntent(BaseModel):
    intent: str = Field(
        description="User intent: either 'save' or 'retrieve'. No other values allowed."
    )

structured_llm = get_shared_llm().with_structured_output(SaveRetrieveIntent)

intent_classifier: RunnableSequence = prompt | structured_llm