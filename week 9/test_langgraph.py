from langgraph_logic import graph


def test_query(query, expected):
    result = graph.invoke({
        "query": query,
        "context": [],
        "relevant": False,
        "refined": False,
        "result": False
    })

    actual = result["result"]

    print("\nQuery:", query)
    print("Result:", actual)
    print("Expected:", expected)

    if actual == expected:
        print("PASS")
    else:
        print("FAIL")


test_query("historically_winning(lakers)", True)
test_query("historically_winning(heat)", False)
test_query("highly_successful(celtics)", True)
test_query("eastern_team(bulls)", True)
test_query("western_team(lakers)", True)    