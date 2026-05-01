"""
FASE 4: EVALUACIÓN DE MODELOS

Script: 09_evaluation_metrics.py
Descripción: Evalúa la calidad de los modelos LDA y análisis de sentimiento
Entrada: 
  - data/processed/lda_results.json
  - data/processed/dataset_with_sentiment.json
Salida:
  - data/processed/topics_evaluation.json
  - data/processed/sentiment_evaluation.json

Autor: Alexis Frank Jimenez
Fecha: 29/04/2026
"""

import json
import os
import re
from collections import Counter, defaultdict
from datetime import datetime
import statistics

def load_json(filepath):
    """Cargar archivo JSON con encoding UTF-8"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            return json.load(f)

def save_json(data, filepath):
    """Guardar JSON con identación"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def _parse_lda_terms(terms_str):
    """
    Parsear string de términos LDA en formato: "0.030*\"word\" + 0.020*\"word2\""
    Retorna lista de (word, weight) ordenada por weight descendente
    """
    pattern = r'([\d.]+)\*"([^"]+)"'
    matches = re.findall(pattern, terms_str)
    
    weighted = [(word, float(weight)) for weight, word in matches]
    return sorted(weighted, key=lambda x: x[1], reverse=True)

def _interpret_topic(words):
    """Interpretar el tema basado en palabras clave"""
    words_lower = [w.lower() for w in words[:10]]
    
    # Mapeos de tema
    themes = {
        'GEOGRAFÍA': ['united', 'states', 'china', 'germany', 'japan', 'india', 'country', 'region'],
        'TEMPORALIDAD': ['2020', '2019', '2021', 'year', 'pandemic', 'covid', 'months'],
        'TECNOLOGÍA': ['automated', 'technology', 'digital', 'software', 'automation'],
        'POLÍTICA MONETARIA': ['interest', 'rates', 'central', 'bank', 'monetary', 'policy'],
        'EMPLEO': ['labor', 'employment', 'workers', 'wages', 'jobs', 'unemployment'],
        'COMERCIO': ['trade', 'export', 'import', 'commerce', 'tariffs'],
        'INFLACIÓN': ['inflation', 'prices', 'commodities', 'costs'],
        'CRECIMIENTO': ['growth', 'economic', 'development', 'expansion', 'gdp'],
        'RIESGO': ['risk', 'crisis', 'volatile', 'uncertainty', 'instability'],
        'INVERSIÓN': ['investment', 'capital', 'finance', 'equity', 'returns']
    }
    
    theme_scores = defaultdict(int)
    for word in words_lower:
        for theme, keywords in themes.items():
            if word in keywords:
                theme_scores[theme] += 1
    
    if theme_scores:
        return max(theme_scores, key=theme_scores.get)
    return 'MIXTO'

def _calculate_relevance(words, theme):
    """Calcular score de relevancia (0-1)"""
    economic_words = {'growth', 'inflation', 'gdp', 'trade', 'investment', 'employment',
                     'crisis', 'markets', 'policy', 'economy', 'economic', 'financial'}
    
    relevant_count = sum(1 for w in words[:5] if w.lower() in economic_words)
    return min(1.0, relevant_count / 3.0)

def evaluate_topics(lda_results):
    """
    FASE 4.2: Evaluar tópicos extraídos
    """
    print("\n" + "="*60)
    print("FASE 4.2: EVALUACIÓN DE TÓPICOS")
    print("="*60)
    
    topics = lda_results.get('topics', [])
    coherence = lda_results.get('coherence_score', 0)
    
    print(f"\n📊 Modelo LDA seleccionado:")
    print(f"  - Número de tópicos: {len(topics)}")
    print(f"  - Coherencia C_v: {coherence:.4f}")
    print(f"  - Validación: {'✅ PASS' if coherence >= 0.40 else '❌ FAIL'}")
    
    topics_eval = {
        'total_topics': len(topics),
        'coherence_score': coherence,
        'coherence_valid': coherence >= 0.40,
        'topics': []
    }
    
    print(f"\n📋 Análisis detallado de tópicos:\n")
    
    for idx, topic in enumerate(topics, 1):
        topic_id = topic.get('id', idx)
        terms_str = topic.get('terms', '')
        
        weighted_words = _parse_lda_terms(terms_str)
        words = [w for w, _ in weighted_words]
        top_5_words = weighted_words[:5]
        
        theme = _interpret_topic(words)
        
        topic_eval = {
            'topic_id': topic_id,
            'top_words': [w for w, _ in top_5_words],
            'word_weights': [round(w, 4) for _, w in top_5_words],
            'total_words': len(words),
            'interpretation': theme,
            'relevance_score': _calculate_relevance(words, theme)
        }
        
        topics_eval['topics'].append(topic_eval)
        
        top_words_str = ", ".join([f"{w}({wt:.2f})" for w, wt in top_5_words[:3]])
        print(f"  Tópico {topic_id}: {theme}")
        print(f"    Top words: {top_words_str}")
        print(f"    Relevancia: {topic_eval['relevance_score']:.2f}")
        print()
    
    return topics_eval

