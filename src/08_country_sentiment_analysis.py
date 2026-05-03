#!/usr/bin/env python3
"""
FASE 3.3: Asociación País + Sentimiento
Análisis agregado de sentimientos por país/región
"""
import json
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

print("="*70)
print("FASE 3.3: ASOCIACIÓN PAÍS + SENTIMIENTO")
print("="*70)

# Cargar dataset con sentimientos
print("\n1. Cargando dataset con sentimientos...")
INPUT_FILE = "data/processed/dataset_with_sentiment.json"

try:
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"   ✓ Cargados {len(data)} párrafos con sentimientos")
except FileNotFoundError:
    print(f"   ✗ Archivo no encontrado: {INPUT_FILE}")
    print("   (Ejecutar FASE 3.2 primero)")
    exit(1)

# Agrupar por país
print("\n2. Agrupando párrafos por país...")
country_data = defaultdict(lambda: {
    "paragraphs": [],
    "sentiments": [],
    "compound_scores": [],
    "positive_count": 0,
    "negative_count": 0,
    "neutral_count": 0
})

for item in data:
    if not isinstance(item, dict):
        continue

    paises = item.get("pais", [])

    # 🔥 NORMALIZACIÓN ROBUSTA
    if not paises:
        continue

    if isinstance(paises, str):
        paises = [paises]

    paises = [
        p.strip()
        for p in paises
        if isinstance(p, str) and len(p.strip()) > 2
    ]                                       
    sentiment = item.get("sentiment", {})
    compound = sentiment.get("compound", 0)
    label = sentiment.get("label", "neutral")

    if not paises:
        continue

    for country in paises:

        # 🔴 limpieza básica obligatoria
        if not isinstance(country, str):
            continue

        country = country.strip()

        if len(country) < 3:
            continue

        if country.lower() in {"sia", "key interest", "financial derivatives"}:
            continue

        country_data[country]["paragraphs"].append(item["texto"][:100])
        country_data[country]["sentiments"].append(label)
        country_data[country]["compound_scores"].append(compound)

        if label == "positive":
            country_data[country]["positive_count"] += 1
        elif label == "negative":
            country_data[country]["negative_count"] += 1
        else:
            country_data[country]["neutral_count"] += 1

print(f"   ✓ {len(country_data)} países identificados")

# Análisis por país
print("\n3. Analizando sentimiento por país:")
print("-" * 70)

country_analysis = {}
for country in sorted(country_data.keys()):
    data_country = country_data[country]
    total = len(data_country["sentiments"])
    
    if total > 0:
        avg_compound = np.mean(data_country["compound_scores"])
        pos_pct = (data_country["positive_count"] / total) * 100
        neg_pct = (data_country["negative_count"] / total) * 100
        neu_pct = (data_country["neutral_count"] / total) * 100
        
        country_analysis[country] = {
            "total_mentions": total,
            "average_compound": avg_compound,
            "positive_percent": pos_pct,
            "negative_percent": neg_pct,
            "neutral_percent": neu_pct,
            "positive_count": data_country["positive_count"],
            "negative_count": data_country["negative_count"],
            "neutral_count": data_country["neutral_count"]
        }
        
        print(f"\n   {country}:")
        print(f"     Menciones: {total:3d} | Sentimiento avg: {avg_compound:6.3f}")
        print(f"     Pos: {pos_pct:5.1f}% | Neg: {neg_pct:5.1f}% | Neu: {neu_pct:5.1f}%")

# Top 10 países con sentimiento más positivo
print("\n4. Top 10 países con sentimiento MÁS POSITIVO:")
print("-" * 70)
top_positive = sorted(country_analysis.items(), key=lambda x: x[1]["average_compound"], reverse=True)[:10]
for i, (country, analysis) in enumerate(top_positive, 1):
    print(f"   {i:2d}. {country:25s} | Score: {analysis['average_compound']:7.4f}")

# Top 10 países con sentimiento más negativo
print("\n5. Top 10 países con sentimiento MÁS NEGATIVO:")
print("-" * 70)
top_negative = sorted(country_analysis.items(), key=lambda x: x[1]["average_compound"])[:10]
for i, (country, analysis) in enumerate(top_negative, 1):
    print(f"   {i:2d}. {country:25s} | Score: {analysis['average_compound']:7.4f}")

# Guardar resultados
print("\n6. Guardando resultados...")

OUTPUT_FILE = "data/processed/country_sentiment_analysis.json"
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(country_analysis, f, indent=2, ensure_ascii=False)

print(f"   ✓ Análisis país-sentimiento: {OUTPUT_FILE}")

# Crear visualización simple (texto)
print("\n7. Visualización - Ranking de Sentimientos:")
print("-" * 70)
print("\n   Matriz País x Sentimiento (Conteos):\n")
print(f"   {'País':<25} {'Positivo':>8} {'Neutral':>8} {'Negativo':>8} {'Total':>8} {'Score':>8}")
print(f"   {'-'*25} {'-'*8} {'-'*8} {'-'*8} {'-'*8} {'-'*8}")

for country in sorted(country_analysis.keys(), key=lambda x: country_analysis[x]["average_compound"], reverse=True):
    analysis = country_analysis[country]
    print(f"   {country:<25} {analysis['positive_count']:>8} {analysis['neutral_count']:>8} {analysis['negative_count']:>8} {analysis['total_mentions']:>8} {analysis['average_compound']:>8.4f}")

print("\n" + "="*70)
print("✓ FASE 3.3 COMPLETADA")
print("="*70)
print(f"\nResultados:")
print(f"  - Países analizados: {len(country_analysis)}")
print(f"  - Archivo: {OUTPUT_FILE}")
print(f"\nInterpretación:")
print(f"  - Score > 0.05: Sentimiento POSITIVO")
print(f"  - Score ≈ 0.00: Sentimiento NEUTRAL")
print(f"  - Score < -0.05: Sentimiento NEGATIVO")
print(f"\nPróximo paso: FASE 4 - Evaluación de modelos")
