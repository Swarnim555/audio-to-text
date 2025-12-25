"""
FIX CORRUPTED WHISPER MODEL
Run this once to clear cache and re-download clean model
"""

import os
import shutil

# Find Whisper cache location
cache_dir = os.path.expanduser("~/.cache/whisper")
if os.name == 'nt':  # Windows
    cache_dir = os.path.join(os.environ['USERPROFILE'], '.cache', 'whisper')

print("="*70)
print("  FIXING WHISPER MODEL CACHE")
print("="*70)
print(f"\nCache location: {cache_dir}\n")

if os.path.exists(cache_dir):
    print("🗑️  Deleting corrupted cache...")
    shutil.rmtree(cache_dir)
    print("✅ Cache deleted!\n")
else:
    print("ℹ️  No cache found (already clean)\n")

print("="*70)
print("  NOW DOWNLOADING FRESH MODEL...")
print("="*70)
print("\nThis will take 2-5 minutes...\n")

import whisper

# Download fresh model
model = whisper.load_model("medium")

print("\n" + "="*70)
print("  ✅ MODEL FIXED AND READY!")
print("="*70)
print("\nNow run: python app.py\n")