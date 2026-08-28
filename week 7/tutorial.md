# Forward Chaining

Forward chaining takes known facts and applies rules to them in order to determine new facts.

```text
human(alice)

human(X) -> mortal(X)
```

The machine knows `human(alice)` exists, applies the rule, and learns `mortal(alice)` exists.

We use forward chaining when we want to determine many conclusions from a knowledge base.

# Backward Chaining

Backward chaining takes a goal and works backwards to see if it can prove that goal.

Let's say our goal is:

```text
grandparent(alice, charlie)
```

The machine looks through all the rules and finds:

```text
parent(X, Y) AND parent(Y, Z) -> grandparent(X, Z)
```

It then attempts to prove:

```text
parent(alice, Y)
parent(Y, charlie)
```

The knowledge base tells us that:

```text
parent(alice, bob)
parent(bob, charlie)
```

Therefore, `Y` must be `bob`, and we are able to prove our original goal.

# My Implementation

My implementation represents predicates as Python tuples.

Example:

```python
("parent", "alice", "bob")
```

Variables are any strings that start with a question mark.

```python
("?x", "?y")
```

My program has a unification function to match variables to constants.

The backward chaining function first checks to see if what it is trying to prove matches a known fact.

If not, it searches for a rule that concludes what it wants to prove.

The program then recursively tries to prove every premise of that rule.

If every premise can be proven, then we assume the original goal is true. Otherwise, it keeps searching or returns false.
