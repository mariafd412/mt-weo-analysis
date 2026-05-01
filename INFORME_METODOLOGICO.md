# Informe Metodológico: Análisis NLP del World Economic Outlook (FMI)

**Fecha:** Abril 2026  
**Autor:** Alexis Frank Jimenez  
**Objetivo:** Asesoramiento a inversores sobre riesgos macroeconómicos emergentes y sentimiento global.

---

## 1. Definición del Supuesto Práctico
Este proyecto aborda la necesidad de procesar grandes volúmenes de texto (miles de páginas de informes WEO del FMI) para extraer inteligencia financiera accionable. 
Dado que los analistas y tomadores de decisiones no tienen el tiempo material para leer y analizar todo el corpus, se ha implementado un *pipeline* automatizado de Inteligencia Artificial y Procesamiento de Lenguaje Natural (PLN). El alcance abarca la identificación de riesgos emergentes, análisis del tono económico (sentimiento) y su distribución a nivel geoespacial.

---

## 2. Técnicas de Procesamiento de Lenguaje Natural (PLN)

### 2.1 Segmentación y Preprocesamiento
Los documentos fueron ingeridos y divididos en unidades lógicas (párrafos) para preservar el contexto de las declaraciones del FMI. 

**Justificación de Stopwords Financieras:**
Se utilizó un filtrado de palabras vacías (stopwords) adaptado al dominio. A diferencia de un análisis de texto general, se conservaron explícitamente términos clave como *"growth"*, *"deficit"*, *"inflation"* o *"crisis"*. Eliminar estas palabras habría destruido la señal económica del texto, ya que representan los núcleos semánticos de las proyecciones macroeconómicas.

### 2.2 Reconocimiento de Entidades Nombradas (NER)
Para asociar las advertencias de riesgo a geografías específicas, se aplicó un modelo NER (mediante la librería `spaCy`). Esto permitió extraer automáticamente entidades del tipo `GPE` (países y regiones) y `ORG` (instituciones como el BCE o el propio FMI), creando una base de datos relacional entre el texto, su sentimiento y la nación afectada.

### 2.3 Representación Vectorial
**Justificación de Modelos Vectoriales:**
Para el descubrimiento de tópicos se utilizó la representación de Bolsa de Palabras (BoW) y TF-IDF, lo cual es altamente efectivo para destacar términos únicos y emergentes del 2026 (por ejemplo, "fragmentation"). Esta representación matricial otorga mayor peso a los términos económicamente raros pero significativos frente a la jerga repetitiva.

---

## 3. Algoritmos de Minería de Texto y Evaluación

### 3.1 Modelado de Tópicos (Latent Dirichlet Allocation - LDA)
Se aplicó el algoritmo LDA para descubrir la estructura temática subyacente de forma no supervisada. El modelo fue capaz de agrupar el vocabulario en clústeres interpretables (ej. Tópicos relacionados con deuda, transición energética, etc.).

**Marco de Evaluación:** Se midió el *score de relevancia* de cada tópico (disponible en `topics_evaluation.json`), validando la coherencia semántica de los grupos de palabras. Las visualizaciones confirman que los tópicos detectados tienen un claro sentido económico.

### 3.2 Análisis de Sentimiento Financiero
**Justificación del enfoque:**
El lenguaje institucional del FMI es diplomático, sutil y cauteloso. Un modelo de sentimiento genérico entrenado en redes sociales (como análisis de tweets) fallaría rotundamente aquí, marcando como "neutras" declaraciones que para un economista son alarmas graves. Por ello, se justificó el uso de léxicos basados en reglas orientadas a la polaridad o ajustados a contextos formales (como VADER ajustado o modelos tipo FinBERT), capaces de captar la negatividad de palabras como "downgrade" o "contraction".

**Marco de Evaluación:** Los resultados fueron sometidos a un escrutinio estadístico, calculando el *Compound Score* promedio y su desviación estándar (almacenados en `sentiment_evaluation.json`), mostrando una distribución que refleja la cautela macroeconómica real del periodo.

---

## 4. Visualización e Impacto (Dashboard de Inteligencia)
Para entregar valor al usuario final (bancos e inversores), los datos procesados fueron proyectados en diversas herramientas visuales:

1. **Mapa Mundial de Sentimientos:** Mediante cruce de coordenadas geoespaciales (`Geopandas`/`Plotly`) y el sentimiento extraído, se generó un mapa donde los inversores pueden visualizar rápidamente la inestabilidad por país.
2. **Análisis de Tendencias Temporales:** Se graficó la evolución temporal de términos de alto impacto (como "fragmentation" e "inflation"), permitiendo comparar las alertas del 2026 contra años anteriores.
3. **Resúmenes Automáticos (TextRank):** Para ahorrar tiempo de lectura, se integró el algoritmo de grafos TextRank (`sumy`), el cual permite seleccionar un país específico (ej. China o Estados Unidos) y generar un resumen extractivo de los 5 párrafos más relevantes del WEO referentes a esa nación.

---

## 5. Conclusión
El *pipeline* desarrollado cumple exitosamente con los requisitos de la consultora de riesgos. Transforma datos no estructurados (miles de páginas de PDF) en inteligencia financiera estructurada, visual, medible y orientada a la toma de decisiones estratégicas.