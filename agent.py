from openai import OpenAI
import json

client = OpenAI()

def run_agent(user_message, tools, tool_functions, system_prompt, max_steps=8):
    # Conversation history. It starts with the user's question.
    input_list = [{"role": "user", "content": user_message}]
    trace = []

    for step in range(max_steps):
        response = client.responses.create(
            model="gpt-5.6-luna",
            instructions=system_prompt,
            input=input_list,
            tools=tools
        )

        # Keep everything the model returned in the history
        input_list += response.output

        # Collect the tool requests
        tool_calls = []
        for item in response.output:
            if item.type == "function_call":
                tool_calls.append(item)

        # No tool requests means the final answer is ready
        if not tool_calls:
            return response.output_text, trace

        # Run each requested tool
        for tool_call in tool_calls:
            arguments = json.loads(tool_call.arguments)
            function = tool_functions.get(tool_call.name)

            if function is None:
                result = "Error: unknown tool " + tool_call.name
            else:
                try:
                    result = function(**arguments)
                except Exception as e:
                    result = "Error: " + str(e)

            if not isinstance(result, str):
                result = json.dumps(result)

            input_list.append({
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": result
            })

            trace.append({
                "step": step,
                "tool": tool_call.name,
                "args": arguments,
                "output": result
            })

    return "Stopped: reached the maximum number of steps.", trace