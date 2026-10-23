import pytest
from tools import get_ticket, lookup_kb_article

def test_get_ticket_found():
    ticket = get_ticket("T-102")

    assert ticket["subject"] == "VPN keeps timing out"

def test_get_ticket_not_found():
    with pytest.raises(ValueError):
        get_ticket("T-999")

def test_kb_exact_topic():
    article = lookup_kb_article("printer")

    assert "KB-2" in article        

def test_kb_topic_inside_longer_text():
    article = lookup_kb_article("VPN keeps timing out")

    assert "KB-1" in article

def test_kb_no_match():
    with pytest.raises(ValueError):
        lookup_kb_article("billing")


