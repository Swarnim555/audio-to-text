import re
import torch
import numpy as np

def process_audio_intelligently(model, audio_path):
    """
    God-level audio processing with automatic language detection
    and intelligent cleaning. NO PROMPTS NEEDED.
    """
    
    # Step 1: Transcribe with optimal settings
    result = model.transcribe(
        audio_path,
        language=None,  # Auto-detect Hindi/English/Hinglish
        task="transcribe",
        temperature=0.0,  # Deterministic (no randomness)
        beam_size=5,  # Better accuracy
        best_of=5,
        patience=1.0,
        
        # Anti-hallucination guards
        condition_on_previous_text=False,
        no_speech_threshold=0.6,
        logprob_threshold=-1.0,
        compression_ratio_threshold=2.4,
        
        # VAD (Voice Activity Detection)
        vad_filter=True,
        vad_parameters={
            "threshold": 0.5,
            "min_speech_duration_ms": 250,
            "min_silence_duration_ms": 2000
        }
    )
    
    raw_text = result["text"].strip()
    detected_lang = result.get("language", "unknown")
    
    # Step 2: Detect if output is garbage/hallucination
    if is_hallucination(raw_text, result.get("segments", [])):
        return {
            "text": "[Unable to transcribe - please speak clearly]",
            "language": detected_lang,
            "confidence": "low"
        }
    
    # Step 3: Clean the text based on detected language
    cleaned_text = clean_transcription(raw_text, detected_lang)
    
    return {
        "text": cleaned_text,
        "language": detected_lang,
        "confidence": "high"
    }


def is_hallucination(text, segments):
    """Detect if Whisper hallucinated garbage output"""
    
    # Empty or too short
    if len(text.strip()) < 3:
        return True
    
    # Repetitive nonsense (same word 7+ times)
    words = text.split()
    if len(words) > 6:
        unique_words = len(set(words))
        if unique_words <= 2:
            return True
    
    # Check for looping patterns
    if len(words) >= 4:
        # Check if same 2-word pattern repeats
        for i in range(len(words) - 3):
            pattern = f"{words[i]} {words[i+1]}"
            rest = " ".join(words[i+2:])
            if rest.count(pattern) >= 3:
                return True
    
    # Low confidence from segments
    if segments:
        avg_logprob = np.mean([s.get("avg_logprob", 0) for s in segments])
        if avg_logprob < -1.0:
            return True
        
        # Check compression ratio
        avg_compression = np.mean([s.get("compression_ratio", 1) for s in segments])
        if avg_compression > 2.4:
            return True
    
    return False


def clean_transcription(text, language):
    """
    Intelligent cleaning for Hindi, English, and Hinglish
    """
    
    # Step 1: Remove repetitions
    text = remove_phrase_repetition(text)
    
    # Step 2: Fix common Hindi OCR-like errors
    text = fix_hindi_errors(text)
    
    # Step 3: Fix Hinglish (technical English words in Hindi script)
    text = fix_hinglish(text)
    
    # Step 4: Normalize spacing and punctuation
    text = normalize_spacing(text)
    
    # Step 5: Fix broken Devanagari
    text = fix_devanagari(text)
    
    return text.strip()


def remove_phrase_repetition(text):
    """Remove repeated phrases and words"""
    words = text.split()
    cleaned = []
    
    for i, word in enumerate(words):
        # Skip if same as last 2 words (simple repetition)
        if len(cleaned) >= 2 and word == cleaned[-1] == cleaned[-2]:
            continue
        
        # Skip if part of repeating 3-word pattern
        if len(cleaned) >= 3:
            last_three = " ".join(cleaned[-3:])
            current_three = " ".join(cleaned[-2:] + [word])
            if last_three == current_three:
                continue
        
        cleaned.append(word)
    
    return " ".join(cleaned)


def fix_hindi_errors(text):
    """Fix common Hindi transcription errors"""
    
    CORRECTIONS = {
        # Greetings
        "सत स्री अकाल": "सत श्री अकाल",
        "सत सरी अकाल": "सत श्री अकाल",
        "सतसरीअकाल": "सत श्री अकाल",
        "नमसते": "नमस्ते",
        "नमसकार": "नमस्कार",
        
        # Common words
        "अबिननदन": "अभिनंदन",
        "अभिननदन": "अभिनंदन",
        "खुबसूरत": "खूबसूरत",
        "खुपसूरत": "खूबसूरत",
        "बिचरना": "बिछड़ना",
        "बिचड़ना": "बिछड़ना",
        
        # Pronouns
        "आप": "आप",
        "हम": "हम",
        "तुम": "तुम",
        
        # Common verbs
        "करना": "करना",
        "होना": "होना",
        "जाना": "जाना",
    }
    
    for wrong, correct in CORRECTIONS.items():
        text = text.replace(wrong, correct)
    
    return text


def fix_hinglish(text):
    """Convert technical English words back from Hindi script"""
    
    HINGLISH_MAP = {
        # Tech terms
        "माइक": "mic",
        "माइट": "mic",
        "टेस्टिंग": "testing",
        "टेस्ट": "test",
        "एपीआई": "API",
        "एपीआईकी": "API key",
        "की": "key",
        "बटन": "button",
        "क्लिक": "click",
        
        # Common English
        "हलो": "hello",
        "हैलो": "hello",
        "थैंक्यू": "thank you",
        "थैंक यू": "thank you",
        "सॉरी": "sorry",
        "ओके": "okay",
        "प्लीज": "please",
        "ईवनिंग": "evening",
        "मॉर्निंग": "morning",
        "जेंटलमेन": "gentleman",
        "लेडीज": "ladies",
        
        # Directions
        "इधर": "idhar",
        "उधर": "udhar",
    }
    
    for hindi, english in HINGLISH_MAP.items():
        # Replace whole words only
        text = re.sub(rf'\b{re.escape(hindi)}\b', english, text)
    
    return text


def normalize_spacing(text):
    """Clean up spacing and punctuation"""
    
    # Fix multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    # Fix repeated punctuation
    text = re.sub(r'([।.!?])\1+', r'\1', text)
    
    # Fix character repetition (e.g., हैैैै -> है)
    text = re.sub(r'(.)\1{3,}', r'\1', text)
    
    # Add space after Devanagari danda
    text = re.sub(r'।(\S)', r'। \1', text)
    
    return text


def fix_devanagari(text):
    """Fix broken Devanagari characters and matras"""
    
    # Fix separated matras (vowel marks)
    text = re.sub(r'(\S)\s+(़)', r'\1\2', text)  # Nukta
    text = re.sub(r'(\S)\s+(ा|ि|ी|ु|ू|े|ै|ो|ौ|ं|ः|्)', r'\1\2', text)  # Vowel marks
    
    # Fix broken conjuncts
    text = re.sub(r'्\s+', '्', text)
    
    return text