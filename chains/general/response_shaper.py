from pydantic import BaseModel, Field
from langsmith import Client
from pydantic import BaseModel, Field
from configuration import get_shared_llm
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnableSequence
# intent: str
#     save_retrieve_response: st
client = Client()
prompt = client.pull_prompt(
    "pavan-n-patil/response-shaper",
)
llm = get_shared_llm()
class ResponseShaper(BaseModel):
    final_ai_message: str = Field(
        description="The final response message from the AI to be sent to the user."
    )

structured_llm = get_shared_llm().with_structured_output(ResponseShaper)

response_shaper: RunnableSequence = prompt | structured_llm