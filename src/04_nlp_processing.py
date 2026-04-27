# Cargar librerías
import json
import spacy
from nltk.corpus import stopwords

# Cargar modelo de lenguaje
nlp = spacy.load("en_core_web_sm")

# Stopwords personalizadas
stop_words = set(stopwords.words("english"))

# palabras que NO queremos eliminar
keep_words = {"growth", "inflation", "crisis", "deficit"}

# quitarlas de stopwords
stop_words = stop_words - keep_words

# Función para procesar texto

def process_text(text):
    doc = nlp(text)

    tokens = []

    for token in doc:
        if token.is_alpha:  # solo palabras
            word = token.lemma_.lower()

            if word not in stop_words:
                tokens.append(word)

    return tokens

# Definir identidades NER
def extract_entities(text):
    doc = nlp(text)

    countries = []
    orgs = []

    for ent in doc.ents:
        if ent.label_ == "GPE":  # países/ciudades
            countries.append(ent.text)
        elif ent.label_ == "ORG":
            orgs.append(ent.text)

    return countries, orgs

# Aplicar procesamiento a dataset
INPUT_FILE = "data/processed/dataset.json"
OUTPUT_FILE = "data/processed/dataset_nlp.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

new_data = []

for row in data:
    text = row["texto"]

    tokens = process_text(text)
    countries, orgs = extract_entities(text)

    row["tokens"] = tokens
    row["pais"] = countries
    row["organizacion"] = orgs

    new_data.append(row)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(new_data, f, indent=2, ensure_ascii=False)

print("NLP completado 🚀")