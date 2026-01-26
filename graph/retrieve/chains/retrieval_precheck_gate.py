from pydantic import BaseModel, Field
from langsmith import Client
from pydantic import BaseModel, Field
from configuration import get_shared_llm
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnableSequence

client = Client()
prompt = client.pull_prompt(
    "pavan-n-patil/retrieval_precheck_gate",
)
llm = get_shared_llm()

class RetrievalPrecheckResult(BaseModel):
    retrieve: bool = Field(..., description="Whether to retrieve or not")
    confidence: float = Field(..., ge=0, le=1, description="Confidence between 0 and 1")
    short_reason: str = Field(..., description="Brief explanation")

structured_llm = get_shared_llm().with_structured_output(RetrievalPrecheckResult)

retrieval_precheck_gate: RunnableSequence = prompt | structured_llm

