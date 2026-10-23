import json

TICKETS = {
    "T-102": {"id": "T-102", "subject": "VPN keeps timing out", "customer": "Acme Ltd"},
    "T-103": {"id": "T-103", "subject": "Cannot print from laptop", "customer": "Beta Corp"},
}

KB = {
    "vpn": "KB-1: Reset VPN profile, update client, check firewall port 443.",
    "printer": "KB-2: Reinstall the driver and restart the print spooler.",
}

def get_ticket(ticket_id: str) -> dict:
    if ticket_id in TICKETS:
        return TICKETS[ticket_id]
    raise ValueError(f"Ticket {ticket_id} doesn't exist.")

def lookup_kb_article(topic: str) -> str:
    topic = topic.lower()
    for key, article in KB.items():
        if key in topic:
            return article
    raise ValueError(f"No KB article matches '{topic}'.")


TOOL_SCHEMAS = [
    {
        "type": "function",
        "name": "get_ticket",
        "description": "Fetch a support ticket by its ID",
        "parameters": {
            "type": "object",
            "properties": {
                "ticket_id": {
                    "type": "string"
                },
            },
            "required": ["ticket_id"]
        },
    },
    {
        "type": "function",
        "name": "lookup_kb_article",
        "description": "Search the knowledge base for an article matching a topic, such as vpn or printer.",
        "parameters": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string"
                },
            },
            "required": ["topic"]
        },
    },
    
]

REGISTRY = {
    "get_ticket": get_ticket,
    "lookup_kb_article": lookup_kb_article
}

if __name__ == "__main__":
    print(get_ticket("T-102"))
    print(lookup_kb_article("VPN timeout"))
    print(lookup_kb_article("printer"))
    try:
        print(lookup_kb_article("billing"))  
    except ValueError as e:
        print("Error:", e)

    


