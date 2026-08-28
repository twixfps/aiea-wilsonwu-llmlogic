from backward_chaining import KnowledgeBase


kb = KnowledgeBase()

kb.add_fact(("parent", "alice", "bob"))
kb.add_fact(("parent", "bob", "charlie"))
kb.add_fact(("human", "alice"))

kb.add_rule(
    ("grandparent", "?x", "?z"),
    [
        ("parent", "?x", "?y"),
        ("parent", "?y", "?z")
    ]
)

kb.add_rule(
    ("mortal", "?x"),
    [
        ("human", "?x")
    ]
)


tests = [
    (("human", "alice"), True),
    (("mortal", "alice"), True),
    (("grandparent", "alice", "charlie"), True),
    (("grandparent", "alice", "david"), False)
]


for goal, expected in tests:
    result = kb.prove(goal)

    print("Goal:", goal)
    print("Result:", result)
    print("Expected:", expected)
    print("PASS" if result == expected else "FAIL")
    print()