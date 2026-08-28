from pathlib import Path
from typing import TypedDict
from pyswip import Prolog
from langchain_core.documents import Document
from langgraph.graph import StateGraph, START, END
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


class GraphState(TypedDict):
    query: str
    context: list[str]
    relevant: bool
    refined: bool
    result: bool


def retrieve(state: GraphState):
    query = state["query"]
    words = re.findall(r"[a-zA-Z_]+", query.lower())

    matches = []

    for document in documents:
        text = document.page_content.lower()

        if any(word in text for word in words):
            matches.append(document.page_content)

    print("\n--- RETRIEVE ---")
    for match in matches[:3]:
        print(match)

    return {
        "context": matches[:3],
        "refined": False
    }


def judge_relevance(state: GraphState):
    query = state["query"]
    context = state["context"]

    predicate = query.split("(")[0]

    relevant = any(
        predicate in section
        for section in context
    )

    print("\n--- RELEVANCE CHECK ---")
    print("Relevant:", relevant)

    return {"relevant": relevant}


def choose_next_step(state: GraphState):
    if state["relevant"]:
        return "prolog"

    return "refine"


def refine(state: GraphState):
    query = state["query"]

    print("\n--- REFINEMENT ---")
    print("Initial context was not sufficient.")
    print("Retrieving additional knowledge...")

    predicate = query.split("(")[0]
    team_match = re.search(r"\(([^)]+)\)", query)
    team = team_match.group(1) if team_match else ""

    refined_context = []

    for document in documents:
        text = document.page_content.lower()

        if predicate in text or team in text:
            refined_context.append(document.page_content)

    return {
        "context": refined_context,
        "relevant": True,
        "refined": True
    }


def run_prolog(state: GraphState):
    query = state["query"]

    print("\n--- PROLOG INFERENCE ---")

    try:
        results = list(prolog.query(query))
        result = len(results) > 0
    except Exception as error:
        print("Prolog error:", error)
        result = False

    print("Goal:", query)
    print("Result:", result)

    return {"result": result}


workflow = StateGraph(GraphState)

workflow.add_node("retrieve", retrieve)
workflow.add_node("relevance", judge_relevance)
workflow.add_node("refine", refine)
workflow.add_node("prolog", run_prolog)

workflow.add_edge(START, "retrieve")
workflow.add_edge("retrieve", "relevance")

workflow.add_conditional_edges(
    "relevance",
    choose_next_step,
    {
        "prolog": "prolog",
        "refine": "refine"
    }
)

workflow.add_edge("refine", "prolog")
workflow.add_edge("prolog", END)

graph = workflow.compile()


def query_logic(query):
    print("\n==============================")
    print("Query:", query)

    result = graph.invoke({
        "query": query,
        "context": [],
        "relevant": False,
        "refined": False,
        "result": False
    })

    print("\nFinal Result:", result["result"])


if __name__ == "__main__":
    query_logic("historically_winning(lakers)")
    query_logic("historically_winning(heat)")