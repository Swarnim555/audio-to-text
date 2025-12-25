"""
Standalone test script - Drop any audio file and get god-level transcription
Usage: python test_audio.py path/to/your/audio.m4a
"""

import whisper
import sys
from audio_processor import process_audio_intelligently

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_audio.py <audio_file_path>")
        sys.exit(1)
    
    audio_path = sys.argv[1]
    
    print("Loading Whisper model (large-v3)...")
    model = whisper.load_model("medium")
    
    print(f"\nTranscribing: {audio_path}")
    print("=" * 60)
    
    result = process_audio_intelligently(model, audio_path)
    
    print(f"\n✓ TRANSCRIPTION ({result['language'].upper()}):\n")
    print(result['text'])
    print(f"\n✓ Confidence: {result['confidence']}")
    print("=" * 60)

if __name__ == "__main__":
    main()