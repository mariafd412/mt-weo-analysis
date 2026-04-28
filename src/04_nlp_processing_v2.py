#!/usr/bin/env python3
"""
NLP Processing Script - Versión mejorada con logging
"""
import json
import sys
import os

# Setup paths
sys.path.insert(0, '/home/alexisfrankj/mt-weo-analysis')
os.chdir('/home/alexisfrankj/mt-weo-analysis')

print("=" * 60)
print("INICIANDO PROCESAMIENTO NLP")
print("=" * 60)

try:
    print("\n1. Importando spacy...")
    import spacy
    nlp = spacy.load("en_core_web_sm")
    print("   ✓ Spacy cargado")
except Exception as e:
    print(f"   ✗ Error con spacy: {e}")
    sys.exit(1)

try:
    print("\n2. Importando NLTK...")
    import nltk
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words("english"))
    print("   ✓ NLTK cargado")
except Exception as e:
    print(f"   ✗ Error con NLTK: {e}")
    sys.exit(1)

# Palabras importantes que no eliminar
keep_words = {"growth", "inflation", "crisis", "deficit"}
stop_words = stop_words - keep_words

def process_text(text):
    """Tokeniza y lematiza el texto"""
    doc = nlp(text)
    tokens = []
    for token in doc:
        if token.is_alpha:
            word = token.lemma_.lower()
            if word not in stop_words:
                tokens.append(word)
    return tokens

def extract_entities(text):
    """Extrae entidades NER (países y organizaciones)"""
    doc = nlp(text)
    countries = []
    orgs = []
    for ent in doc.ents:
        if ent.label_ == "GPE":
            countries.append(ent.text)
        elif ent.label_ == "ORG":
            orgs.append(ent.text)
    return countries, orgs

# Cargar dataset
print("\n3. Cargando dataset.json...")
INPUT_FILE = "data/processed/dataset.json"
OUTPUT_FILE = "data/processed/dataset_nlp.json"

try:
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"   ✓ Cargados {len(data)} párrafos")
except Exception as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

# Procesar
print(f"\n4. Procesando {len(data)} párrafos...")
new_data = []

for i, row in enumerate(data):
    if (i + 1) % 50 == 0:
        print(f"   [{i + 1}/{len(data)}]...")
    
    try:
        text = row["texto"]
        tokens = process_text(text)
        countries, orgs = extract_entities(text)
        
        row["tokens"] = tokens
        row["pais"] = countries
        row["organizacion"] = orgs
        new_data.append(row)
    except Exception as e:
        print(f"   ✗ Error en párrafo {i}: {e}")
        continue

print(f"\n5. Guardando resultados en {OUTPUT_FILE}...")
try:
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(new_data, f, indent=2, ensure_ascii=False)
    print(f"   ✓ Guardados {len(new_data)} párrafos procesados")
except Exception as e:
    print(f"   ✗ Error al guardar: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✓ ¡PROCESAMIENTO NLP COMPLETADO EXITOSAMENTE!")
print("=" * 60)
print(f"\nResultado: {OUTPUT_FILE}")
print(f"Total: {len(new_data)} párrafos con tokens, entidades de país y organización")
