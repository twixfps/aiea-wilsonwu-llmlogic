from z3 import *

# NBA facts from Task 4
teams = ["lakers", "celtics", "warriors", "bulls", "heat"]

championships = {
    "lakers": 17,
    "celtics": 18,
    "warriors": 7,
    "bulls": 6,
    "heat": 3
}

conference = {
    "lakers": "west",
    "warriors": "west",
    "celtics": "east",
    "bulls": "east",
    "heat": "east"
}


def historically_winning(team):
    return championships[team] >= 6


print("=== Task 4 NBA KB Tests ===")

print("\nHistorically winning teams:")
for team in teams:
    if historically_winning(team):
        print("-", team)

print("\nWestern Conference teams:")
for team in teams:
    if conference[team] == "west":
        print("-", team)

print("\nCeltics championships:")
print(championships["celtics"])

print("\nIs Miami historically winning?")
print(historically_winning("heat"))