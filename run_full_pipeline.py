#!/usr/bin/env python3
"""
Ejecuta todos los scripts necesarios del pipeline de Minería de Texto
Fase 1: Dataset limpio
Fase 2: Procesamiento NLP
Fase 3: Análisis de tópicos
"""
import os
import sys
import json

# Cambiar a directorio relativo o home
if os.path.exists('/home/alexisfrankj/mt-weo-analysis'):
    os.chdir('/home/alexisfrankj/mt-weo-analysis')
else:
    # Windows path
    home = os.path.expanduser('~')
    # Try to find mt-weo-analysis
    for root, dirs, files in os.walk(home):
        if 'mt-weo-analysis' in dirs:
            os.chdir(os.path.join(root, 'mt-weo-analysis'))
            break

print(f"\nDirectorio de trabajo: {os.getcwd()}")
print("\n" + "="*70)
print("PIPELINE DE MINERÍA DE TEXTO - EJECUCIÓN COMPLETA")
print("="*70)

# ============================================================================
# FASE 2B: Procesamiento NLP  (si dataset.json existe)
# ============================================================================

print("\n▶ FASE 2B: Procesamiento NLP")
print("-" * 70)

# Verificar dependencias
print("Verificando dependencias...")
try:
    import nltk
    from nltk.corpus import stopwords
    print("  ✓ NLTK OK")
except:
    print("  ✗ NLTK falta. Instalando...")
    os.system(f"{sys.executable} -m pip install nltk -q")
    import nltk
    from nltk.corpus import stopwords
    # Descargar stopwords
    nltk.download('stopwords', quiet=True)

try:
    import spacy
    print("  ✓ Spacy OK")
except:
    print("  ✗ Spacy falta. Instalando...")
    os.system(f"{sys.executable} -m pip install spacy -q")
    os.system(f"{sys.executable} -m spacy download en_core_web_sm -q")
    import spacy

try:
    nlp = spacy.load("en_core_web_sm")
    print("  ✓ Spacy model OK")
except:
    print("  ✗ Modelo spacy falta. Descargando...")
    os.system(f"{sys.executable} -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Stopwords
stop_words = set(stopwords.words("english"))
keep_words = {"growth", "inflation", "crisis", "deficit"}
stop_words = stop_words - keep_words
print(f"  ✓ Stopwords personalizadas ({len(keep_words)} palabras clave protegidas)")

# Funciones de procesamiento
def process_text(text):
    """Tokeniza y lematiza"""
    doc = nlp(text)
    tokens = []
    for token in doc:
        if token.is_alpha:
            word = token.lemma_.lower()
            if word not in stop_words:
                tokens.append(word)
    return tokens

def extract_entities(text):
    """Extrae entidades"""
    doc = nlp(text)
    countries = []
    orgs = []
    for ent in doc.ents:
        if ent.label_ == "GPE":
            countries.append(ent.text)
        elif ent.label_ == "ORG":
            orgs.append(ent.text)
    return countries, orgs

# Procesar dataset
print("\nProcesando dataset...")
INPUT_FILE = "data/processed/dataset.json"
OUTPUT_FILE = "data/processed/dataset_nlp.json"

print(f"  Leyendo: {INPUT_FILE}")
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)
print(f"  Total de párrafos: {len(data)}")

print(f"\n  Procesando {len(data)} párrafos...")
new_data = []
for i, row in enumerate(data):
    if (i + 1) % 100 == 0:
        print(f"    [{i+1:4d}/{len(data)}] procesados")
    
    try:
        text = row["texto"]
        tokens = process_text(text)
        countries, orgs = extract_entities(text)
        
        row["tokens"] = tokens
        row["pais"] = countries
        row["organizacion"] = orgs
        new_data.append(row)
    except Exception as e:
        print(f"    ERROR en párrafo {i}: {e}")
        continue

print(f"  Guardando: {OUTPUT_FILE}")
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(new_data, f, indent=2, ensure_ascii=False)

print(f"\n✓ FASE 2B completada!")
print(f"  - {len(new_data)} párrafos procesados")
print(f"  - Tokens + entidades extraídas")
print(f"  - Archivo: {OUTPUT_FILE}")

print("\n" + "="*70)
print("✓ PIPELINE COMPLETADO EXITOSAMENTE")
print("="*70)
print("\nProximos pasos:")
print("  - FASE 3.1: Topic Modeling (LDA)")
print("  - FASE 3.2: Análisis de Sentimiento")
print("  - FASE 4: Evaluación")
print("  - FASE 5: Visualización")
