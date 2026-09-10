from app.services.response_parser import append_source_citations, parse_travel_response


def test_parse_travel_response_extracts_sections_and_sources():
    answer = """A concise Jaipur plan.

🏨 Accommodation:
- Heritage guesthouse

💰 Budget Summary:
- Total: INR 5000

### Sources
- Rajasthan guide (relevance: 0.88)
"""

    parsed = parse_travel_response(answer)

    assert parsed.summary == "A concise Jaipur plan."
    assert parsed.accommodation == ["Heritage guesthouse"]
    assert parsed.budget_summary == ["Total: INR 5000"]
    assert parsed.sources[0].source == "Rajasthan guide"
    assert parsed.sources[0].relevance == 0.88


def test_append_source_citations_is_idempotent():
    retrieved = [{"metadata": {"source": "guide.pdf"}, "distance": 0.2}]
    answer = "A grounded answer."

    cited = append_source_citations(answer, retrieved)

    assert "### Sources" in cited
    assert "guide.pdf" in cited
    assert append_source_citations(cited, retrieved) == cited