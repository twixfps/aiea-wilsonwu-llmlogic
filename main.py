from openai import OpenAI
from dotenv import load_dotenv
from pyswip import Prolog
import tempfile
import re

load_dotenv()
client = OpenAI()

problem = """
Wilson is an auditor.
Every auditor knows Kubernetes.
Does Wilson know Kubernetes?
"""

prompt = f"""
Convert this English logic problem into Prolog.

You MUST output:
1. At least one fact.
2. At least one rule.
3. One query comment at the end.

Return ONLY Prolog code. No markdown.

Example format:
auditor(wilson).
knows_kubernetes(X) :- auditor(X).
% query: knows_kubernetes(wilson)

Problem:
{problem}
"""

response = client.responses.create(
    model="gpt-4.1-mini",
    input=prompt
)

prolog_text = response.output_text.strip()

print("Generated Prolog:")
print(prolog_text)

query_match = re.search(r"%\s*query:\s*(.+)", prolog_text)
query = query_match.group(1).strip()

prolog_code = re.sub(r"%\s*query:.*", "", prolog_text).strip()

with tempfile.NamedTemporaryFile(mode="w", suffix=".pl", delete=False) as f:
    f.write(prolog_code)
    filename = f.name

prolog = Prolog()
prolog.consult(filename)

result = list(prolog.query(query))

print("\nQuery:")
print(query)

print("\nResult:")
print("TRUE" if result else "FALSE")