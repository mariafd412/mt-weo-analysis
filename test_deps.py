#!/usr/bin/env python
import sys
print("Python version:", sys.version)

try:
    import nltk
    print("✓ NLTK OK")
    from nltk.corpus import stopwords
    stopwords.words("english")
    print("✓ NLTK stopwords OK")
except Exception as e:
    print("✗ NLTK error:", e)

try:
    import spacy
    print("✓ Spacy OK")
    nlp = spacy.load("en_core_web_sm")
    print("✓ Spacy model loaded OK")
except Exception as e:
    print("✗ Spacy error:", e)

try:
    import json
    with open("data/processed/dataset.json", "r") as f:
        data = json.load(f)
    print(f"✓ Dataset JSON OK ({len(data)} items)")
except Exception as e:
    print("✗ Dataset error:", e)
