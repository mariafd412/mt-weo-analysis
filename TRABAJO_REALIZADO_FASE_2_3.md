# FASE 2 & 3: Mejoras en Procesamiento NLP - Documentación de Trabajo

**Autor:** Alexis Frank Jimenez  
**Fecha:** 28-29 de Abril, 2026  
**Estado:** ✅ FASE 3 COMPLETADA

---

## Resumen de Cambios

Se ha mejorado significativamente el pipeline de procesamiento de texto para la minería de texto del informe WEO del FMI.

### ✅ Completado

#### Fase 0: Setup Inicial
- ✓ Repositorio git configurado
- ✓ Entorno virtual (venv) creado
- ✓ Dependencias instaladas (requirements.txt)

#### Fase 1: Extracción de PDFs
- ✓ Extracción de 46 PDFs → 45 archivos .txt limpios
- ✓ PDFs procesados: enero, abril, julio, octubre (2015-2026)
- ✓ Datos almacenados en `data/processed/`

#### Fase 2: Procesamiento NLP (EN PROGRESO)
- ✓ Limpieza de texto (regex para saltos de línea, espacios, caracteres raros)
- ✓ División en párrafos: 1000+ párrafos extraídos
- ✓ Dataset estructurado: `data/processed/dataset.json` (18.3 MB)
- 🟡 Procesamiento NLP: Instalación de spacy + NLTK finalizada
- 🟡 Extracción de tokens, lematización y entidades NER: EN PROGRESO

---

## Cambios de Código

### 1. Mejorado: `src/04_nlp_processing.py`
**Cambios:**
- Añadido manejo robusto de errores
- Instalación automática de dependencias (spacy, NLTK)
- Descarga automática de modelos
- Protección de palabras clave del dominio: `{growth, inflation, crisis, deficit}`
- Extracción de tokens + entidades NER (países y organizaciones)
- Logging de progreso (cada 100 párrafos)

**Entrada:** `data/processed/dataset.json`  
**Salida:** `data/processed/dataset_nlp.json` (en progreso)

**Palabras clave protegidas:**
```python
keep_words = {"growth", "inflation", "crisis", "deficit"}
stop_words = stop_words - keep_words
```

### 2. Nuevos Scripts de Support

#### `install_and_process_nlp.py`
- Instalación automática de dependencias
- Descarga de modelos de spacy
- Ejecución de procesamiento NLP

#### `nlp_minimal.py`
- Versión simplificada usando solo NLTK
- Sin dependencia de spacy (alternativa más ligera)

#### `run_full_pipeline.py`
- Ejecuta el pipeline completo (Fase 1 y 2)
- Verificación automática de dependencias

#### `test_deps.py`
- Script de prueba para verificar que todas las dependencias estén disponibles

### 3. Configuración Git

#### `.gitignore`
Añadido para evitar commitear:
- Carpetas virtuales (`venv/`, `.venv/`)
- Archivos Python compilados (`__pycache__/`, `*.pyc`)
- IDE files (`.vscode/`, `.idea/`)
- Archivos temporales

---

## Estadísticas del Procesamiento

| Métrica | Valor |
|---------|-------|
| PDFs Procesados | 46 |
| TXT Generados | 45 |
| Párrafos Extraídos | 1000+ |
| Dataset JSON | 18.3 MB |
| Tokens por párrafo (promedio) | 50-100 |
| Entidades NER (esperadas) | Países, Organizaciones |

---

## Dependencias Instaladas

```
spacy==3.8.0
nltk==3.9.4
scikit-learn==1.8.0
gensim==4.4.0
matplotlib==3.10.9
seaborn==0.14.0
transformers==4.40.0
```

---

## ✅ FASE 3: COMPLETADA (29 Abril 2026)

### 3.1 Topic Modeling (LDA) ✅
- ✓ Entrenamiento de 4 modelos LDA (5, 7, 10, 15 tópicos)
- ✓ Modelo óptimo: **10 tópicos** (coherencia C_v: 0.4242)
- ✓ Extracción de palabras clave por tópico
- ✓ Tópicos identificados:
  - Tópico 0: GEOGRAFÍA (United States, productivity)
  - Tópico 1: TEMPORALIDAD (2020, 2019, pandemia)
  - Tópico 2: TECNOLOGÍA (Automatización, costo de vida)
  - Tópico 3: CRECIMIENTO (International data)
  - Tópico 4: CRECIMIENTO (External conditions)
  - Tópico 5: POLÍTICA MONETARIA (Interest rates)
  - Tópico 6: EMPLEO (Labor shares, ingresos)
  - Tópico 7: DISPARIDADES (Disparities, results)
  - Tópico 8: MIXTO (Welfare, social issues)
  - Tópico 9: CRECIMIENTO (Economic divergence, world outlook)
- ✓ Archivo: `data/processed/lda_results.json`

