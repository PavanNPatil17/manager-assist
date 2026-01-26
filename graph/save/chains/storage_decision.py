
import sys
from pathlib import Path

# Add project root to path simply to run directly the file
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from pydantic import BaseModel, Field
from typing import Literal
from graph.save.save_graph_state import NormalizedMemory
from graph.save.constants import ALLOWED_CATEGORIES, ALLOWED_SUBCATEGORIES
from configuration import get_shared_llm
from langchain_core.runnables import RunnableSequence
import os 
from datetime import datetime
from dotenv import load_dotenv
from chains.general.url_detector import url_detector
from graph.save.chains.normalize import normalize_chain
from langsmith import Client
load_dotenv()

# Define the storage decision model
class StorageDecision(BaseModel):
    storage_intent: Literal["STRUCTURED_AND_VECTOR", "VECTOR_ONLY"] = Field(
        description="Storage intent classification. STRUCTURED_AND_VECTOR: structured facts/decisions/tasks. VECTOR_ONLY: vague/ideational content."
    )
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence score between 0.0 and 1.0 for the classification decision"
    )

client = Client()
prompt = client.pull_prompt(
    "pavan-n-patil/storage-decision-prompt",
)
llm = get_shared_llm()

structured_llm = llm.with_structured_output(StorageDecision, method="json_mode")

storage_decision_chain: RunnableSequence = prompt | structured_llm

# if __name__ == "__main__":    
#     with open("schema.sql", "r") as f:
#         db_schema_content = f.read()
#     sample_input = {
#         "raw_text": "Index this website https://example.com for future retrieval of its content.",
#         "user_id": os.environ.get("USER_ID", "testuser"),
#         "org_id": os.environ.get("ORG_ID", "testorg"),
#         "source": "manager_chat",
#         "db_schema": db_schema_content,
#         "allowed_categories": list(ALLOWED_CATEGORIES),
#         "allowed_subcategories": {k: list(v) for k, v in ALLOWED_SUBCATEGORIES.items()},
#         "now_iso": datetime.now().isoformat()
#     }
#     result = normalize_chain.invoke(sample_input)
#     url_detector_result = url_detector.invoke({"user_input": sample_input["raw_text"]})
#     print("Normalized Memory:") 
#     print(result.model_dump_json(indent=2))
    # storage_decision_chain_input = {
    #     "raw_text":"Index this website https://example.com for future retrieval of its content.",
    # }
    # storage_decision_result = storage_decision_chain.invoke(storage_decision_chain_input)
    # print(storage_decision_result.model_dump_json(indent=2))