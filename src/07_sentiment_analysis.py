#!/usr/bin/env python3
"""
FASE 3.2: Análisis de Sentimiento usando VADER
Clasifica paragrafos como positivo, neutro, negativo
"""
import json
import sys
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import numpy as np
from collections import Counter

print("="*70)
print("FASE 3.2: ANÁLISIS DE SENTIMIENTO (VADER)")
print("="*70)

# Descargar recursos VADER
print("\n1. Descargando recursos VADER...")
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon', quiet=True)

# Inicializar VADER
print("   Inicializando VADER...")
sia = SentimentIntensityAnalyzer()
print("   ✓ VADER listo")

# Cargar dataset
print("\n2. Cargando dataset...")
INPUT_FILE = "data/processed/dataset.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"   ✓ Cargados {len(data)} párrafos")

# Analizar sentimiento
print("\n3. Analizando sentimiento (esto puede tomar 30-60 segundos)...")

sentiments = []
for i, item in enumerate(data):
    if (i + 1) % 200 == 0:
        print(f"   [{i+1}/{len(data)}]...")
    
    text = item["texto"]
    
    # Análisis VADER
    scores = sia.polarity_scores(text)
    
    # Clasificar
    compound = scores['compound']
    if compound >= 0.05:
        sentiment = 'positive'
    elif compound <= -0.05:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'
    
    item["sentiment"] = {
        "label": sentiment,
        "scores": scores,
        "compound": compound
    }
    
    # Extraer país si existe
    country = item.get("pais", [None])[0] if item.get("pais") else None
    
    sentiments.append({
        "sentimento": sentiment,
        "compound": compound,
        "doc": item["doc"],
        "pais": country,
        "parrafo_id": item["parrafo_id"]
    })

print(f"   ✓ {len(sentiments)} párrafos analizados")

# Estadísticas generales
print("\n4. Estadísticas de sentimiento:")
print("-" * 70)

sentiment_counts = Counter([s["sentimento"] for s in sentiments])
print(f"\n   Distribución de sentimientos:")
for sentiment, count in sentiment_counts.most_common():
    percentage = (count / len(sentiments)) * 100
    print(f"     {sentiment:10s}: {count:4d} ({percentage:5.1f}%)")

avg_compound = np.mean([s["compound"] for s in sentiments])
print(f"\n   Sentimiento promedio (compound): {avg_compound:.4f}")

# Sentimiento por país (si existen)
print(f"\n   Top 10 países con mejor sentimiento:")
countries_sentiment = {}
for s in sentiments:
    if s["pais"]:
        if s["pais"] not in countries_sentiment:
            countries_sentiment[s["pais"]] = []
        countries_sentiment[s["pais"]].append(s["compound"])

if countries_sentiment:
    for country, scores in sorted(
        countries_sentiment.items(),
        key=lambda x: np.mean(x[1]),
        reverse=True
    )[:10]:
        avg = np.mean(scores)
        print(f"     {country:20s}: {avg:7.4f} (n={len(scores)})")
else:
    print("     (Sin información de países en los datos)")

# Guardar dataset con sentimientos
print("\n5. Guardando resultados...")

OUTPUT_FILE = "data/processed/dataset_with_sentiment.json"
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"   ✓ Dataset con sentimientos: {OUTPUT_FILE}")

# Guardar resumen de sentimientos
SUMMARY_FILE = "data/processed/sentiment_summary.json"
summary = {
    "total_documents": len(sentiments),
    "sentiment_distribution": dict(sentiment_counts),
    "average_compound_score": float(avg_compound),
    "sentiment_by_country": {
        country: {
            "average_compound": float(np.mean(scores)),
            "count": len(scores),
            "positive": sum(1 for s in scores if s >= 0.05),
            "negative": sum(1 for s in scores if s <= -0.05),
            "neutral": sum(1 for s in scores if -0.05 < s < 0.05)
        }
        for country, scores in countries_sentiment.items()
    }
}

with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)

print(f"   ✓ Resumen de sentimientos: {SUMMARY_FILE}")

print("\n" + "="*70)
print("✓ FASE 3.2 COMPLETADA")
print("="*70)
print(f"\nResultados:")
print(f"  - Párrafos analizados: {len(sentiments)}")
print(f"  - Distribución: {dict(sentiment_counts)}")
print(f"  - Sentimiento promedio: {avg_compound:.4f}")
print(f"  - Archivos: {OUTPUT_FILE}, {SUMMARY_FILE}")
print(f"\nPróximo paso: FASE 3.3 - Asociación país + sentimiento")