def evaluate_sentiment(dataset_with_sentiment):
    """
    FASE 4.3: Evaluar análisis de sentimiento
    """
    print("\n" + "="*60)
    print("FASE 4.3: EVALUACIÓN DE SENTIMIENTO")
    print("="*60)
    
    if isinstance(dataset_with_sentiment, list):
        paragraphs = dataset_with_sentiment
    else:
        paragraphs = dataset_with_sentiment.get('paragraphs', [])
    
    sentiment_counter = Counter()
    compound_scores = []
    sentiment_stats = defaultdict(list)
    
    print(f"\n📊 Procesando {len(paragraphs)} párrafos...\n")
    
    for para in paragraphs:
        sentiment = para.get('sentiment', {})
        
        if isinstance(sentiment, dict):
            label = sentiment.get('label', 'neutral')
            compound = sentiment.get('compound', 0.0)
        else:
            label = str(sentiment).lower()
            compound = 0.5 if label == 'positive' else (-0.5 if label == 'negative' else 0)
        
        sentiment_counter[label] += 1
        compound_scores.append(compound)
        sentiment_stats[label].append(compound)
    
    total = len(paragraphs)
    
    print(f"📈 Distribución de sentimientos:\n")
    sentiment_eval = {
        'total_paragraphs': total,
        'sentiment_distribution': {},
        'compound_statistics': {},
        'validation': {}
    }
    
    for label in ['positive', 'neutral', 'negative']:
        count = sentiment_counter.get(label, 0)
        percentage = (count / total * 100) if total > 0 else 0
        scores = sentiment_stats[label]
        
        sentiment_eval['sentiment_distribution'][label] = {
            'count': count,
            'percentage': round(percentage, 2),
            'compound_avg': round(statistics.mean(scores), 4) if scores else 0,
            'compound_std': round(statistics.stdev(scores), 4) if len(scores) > 1 else 0
        }
        
        print(f"  {label.upper():10} {count:5} párrafos ({percentage:5.1f}%)")
        if scores:
            print(f"    - Compound avg: {statistics.mean(scores):.4f}")
            if len(scores) > 1:
                print(f"    - Compound std: {statistics.stdev(scores):.4f}")
        print()
    
    compound_avg = statistics.mean(compound_scores) if compound_scores else 0
    compound_std = statistics.stdev(compound_scores) if len(compound_scores) > 1 else 0
    
    sentiment_eval['compound_statistics'] = {
        'mean': round(compound_avg, 4),
        'std_dev': round(compound_std, 4),
        'min': round(min(compound_scores), 4) if compound_scores else 0,
        'max': round(max(compound_scores), 4) if compound_scores else 0,
        'median': round(statistics.median(compound_scores), 4) if compound_scores else 0
    }
    
    print(f"📊 Estadísticas generales:")
    print(f"  - Compound promedio: {compound_avg:.4f} (ligeramente {'positivo' if compound_avg > 0 else 'negativo'})")
    print(f"  - Desviación std: {compound_std:.4f}")
    if compound_scores:
        print(f"  - Rango: [{min(compound_scores):.4f}, {max(compound_scores):.4f}]")
    
    sentiment_eval['validation'] = {
        'neutral_dominance': sentiment_counter['neutral'] / total > 0.5 if total > 0 else False,
        'reasonable_distribution': all(0 < sentiment_counter.get(s, 0) / total < 0.8 for s in ['positive', 'neutral', 'negative']) if total > 0 else False
    }
    
    return sentiment_eval

def main():
    """Ejecutar evaluación completa"""
    
    print("\n" + "█"*60)
    print("█ FASE 4: EVALUACIÓN DE MODELOS")
    print("█"*60)
    print(f"\nFecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Rutas
    lda_path = 'data/processed/lda_results.json'
    sentiment_path = 'data/processed/dataset_with_sentiment.json'
    
    # Validar archivos
    if not os.path.exists(lda_path):
        print(f"❌ Error: No se encontró {lda_path}")
        return
    
    if not os.path.exists(sentiment_path):
        print(f"❌ Error: No se encontró {sentiment_path}")
        return
    
    # Cargar datos
    print("\n📂 Cargando archivos...")
    lda_results = load_json(lda_path)
    dataset_sentiment = load_json(sentiment_path)
    print("   ✅ Datos cargados\n")
    
    # Ejecutar evaluaciones
    topics_eval = evaluate_topics(lda_results)
    sentiment_eval = evaluate_sentiment(dataset_sentiment)
    
    # Guardar resultados
    print("\n💾 Guardando resultados...\n")
    
    save_json(topics_eval, 'data/processed/topics_evaluation.json')
    print("   ✅ Guardado: data/processed/topics_evaluation.json")
    
    save_json(sentiment_eval, 'data/processed/sentiment_evaluation.json')
    print("   ✅ Guardado: data/processed/sentiment_evaluation.json")
    
    # Resumen final
    print("\n" + "="*60)
    print("RESUMEN EJECUTIVO - FASE 4")
    print("="*60)
    
    print(f"\n✅ Evaluación de tópicos: {topics_eval['coherence_score']:.4f} (válido: {topics_eval['coherence_valid']})")
    print(f"✅ Análisis de sentimiento: {len(sentiment_eval['sentiment_distribution'])} categorías")
    print(f"✅ Total párrafos analizados: {sentiment_eval['total_paragraphs']}")
    
    print("\n" + "="*60)
    print("✅ FASE 4 COMPLETADA")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()
