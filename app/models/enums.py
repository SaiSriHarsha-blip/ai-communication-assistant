from enum import Enum

class Platform(str, Enum):
    """Supported communication platforms."""
    WHATSAPP = "whatsapp"
    GMAIL = "gmail"
    INSTAGRAM = "instagram"
    LINKEDIN = "linkedin"
    SMS = "sms"

class Relationship(str, Enum):
    """Types of relationships with the recipient."""
    FAMILY = "family"
    FRIEND = "friend"
    MANAGER = "manager"
    HR = "hr"
    PROFESSOR = "professor"
    COLLEAGUE = "colleague"
    CLIENT = "client"

class Language(str, Enum):
    """Supported languages for messages."""
    ENGLISH = "english"
    TELUGU = "telugu"
    HINDI = "hindi"
    MIXED = "mixed"

class Tone(str, Enum):
    """Tones available for the message."""
    CASUAL = "casual"
    PROFESSIONAL = "professional"
    FRIENDLY = "friendly"
    RESPECTFUL = "respectful"
    FORMAL = "formal"
    APOLOGETIC = "apologetic"
