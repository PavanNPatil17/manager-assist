import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from graph.save.chains.normalize import normalize_chain
from graph.save.chains.storage_decision import storage_decision_chain
from chains.general.url_detector import url_detector
from graph.save.constants import ALLOWED_CATEGORIES, ALLOWED_SUBCATEGORIES
from datetime import datetime
import os

def test_storage_decision_structured_and_vector():
    """Test storage decision for structured and vector intent"""
    with open("schema.sql", "r") as f:
        db_schema_content = f.read()
    
    sample_input = {
        "raw_text": "We finalized the Q1 budget with Acme Corp. Total allocated: $500,000. Contact: John Doe (john@acme.com).",
        "user_id": os.environ.get("USER_ID", "testuser"),
        "org_id": os.environ.get("ORG_ID", "testorg"),
        "source": "manager_chat",
        "db_schema": db_schema_content,
        "allowed_categories": list(ALLOWED_CATEGORIES),
        "allowed_subcategories": {k: list(v) for k, v in ALLOWED_SUBCATEGORIES.items()},
        "now_iso": datetime.now().isoformat()
    }
    
    result = normalize_chain.invoke(sample_input)
    url_detector_result = url_detector.invoke({"user_input": sample_input["raw_text"]})
    
    storage_decision_chain_input = {
        "normalized_json": result.model_dump(),
        "raw_text": sample_input["raw_text"],
        "detected_urls": url_detector_result.model_dump() 
    }
    
    storage_decision_result = storage_decision_chain.invoke(storage_decision_chain_input)
    
    assert storage_decision_result.storage_intent == "STRUCTURED_AND_VECTOR"
    assert 0.0 <= storage_decision_result.confidence <= 1.0


def test_storage_decision_vector_only():
    """Test storage decision for vector only intent"""
    with open("schema.sql", "r") as f:
        db_schema_content = f.read()
    
    sample_input = {
        "raw_text": "I'm thinking we should explore more innovative approaches to team collaboration in the future.",
        "user_id": os.environ.get("USER_ID", "testuser"),
        "org_id": os.environ.get("ORG_ID", "testorg"),
        "source": "manager_chat",
        "db_schema": db_schema_content,
        "allowed_categories": list(ALLOWED_CATEGORIES),
        "allowed_subcategories": {k: list(v) for k, v in ALLOWED_SUBCATEGORIES.items()},
        "now_iso": datetime.now().isoformat()
    }
    
    result = normalize_chain.invoke(sample_input)
    url_detector_result = url_detector.invoke({"user_input": sample_input["raw_text"]})
    
    storage_decision_chain_input = {
        "normalized_json": result.model_dump(),
        "raw_text": sample_input["raw_text"],
        "detected_urls": url_detector_result.model_dump() 
    }
    
    storage_decision_result = storage_decision_chain.invoke(storage_decision_chain_input)
    
    assert storage_decision_result.storage_intent == "VECTOR_ONLY"
    assert 0.0 <= storage_decision_result.confidence <= 1.0
    