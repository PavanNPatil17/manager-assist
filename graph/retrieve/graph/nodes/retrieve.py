from typing import Any, Dict

from graph.retrieve.graph.state import GraphState
from configuration import get_vector_store
from graph.save.chains.save_postgres import get_memory_by_id
from dotenv import load_dotenv
load_dotenv()

def retrieve(state: GraphState) -> Dict[str, Any]:
    print("---RETRIEVE---")
    question = state["question"]
    documents = get_vector_store().similarity_search(question,k=5)
    postgres_records = get_postgres_records(documents)
    if postgres_records and len(postgres_records) > 0:
        print(f"---FOUND {len(postgres_records)} POSTGRES RECORDS FOR RETRIEVED DOCUMENTS---")
        for i, record in enumerate(postgres_records):
            documents[i].metadata["postgres_record"] = record
    print(f"---RETRIEVED {len(documents)} DOCUMENTS---")
    for doc in documents:
        print(doc)
    return {"documents": documents, "question": question}

def get_postgres_records(documents):
    records = []
    for doc in documents:
        postgres_id = doc.metadata.get("postgres_id")
        if postgres_id:
            record = get_memory_by_id(postgres_id)
            if record:
                records.append(record)
    return records