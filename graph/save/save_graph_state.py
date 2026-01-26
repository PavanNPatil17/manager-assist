from pydantic import BaseModel, Field, field_validator
from typing import Dict, List, Optional, Union, Literal, Annotated
from datetime import date, datetime

def merge_storage_status(left: Optional[Dict[str, str]], right: Optional[Dict[str, str]]) -> Dict[str, str]:
    """Merge storage status dictionaries from different nodes"""
    if left is None:
        left = {}
    if right is None:
        right = {}
    return {**left, **right}

FactValue = Union[str, int, float, bool, List[Union[str, int, float, bool]]]

class NormalizedMemory(BaseModel):
    title: Optional[str] = Field(None, description="Short descriptive title for the memory")
    summary: Optional[str] = Field(None, description="Brief summary of the content")

    category: List[str] = Field(description="List of categories from allowed categories. Can include multiple if text spans multiple topics. Example: ['budget', 'reminder', 'hiring']")
    subcategory: Optional[str] = Field(None, description="Subcategory if applicable")

    entities: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="REQUIRED: Mapping of entity types to lists of entity names. Types: person, company, project, client, email, team, product. ALWAYS extract entities from the text. Example: {'person': ['John Doe'], 'company': ['OpenAI']}"
    )
    facts: Dict[str, FactValue] = Field(
        default_factory=dict,
        description="REQUIRED: Structured key-value facts extracted from text. Keys should be descriptive like 'profession', 'birth_date', 'skills', 'budget', 'status'. ALWAYS extract facts from the text. Example: {'profession': 'software engineer', 'birth_date': '1990-01-01', 'interests': ['coding']}"
    )

    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score between 0 and 1")

    source: str = Field(description="Source of the information")

    memory_date: Optional[date] = Field(None, description="Primary date mentioned in the text (YYYY-MM-DD format)")
    created_at: datetime = Field(description="Timestamp when this was created (ISO 8601)")
    
    @field_validator('memory_date', mode='before')
    @classmethod
    def parse_memory_date(cls, v):
        """Convert list format [2026, 1, 11] to date object"""
        if v is None:
            return v
        if isinstance(v, list) and len(v) == 3:
            return date(v[0], v[1], v[2])
        if isinstance(v, str):
            return date.fromisoformat(v)
        return v

class GraphState(BaseModel):
    """Extended state for the save graph workflow"""
    raw_text: str = Field(description="Original user input text")
    storage_location: Optional[List[Literal["POSTGRES", "MILVUS", "WEBSITE_INDEX"]]] = Field(
        None, 
        description="Storage location decided by storage_decision node"
    )
    storage_intent: Optional[Literal["STRUCTURED_AND_VECTOR", "VECTOR_ONLY"]] = Field(
        None, 
        description="Storage decision made by storage_decision node"
    )
    normalized_memory: Optional[NormalizedMemory] = Field(
        None,
        description="Normalized memory extracted from the raw text"
    )
    postgres_id: Optional[str] = Field(
        None,
        description="UUID of the memory record in PostgreSQL"
    )
    storage_status: Annotated[Dict[str, str], merge_storage_status] = Field(
        default_factory=dict,
        description="Status of storage operations for different storage locations"
    )