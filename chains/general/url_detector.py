from pydantic import BaseModel, Field
from typing import List
from langsmith import Client
from configuration import get_shared_llm
from langchain_core.runnables import RunnableSequence
from dotenv import load_dotenv
load_dotenv()

from langsmith import Client

client = Client()
prompt = client.pull_prompt(
    "pavan-n-patil/url-detector",
)

llm = get_shared_llm()

class Urls(BaseModel):
    has_urls: bool = Field(
        description="True if the text contains any URLs (http/https), False otherwise"
    )
    urls: List[str] = Field(
        default_factory=list,
        description="Array of detected URLs from the user input. Extract all HTTP/HTTPS URLs found in the text. Empty list if no URLs found."
    )

structured_llm = llm.with_structured_output(Urls)

url_detector: RunnableSequence = prompt | structured_llm