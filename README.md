# Reusable AI Agent

## About this project
I built this project to learn how AI agents use multiple tools to answer a user's query.

## How it works
When a user enters a query, the LLM reads it and decides which tool it needs. The LLM does not run the tool itself. It sends a request, and Python executes the matching function and returns the output. Based on that output, the LLM decides whether a second function is needed. Once it has what it needs, the LLM combines the outputs and writes the final response to the user.

The loop has a maximum number of steps, so it cannot run forever. If a tool fails, the error is sent back to the LLM so it can tell the user.

## Example
Query: Is ticket T-102 urgent, and which KB article should I send?

```
Trace: [
  {'step': 0, 'tool': 'get_ticket', 'args': {'ticket_id': 'T-102'}, 'output': '{"id": "T-102", "subject": "VPN keeps timing out", "customer": "Acme Ltd"}'},
  {'step': 1, 'tool': 'lookup_kb_article', 'args': {'topic': 'VPN keeps timing out'}, 'output': 'KB-1: Reset VPN profile, update client, check firewall port 443.'}
]

Answer: Ticket T-102 is about VPN timeouts, but its urgency is not available in the ticket data.
Send KB-1: "Reset VPN profile, update client, check firewall port 443."
```

Note: The tickets and KB articles are sample dictionaries created only for this project.

## Project structure
- `main.py`: asks for a query and prints the answer
- `agent.py`: contains the reusable loop
- `tools.py`: contains the functions and their descriptions
- `test_tools.py`: contains the pytest tests for the tools

## How to run
1. Create and activate a virtual environment
2. `pip install -r requirements.txt`
3. Set your `OPENAI_API_KEY` environment variable
4. `python main.py`

The code uses the OpenAI Responses API. Check the model name in `agent.py` and change it if it is not available on your account.

To run the tests: `python -m pytest`

## What I learned
- How to write the functions and tool schemas so the agent can decide which tool to use for a query
- How to build the loop and handle errors with try/except
- How the system prompt shapes the agent's behavior
- How to write pytest tests to check the functions before running the agent

## Limitations and next steps
- I used sample tickets and KB articles that I created myself
- The tests cover the tools, not the LLM's behavior. An evaluation set is a next step
- I have not used retrieval-augmented generation (RAG) yet
- This is a simple project to learn how an agent reads a query, chooses tools, and builds a final answer from their output