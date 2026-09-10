import re

from app.schemas.response import SourceCitation, TravelResponse

SECTION_NAMES = {
    "accommodation": "accommodation",
    "food": "food",
    "transport": "transport",
    "things to do": "things_to_do",
    "budget summary": "budget_summary",
}


def append_source_citations(answer: str, retrieved: list[dict]) -> str:
    if not retrieved or "sources" in answer.lower():
        return answer

    lines = [answer.rstrip(), "", "### Sources"]
    for item in retrieved:
        metadata = item.get("metadata") or {}
        source = metadata.get("source", "Knowledge base")
        distance = item.get("distance")
        relevance = max(0.0, min(1.0, 1.0 - float(distance))) if distance is not None else None
        suffix = f" (relevance: {relevance:.2f})" if relevance is not None else ""
        lines.append(f"- {source}{suffix}")
    return "\n".join(lines)


def parse_travel_response(answer: str) -> TravelResponse:
    sections: dict[str, list[str]] = {key: [] for key in SECTION_NAMES.values()}
    sources: list[SourceCitation] = []
    current_section: str | None = None
    summary = ""

    for raw_line in answer.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        source_match = re.match(r"[-*]\s*([^(:]+?)(?:\s*\(relevance:\s*([0-9.]+)\))?$", line, re.IGNORECASE)
        if current_section == "sources" and source_match:
            relevance = float(source_match.group(2)) if source_match.group(2) else None
            sources.append(SourceCitation(source=source_match.group(1).strip(), relevance=relevance))
            continue

        normalized = re.sub(r"[^a-z ]", "", line.lower()).strip().rstrip(":")
        if normalized in SECTION_NAMES:
            current_section = SECTION_NAMES[normalized]
            continue
        if normalized == "sources" or normalized == "references":
            current_section = "sources"
            continue

        if line.startswith("-") or line.startswith("*"):
            if current_section in sections:
                sections[current_section].append(line[1:].strip())
        elif not summary:
            summary = line.strip('"')

    return TravelResponse(answer=answer, summary=summary, sources=sources, **sections)