from pathlib import Path
from pyswip import Prolog
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from pydantic import Field
import re

KB_FILE = Path(__file__).parent / "nba_kb.pl"

prolog = Prolog()
prolog.consult(str(KB_FILE))

with open(KB_FILE, "r", encoding="utf-8") as file:
    kb_text = file.read()

sections = kb_text.split("\n\n")

documents = [
    Document(page_content=section)
    for section in sections
    if section.strip()
]


class KnowledgeBaseRetriever(BaseRetriever):
    documents: list[Document] = Field(default_factory=list)

    def _get_relevant_documents(self, query: str, *, run_manager=None):
        words = re.findall(r"[a-zA-Z_]+", query.lower())
        matches = []

        for document in self.documents:
            text = document.page_content.lower()

            if any(word in text for word in words):
                matches.append(document)

        return matches[:5]


retriever = KnowledgeBaseRetriever(documents=documents)


def get_team(query):
    match = re.search(r"\(([^)]+)\)", query)

    if match:
        return match.group(1)

    return None


def print_trace(query, result):
    team = get_team(query)

    print("\nInference Trace:")
    print("Goal:", query)

    if "historically_winning" in query and team:
        titles = list(prolog.query(f"championships({team}, Titles)"))

        if titles:
            count = titles[0]["Titles"]
            print(f"Fact: championships({team}, {count})")
            print("Rule: historically_winning(Team) requires Titles >= 6")
            print(f"Check: {count} >= 6 -> {count >= 6}")

    elif "highly_successful" in query and team:
        titles = list(prolog.query(f"championships({team}, Titles)"))

        if titles:
            count = titles[0]["Titles"]
            print(f"Fact: championships({team}, {count})")
            print("Rule: highly_successful(Team) requires Titles >= 10")
            print(f"Check: {count} >= 10 -> {count >= 10}")

    elif "eastern_team" in query and team:
        conference = list(prolog.query(f"conference({team}, Conference)"))

        if conference:
            value = conference[0]["Conference"]
            print(f"Fact: conference({team}, {value})")
            print("Rule: eastern_team(Team) requires conference(Team, east)")

    elif "western_team" in query and team:
        conference = list(prolog.query(f"conference({team}, Conference)"))

        if conference:
            value = conference[0]["Conference"]
            print(f"Fact: conference({team}, {value})")
            print("Rule: western_team(Team) requires conference(Team, west)")

    print(f"Therefore: {query} -> {result}")


def query_logic(query):
    print("\nQuery:", query)

    retrieved_docs = retriever.invoke(query)

    print("\nRAG Context:")
    for doc in retrieved_docs:
        print(doc.page_content)

    try:
        results = list(prolog.query(query))
        result = len(results) > 0
    except Exception as error:
        print("Prolog error:", error)
        return

    print_trace(query, result)

    print("\nResult:", result)


if __name__ == "__main__":
    query_logic("historically_winning(lakers)")
    query_logic("historically_winning(heat)")