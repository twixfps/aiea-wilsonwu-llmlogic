from pathlib import Path

from pyswip import Prolog


def run_query(prolog: Prolog, query: str) -> None:
    results = list(prolog.query(query))
    print(f"Query: {query}")
    print(f"Results: {results}")
    print()


def main() -> None:
    kb_path = Path(__file__).parent / "nba_kb.pl"

    if not kb_path.exists():
        raise FileNotFoundError(f"Knowledge base not found: {kb_path}")

    prolog = Prolog()
    prolog.consult(str(kb_path))

    run_query(prolog, "historically_winning(lakers)")
    run_query(prolog, "historically_winning(heat)")
    run_query(prolog, "historically_winning(X)")
    run_query(prolog, "conference(lakers, X)")
    run_query(prolog, "championships(celtics, X)")


if __name__ == "__main__":
    main()