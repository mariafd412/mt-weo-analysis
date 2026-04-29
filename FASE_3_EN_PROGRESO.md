# FASE 3: Minería de Texto (CORE) - COMPLETADA ✅

**Estado:** COMPLETADO  
**Fecha inicio:** 28 de Abril, 2026  
**Fecha finalización:** 29 de Abril, 2026

---

## Descripción

Esta fase implementa los algoritmos core de minería de texto:

### FASE 3.1: Topic Modeling (LDA) ⏳
Identificar temas principales en los informes WEO usando Latent Dirichlet Allocation.

**Script:** `src/06_lda_topic_modeling.py`

**Proceso:**
1. Cargar dataset (15,519 párrafos)
2. Tokenización de textos
3. Crear diccionario y corpus
4. Entrenar modelos LDA con 5, 7, 10, 15 tópicos
5. Seleccionar modelo óptimo por coherencia C_v
6. Guardar tópicos e interpretarlos

**Salida esperada:**
- `data/processed/lda_results.json` - Tópicos y coherencia
- `data/processed/lda_model` - Modelo entrenado
- `data/processed/dictionary.dict` - Diccionario gensim
- `data/processed/corpus.mm` - Corpus serializado

**Tiempo estimado:** 3-5 minutos

---

### FASE 3.2: Análisis de Sentimiento (VADER) ⏳
Clasificar párrafos como positivo/neutro/negativo.

**Script:** `src/07_sentiment_analysis.py`

**Proceso:**
1. Cargar dataset (15,519 párrafos)
2. Aplicar VADER sentiment analyzer
3. Clasificar sentimiento (pos/neg/neutral)
4. Calcular compound score
5. Agrupar por documento
6. Analizar por país si existen entidades NER

**Salida esperada:**
- `data/processed/dataset_with_sentiment.json` - Dataset + sentimientos
- `data/processed/sentiment_summary.json` - Resumen estadístico

**Tiempo estimado:** 30-60 segundos

---

### FASE 3.3: Asociación País + Sentimiento ⏳
Análisis agregado de sentimientos por país/región.

**Script:** `src/08_country_sentiment_analysis.py`

**Proceso:**
1. Cargar dataset con sentimientos
2. Agrupar párrafos por país
3. Calcular estadísticas por país
4. Ranking de países por sentimiento
5. Matriz país x sentimiento

**Salida esperada:**
- `data/processed/country_sentiment_analysis.json` - Análisis agregado

**Tiempo estimado:** 30 segundos

---

## Tópicos Esperados en WEO

Basado en el contexto económico (2015-2026):

1. **Crecimiento Global** - Growth, economic activity, investment
2. **Inflación y Precios** - Inflation, commodity prices, oil
3. **Política Monetaria** - Central banks, interest rates, monetary policy
4. **Emergentes** - Emerging markets, China, developing economies
5. **Empleo y Mercados de Trabajo** - Employment, labor markets
6. **Deuda y Crisis** - Debt, financial crisis, sovereign
7. **Comercio Internacional** - Trade, exports, imports
8. **Sectores Específicos** - Energy, agriculture, manufacturing
9. **Riesgos Geopolíticos** - Tensions, geopolitical
10. **Fragmentación Económica** - Fragmentation, decoupling, regional

---

## Métricas Clave

### Topic Modeling
- **Coherencia C_v**: Mide coherencia temática (0-1, mejor ≈ 0.6)
- **Perplexity**: Perplejidad del modelo (menor = mejor)
- **Número óptimo de tópicos**: Determinado por coherencia máxima

### Análisis de Sentimiento
- **Compound Score**: -1 (muy negativo) a +1 (muy positivo)
- **Distribuciónpositivo/neutral/negativo**: Porcentaje de cada categoría
- **Sentimiento promedio**: Media de compound scores

---

## Archivos Generados

```
data/processed/
├── lda_results.json                      # Tópicos e info
├── lda_model                             # Modelo LDA serializado
├── dictionary.dict                       # Diccionario gensim
├── corpus.mm                             # Corpus serializado
├── dataset_with_sentiment.json           # Dataset + sentimientos
├── sentiment_summary.json                # Resumen sentimientos
└── country_sentiment_analysis.json       # Análisis país-sentimiento
```

---

## Próximos Pasos

Después de completar FASE 3:

1. **FASE 4**: Evaluación
   - Validación de coherencia de tópicos
   - Evaluación manual de sentimientos
   - Métricas de desempeño

2. **FASE 5**: Visualización
   - Gráficos de distribución de tópicos
   - Mapas de sentimiento por país
   - Evolución temporal de sentimientos
   - Wordclouds por tópico

3. **FASE 6**: Dashboard (opcional)
   - Streamlit/Dash
   - Interfaz interactiva

4. **FASE 7**: Documentación final
   - Memoria completa del trabajo
   - Justificación metodológica
   - Conclusiones y hallazgos

---

**Estado de ejecución:** COMPLETADO  
**Última actualización:** 29/04/2026 - Fase 3 finalizada, iniciando Fase 4
