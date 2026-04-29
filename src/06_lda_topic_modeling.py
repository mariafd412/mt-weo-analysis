#!/usr/bin/env python3
"""
FASE 3.1: Topic Modeling usando LDA (Latent Dirichlet Allocation)
Identifica tópicos principales en los informes WEO
"""
import json
import numpy as np
import matplotlib.pyplot as plt
from gensim import corpora, models
from gensim.models import CoherenceModel
import re

print("="*70)
print("FASE 3.1: TOPIC MODELING (LDA)")
print("="*70)

# Cargar dataset
print("\n1. Cargando dataset...")
INPUT_FILE = "data/processed/dataset.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"   ✓ Cargados {len(data)} párrafos")

# Preparar textos para LDA
print("\n2. Preparando textos (tokenización mínima)...")
texts = []
for i, item in enumerate(data):
    # Obtener tokens si existen, si no tokenizar el texto
    if "tokens" in item and item["tokens"]:
        tokens = item["tokens"]
    else:
        # Tokenización simple
        text = item["texto"].lower()
        text = re.sub(r"[^\w\s]", "", text)
        tokens = [w for w in text.split() if len(w) > 3]
    
    if tokens:
        texts.append(tokens)

print(f"   ✓ {len(texts)} textos tokenizados")
print(f"   ✓ Promedio de tokens por texto: {np.mean([len(t) for t in texts]):.0f}")

# Crear diccionario y corpus
print("\n3. Creando diccionario y corpus...")
dictionary = corpora.Dictionary(texts)
print(f"   ✓ Diccionario: {len(dictionary)} palabras únicas")

corpus = [dictionary.doc2bow(text) for text in texts]
print(f"   ✓ Corpus: {len(corpus)} documentos")

# Entrenar modelos LDA con diferentes números de tópicos para encontrar el óptimo
print("\n4. Entrenando modelos LDA (esto puede tomar 1-2 minutos)...")

num_topics_range = [5, 7, 10, 15]
coherence_scores = []
lda_models = {}

for num_topics in num_topics_range:
    print(f"\n   Entrenando LDA con {num_topics} tópicos...")
    lda = models.LdaModel(
        corpus=corpus,
        id2word=dictionary,
        num_topics=num_topics,
        random_state=42,
        passes=10,
        per_word_topics=True,
        minimum_probability=0.0,
        alpha='auto',
        eta='auto'
    )
    
    # Calcular coherencia
    coherence_model = CoherenceModel(model=lda, texts=texts, dictionary=dictionary, coherence='c_v')
    coherence_score = coherence_model.get_coherence()
    coherence_scores.append(coherence_score)
    lda_models[num_topics] = (lda, coherence_score)
    
    print(f"   ✓ Coherencia C_v: {coherence_score:.4f}")

# Seleccionar el mejor modelo
best_num_topics = num_topics_range[np.argmax(coherence_scores)]
best_lda = lda_models[best_num_topics][0]

print(f"\n5. Modelo seleccionado: {best_num_topics} tópicos (Coherencia: {max(coherence_scores):.4f})")

# Mostrar tópicos
print("\n6. Tópicos identificados:")
print("-" * 70)

for idx, topic in best_lda.print_topics(-1):
    print(f"\n   Tópico {idx + 1}:")
    print(f"   {topic}")

# Guardar resultados
print("\n7. Guardando resultados...")

results = {
    "num_topics": best_num_topics,
    "coherence_score": max(coherence_scores),
    "coherence_scores_by_topics": {str(k): v for k, v in zip(num_topics_range, coherence_scores)},
    "topics": []
}

for idx, topic in best_lda.print_topics(-1):
    results["topics"].append({
        "id": int(idx),
        "terms": topic
    })

OUTPUT_FILE = "data/processed/lda_results.json"
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"   ✓ Guardado en: {OUTPUT_FILE}")

# Guardar modelo
MODEL_FILE = "data/processed/lda_model"
best_lda.save(MODEL_FILE)
dictionary.save("data/processed/dictionary.dict")
corpora.MmCorpus.serialize("data/processed/corpus.mm", corpus)

print(f"   ✓ Modelo guardado en: {MODEL_FILE}")

print("\n" + "="*70)
print("✓ FASE 3.1 COMPLETADA")
print("="*70)
print(f"\nResultados:")
print(f"  - Tópicos identificados: {best_num_topics}")
print(f"  - Coherencia (C_v): {max(coherence_scores):.4f}")
print(f"  - Archivo: {OUTPUT_FILE}")
print(f"\nPróximo paso: FASE 3.2 - Análisis de Sentimiento (VADER)")
