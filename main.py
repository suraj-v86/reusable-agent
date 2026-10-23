from agent import run_agent
from tools import TOOL_SCHEMAS, REGISTRY

SYSTEM = """
You are a support assistant. Use tools to look up facts. Do not guess.
If the data does not contain something, say it is not available.
Call each tool at most once unless a call failed.
"""

question = input("Enter your query: ")

answer, trace = run_agent(question, TOOL_SCHEMAS, REGISTRY, SYSTEM)

print("Question:", question)
print("Trace:", trace)
print("Answer:", answer)