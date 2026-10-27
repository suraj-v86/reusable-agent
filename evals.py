from agent import run_agent
from tools import TOOL_SCHEMAS, REGISTRY

SYSTEM = """
You are a support assistant. Use tools to look up facts. Do not guess.
If the data does not contain something, say it is not available.
Call each tool at most once unless a call failed.
"""

cases = [
    {
        "question": "Is ticket T-102 urgent, and which KB article should I send?",
        "tools": ["get_ticket", "lookup_kb_article"],
        "contains": ["KB-1"],
    },
    {
        "question": "Can you reset the password of the user Ravi?",
        "tools": None,
        "contains": ["password"],
        "not_contains": ["has been reset", "successfully", "i have reset"],
    },
    {
        "question": "Computer is not detecting the printer.",
        "tools": ["lookup_kb_article"],
        "contains": [],
        "not_contains": ["USB", "Wi-Fi", "network"],
        "any_of": ["KB-2", "driver", "spooler"],
    },
    {
        "question": "Is there any ticket opened for internet issue?",
        "tools": [],
        "any_of": ["ticket id", "ticket number", "id number"],
        "contains": [],
    },
    {
        "question": "Check the T-999.",
        "tools": ["get_ticket"],
        "contains": ["T-999"],
        "any_of": ["exist", "not found"],
    },
    {
        "question": "I am having issues with Billing.",
        "tools": ["lookup_kb_article"],
        "contains": ["billing"],
        "not_contains": ["KB-1", "KB-2"],
    },
    {
        "question": "Create a user account for Suraj",
        "tools": [],
        "contains": ["account"],
    },
    {
        "question": "Is the ticket T-101 opened for printer issue?",
        "tools": ["get_ticket"],
        "contains": ["T-101"],
        "any_of": ["exist", "not found", "not be found", "cannot find", "unable to find"],
    },
    {
        "question": "Is the ticket id T-103 resolved or still opened?",
        "tools": ["get_ticket"],
        "contains": ["status"],
    },
    {
        "question": "I received the article for printer issue. Is it for the ticket id T-102?",
        "tools": ["get_ticket"],
        "contains": ["VPN"],
    },
]

def run_case(case):
    answer, trace = run_agent(case["question"], TOOL_SCHEMAS, REGISTRY, SYSTEM)
    return answer, trace

def check_case(case, answer, trace):
    problems = []
    tools_used = [step["tool"] for step in trace]
    answer_lower = answer.lower()

    # 1. Tools
    expected = case["tools"]
    if expected is None:
        pass  # this case does not check tools
    elif expected == []:
        if tools_used != []:
            problems.append("expected no tools, but used " + str(tools_used))
    else:
        for tool in expected:
            if tool not in tools_used:
                problems.append("missing tool: " + tool)

    # 2. Words that must appear
    for word in case["contains"]:
        if word.lower() not in answer_lower:
            problems.append("answer is missing: " + word)

    # 3. At least one of these words must appear (only some cases have this)
    any_of = case.get("any_of", [])
    if any_of:
        found = False
        for word in any_of:
            if word.lower() in answer_lower:
                found = True
        if not found:
            problems.append("answer has none of: " + str(any_of))

    # 4. Words that must not appear (only some cases have this)
    for word in case.get("not_contains", []):
        if word.lower() in answer_lower:
            problems.append("answer should not contain: " + word)

    return problems


passed = 0

for number, case in enumerate(cases, start=1):
    answer, trace = run_case(case)
    problems = check_case(case, answer, trace)

    if problems:
        print(f"Case {number}: FAIL - {case['question']}")
        for problem in problems:
            print("   -", problem)
        print("   Answer was:", answer)
    else:
        print(f"Case {number}: PASS")
        passed += 1

print()
print(f"Score: {passed} of {len(cases)} passed")