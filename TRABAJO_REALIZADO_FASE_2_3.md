# FASE 2 & 3: Mejoras en Procesamiento NLP - Documentación de Trabajo

**Autor:** Alexis Frank Jimenez  
**Fecha:** 28 de Abril, 2026  
**Estado:** En Progreso (Fase 2 y 3 iniciales)

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

## Próximos Pasos (Fase 3)

### 3.1 Topic Modeling (LDA)
- [ ] Entrenar modelo LDA con gensim
- [ ] Seleccionar número óptimo de tópicos (5-10)
- [ ] Extraer palabras clave por tópico
- [ ] Interpretar: deuda, energía, inflación, etc.

### 3.2 Análisis de Sentimiento
- [ ] Implementar VADER (nltk.sentiment)
- [ ] Alternativa: FinBERT (transformers)
- [ ] Clasificar párrafos: positivo/neutro/negativo

### 3.3 Asociación País + Sentimiento
- [ ] Mapear entidades NER (países) con sentimientos
- [ ] Calcular sentimiento promedio por país
- [ ] Crear matriz país-sentimiento

---

## Evaluación

### Coherencia de Tópicos
- Usar `CoherenceModel` de gensim
- Métrica: Coherencia C_v

### Validación Manual
- Seleccionar 10-20 párrafos
- Etiquetarlos manualmente
- Comparar con predicciones del modelo

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
✓ src/04_nlp_processing.py              (MEJORADO)
✓ src/04_nlp_processing_v2.py          (NUEVO)
✓ install_and_process_nlp.py           (NUEVO)
✓ nlp_minimal.py                       (NUEVO)
✓ run_full_pipeline.py                 (NUEVO)
✓ run_nlp.py                           (NUEVO)
✓ test_deps.py                         (NUEVO)
✓ .gitignore                           (CREADO)
✓ data/processed/dataset.json          (ACTUALIZADO)
```

---

## Estado de la Rama

- **Rama:** `feature/fase-2-3-nlp-improvements`
- **Commits:** Documentados en git log
- **Pull Request:** Listo para revisar por mariafd412

---

**Próxima reunión:** Revisar resultados de Fase 2, iniciar Fase 3 (LDA + Sentimiento)