### 3.2 Análisis de Sentimiento ✅
- ✓ Implementación VADER completada
- ✓ Clasificación de 15,519 párrafos
- ✓ Distribución de sentimientos:
  - **Positivo:** 4,546 párrafos (29.3%)
  - **Neutral:** 9,073 párrafos (58.5%)
  - **Negativo:** 1,900 párrafos (12.2%)
- ✓ Compound score promedio: 0.0680 (ligeramente positivo)
- ✓ Rango compound: [-0.8720, 1.0000]
- ✓ Archivos: 
  - `data/processed/dataset_with_sentiment.json` (21 MB)
  - `data/processed/sentiment_summary.json`

### 3.3 Asociación País + Sentimiento ✅
- ✓ Script creado y ejecutado
- ⚠ Nota: 0 países identificados (requiere ejecutar NER previamente)
- ✓ Archivo: `data/processed/country_sentiment_analysis.json`

---

## ✅ FASE 4: EVALUACIÓN DE MODELOS - COMPLETADA (29 Abril 2026)

### 4.1 Validación de Coherencia LDA ✅
- ✓ Coherencia C_v del modelo óptimo: **0.4242**
- ✓ Umbral mínimo: 0.40
- ✓ **Estado:** ✅ PASS

### 4.2 Evaluación de Tópicos ✅
- ✓ Análisis de interpretación temática de 10 tópicos
- ✓ Cálculo de relevancia económica por tópico:
  - Tópicos con relevancia alta (>0.30): Tópicos 1, 3, 5, 9
  - Tópicos con relevancia media: Tópicos 2, 4, 6
  - Tópicos con baja relevancia: Tópicos 0, 7, 8
- ✓ Identificación de temas dominantes (Geografía, Temporalidad, Tecnología, etc.)
- ✓ Archivo: `data/processed/topics_evaluation.json`

### 4.3 Análisis de Sentimiento ✅
- ✓ Evaluación estadística de compound scores por categoría:
  - Positivo: promedio 0.3817 (±0.1601)
  - Neutral: promedio 0.0001 (±0.0031)
  - Negativo: promedio -0.3577 (±0.1696)
- ✓ Validación: Distribución neutral dominante (58.5%), razonable
- ✓ Archivo: `data/processed/sentiment_evaluation.json`

### 4.4 Scripts Creados
- ✓ `src/09_evaluation_metrics.py` - Script de evaluación (315 líneas)
- ✓ `src/10_visualization.py` - Script de visualización (420 líneas)

---

## 📊 Próximos Pasos (Fase 5+)
- [ ] Muestreo manual de sentimientos (10-20 párrafos)
- [ ] Matriz confusión para VADER

### 5. Extracción NER (Necesario) ⏳
- [ ] Ejecutar `src/04_nlp_processing.py` para extraer países/organizaciones
- [ ] Generar `dataset_nlp.json` con entidades etiquetadas
- [ ] Repetir país-sentimiento con entidades extraídas

### 6. Visualización ⏳
- [ ] Wordclouds por tópico
- [ ] Gráficos de distribución de sentimiento
- [ ] Mapa de países por sentimiento
- [ ] Evolución temporal de tópicos

---

## Notas Técnicas

### Problemas Encontrados y Soluciones

1. **Rutas WSL/Windows incompatibles**
   - Solución: Usar WSL bash directamente para ejecutar scripts

2. **Conflicto de dependencias venv**
   - Solución: Usar venv existente, eliminar `.venv` duplicada

3. **Spacy model download delays**
   - Solución: Ejecutar con `-q` (quiet mode) para evitar timeouts

### Próximas Mejoras
- Paralelizar procesamiento NLP para datasets grandes
- Caché de embeddings word2vec
- Integración con base de datos (SQLite/PostgreSQL)

---

## Cómo Ejecutar

### Opción 1: Pipeline Completo
```bash
source venv/bin/activate
python src/04_nlp_processing.py
```

### Opción 2: Con Auto-instalación de Dependencias
```bash
python install_and_process_nlp.py
```

### Opción 3: Versión Mínima (NLTK only)
```bash
python nlp_minimal.py
```

---

## Archivos Modificados/Creados

```
- ✓ src/06_lda_topic_modeling.py          (NUEVO - FASE 3.1)
- ✓ src/07_sentiment_analysis.py         (NUEVO - FASE 3.2)
- ✓ src/08_country_sentiment_analysis.py (NUEVO - FASE 3.3)
- ✓ data/processed/lda_results.json      (NUEVO)
- ✓ data/processed/dataset_with_sentiment.json (NUEVO - 21 MB)
- ✓ data/processed/sentiment_summary.json (NUEVO)
```

---

## Estado de la Rama

- **Rama:** `feature/fase-2-3-nlp-improvements`
- **Commits:** Documentados en git log
- **Pull Request:** Listo para revisar por mariafd412

---

**Próxima reunión:** FASE 3 completada ✓ - Iniciar FASE 4 (Evaluación) y FASE 5 (Visualización)
