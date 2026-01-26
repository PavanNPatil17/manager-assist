
import sys
from pathlib import Path

# Add project root to path to run directly the file
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from graph.save.save_graph_state import NormalizedMemory
from graph.save.constants import ALLOWED_CATEGORIES, ALLOWED_SUBCATEGORIES
from configuration import get_shared_llm
from langchain_core.runnables import RunnableSequence
from langchain_core.prompts import ChatPromptTemplate
import os 
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
from langsmith import Client

client = Client()
prompt = client.pull_prompt(
    "pavan-n-patil/normalization",
)

llm = get_shared_llm()

structured_llm = llm.with_structured_output(NormalizedMemory, method="json_mode")

normalize_chain: RunnableSequence = prompt | structured_llm

# if __name__ == "__main__":    
#     with open("schema.sql", "r") as f:
#         db_schema_content = f.read()
#     sample_input = {
#         "raw_text": "On March 15th, we need to finalize the budget of $75,000 for the new project with Acme Corp. Please coordinate with Jane Doe and ensure the marketing team is looped in. Also, remember to schedule a follow-up meeting next Monday to discuss the hiring of two new software engineers.",
#         "user_id": os.environ.get("USER_ID", "testuser"),
#         "org_id": os.environ.get("ORG_ID", "testorg"),
#         "source": "manager_chat",
#         "db_schema": db_schema_content,
#         "allowed_categories": list(ALLOWED_CATEGORIES),
#         "allowed_subcategories": {k: list(v) for k, v in ALLOWED_SUBCATEGORIES.items()},
#         "now_iso": datetime.now().isoformat()
#     }
#     result = normalize_chain.invoke(sample_input)
#     print(result.model_dump_json(indent=2))