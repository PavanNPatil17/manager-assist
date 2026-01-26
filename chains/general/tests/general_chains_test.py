from dotenv import load_dotenv

from pprint import pprint
from chains.general.intent_classifier import intent_classifier
from chains.general.url_detector import url_detector
from chains.general.response_shaper  import response_shaper

load_dotenv()

def test_intent_classifier():
    """Test the intent classifier chain."""
    test_input = "Who is good in spring boot development?"
    result = intent_classifier.invoke({"user_input": test_input})
    pprint(result)
    assert result.intent in ["save", "retrieve"]

def test_intent_classifier_save():
    """Test intent classifier with save intent."""
    test_input = "Remember that John is an expert in machine learning"
    result = intent_classifier.invoke({"user_input": test_input})
    pprint(result)
    assert result.intent == "save"

def test_intent_classifier_retrieve():
    """Test intent classifier with retrieve intent."""
    test_input = "What do you know about Python developers?"
    result = intent_classifier.invoke({"user_input": test_input})
    pprint(result)
    assert result.intent == "retrieve"

def test_intent_classifier_complex_query():
    """Test intent classifier with complex query."""
    test_input = "Find me someone who has experience with React and TypeScript"
    result = intent_classifier.invoke({"user_input": test_input})
    pprint(result)
    assert result.intent in ["save", "retrieve"]

def test_url_detector_with_url():
    """Test URL detector with input containing URLs."""
    test_input = "Check out this article https://example.com/article"
    result = url_detector.invoke({"user_input": test_input})
    pprint(result)
    assert result.has_urls is True
    assert len(result.urls) > 0

def test_url_detector_without_url():
    """Test URL detector with input not containing URLs."""
    test_input = "This is just a regular message without any links"
    result = url_detector.invoke({"user_input": test_input})
    pprint(result)
    assert result.has_urls is False

def test_url_detector_multiple_urls():
    """Test URL detector with multiple URLs."""
    test_input = "Visit https://example.com and http://test.org for more info"
    result = url_detector.invoke({"user_input": test_input})
    pprint(result)
    assert result.has_urls is True
    assert len(result.urls) >= 2

def test_response_shaper():
    """Test the response shaper chain."""
    test_input = {
        "intent": "retrieve",
        "save_retrieve_response": "{'raw_text': 'What i like?', 'retrieve': True, 'generation': 'You like Rekha.'}"
    }
    result = response_shaper.invoke(test_input)
    pprint(result)
    assert "Rekha" in result.final_ai_message

def test_response_shaper_llm():
    """Test the response shaper chain."""
    test_input = {
        "intent": "retrieve",
        "save_retrieve_response": "{'raw_text': 'What is the capital of France?', 'retrieve': False, 'llm_result': 'Paris.'}"
    }
    result = response_shaper.invoke(test_input)
    pprint(result)
    assert "Paris" in result.final_ai_message