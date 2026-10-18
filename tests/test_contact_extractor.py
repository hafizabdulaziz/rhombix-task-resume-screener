import pytest
from src.services.contact_extractor import ContactExtractor

def test_contact_extractor():
    sample_text = """
    John Doe
    Email: john.doe@example.com, contact@johndoe.io
    Phone: +1 (555) 123-4567, 5559876543
    Profiles:
    https://linkedin.com/in/johndoe
    github.com/johndoe-dev
    """
    contacts = ContactExtractor.extract_contacts(sample_text)
    assert "john.doe@example.com" in contacts["emails"]
    assert "contact@johndoe.io" in contacts["emails"]
    assert len(contacts["phones"]) > 0
    assert contacts["linkedin"] == "https://linkedin.com/in/johndoe"
    assert contacts["github"] == "github.com/johndoe-dev"

def test_empty_contacts():
    contacts = ContactExtractor.extract_contacts("")
    assert contacts["emails"] == []
    assert contacts["phones"] == []
    assert contacts["linkedin"] is None
    assert contacts["github"] is None
