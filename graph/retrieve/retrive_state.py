from pydantic import BaseModel, Field
from typing import Optional

class GraphState(BaseModel):
    """Extended state for the save graph workflow"""
    raw_text: str = Field(None, description="Raw text input")
    retrieve: Optional[bool] = Field(default=False, description="Retrieve from internal vector store or not")
    llm_result: Optional[str] = Field(
        None, description="Result from LLM or other processing nodes"
    )
    generation: Optional[str] = Field(
        None, description="generation from agentic rag"
    )