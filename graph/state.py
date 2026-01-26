from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage
from typing import Optional, TypedDict, Annotated, Sequence

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    intent: Optional[str]
    save_retrieve_response: Optional[str]
    final_response: Optional[str]