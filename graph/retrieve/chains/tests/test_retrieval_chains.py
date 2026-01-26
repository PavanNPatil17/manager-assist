import pytest
from graph.retrieve.chains.retrieval_precheck_gate import retrieval_precheck_gate, RetrievalPrecheckResult

@pytest.mark.parametrize("user_input,expected", [
    # Should trigger retrieval
    ("Who in my team has experience with Python?", True),
    ("Show me the history of our last project discussion.", True),
    ("What decisions did we make about remote work?", True),
    # Should NOT trigger retrieval
    ("Hello!", False),
    ("What can you do?", False),
])
def test_retrieval_precheck_gate(user_input, expected):
    # Simulate the chain input
    input_data = {"user_input": user_input}
    result = retrieval_precheck_gate.invoke(input_data)
    assert isinstance(result, RetrievalPrecheckResult)
    assert result.retrieve == expected
    assert 0 <= result.confidence <= 1
    assert isinstance(result.short_reason, str)
    assert len(result.short_reason) > 0
