"""
Custom Dictionary - Add your own word corrections here!
The system will automatically use these corrections.
"""

# Add any misspellings you notice here
CUSTOM_CORRECTIONS = {
    # Format: "wrong spelling": "correct spelling"
    
    # Add gentleman variations
    "जनतलमन": "gentleman",
    "जेन्टलमैन": "gentleman",
    "जेंटलमेन": "gentleman",
    "जैंटलमैन": "gentleman",
    
    # Add any other words that get misspelled
    "एपनिंग": "evening",
    "ईवनिंग": "evening",
    "इवनिंग": "evening",
    
    # Morning
    "मोर्निंग": "morning",
    "मॉर्निंग": "morning",
    
    # Common Hindi words
    "कहानी": "कहानी",
    "किस्सा": "किस्सा",
    
    # Add more as you discover them...
}

# Words that should ALWAYS be in English (even if transcribed in Hindi)
FORCE_ENGLISH = [
    "gentleman",
    "ladies",
    "hello",
    "good morning",
    "good evening",
    "good afternoon",
    "good night",
    "thank you",
    "sorry",
    "excuse me",
    "please",
    "okay",
    "yes",
    "no",
]
