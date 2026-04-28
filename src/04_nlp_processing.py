# Cargar librerías
import json
import spacy
from nltk.corpus import stopwords

# Cargar modelo de lenguaje
nlp = spacy.load("en_core_web_sm")

# Aumentar límite (por seguridad)
nlp.max_length = 2000000

# Stopwords personalizadas
stop_words = set(stopwords.words("english"))

domain_stopwords = {
    "percent", "year", "figure", "box", "chapter",
    "april", "october", "datum", "nso", "cb", "bpm", "cg",
    "outlook"
}

keep_words = {"growth", "inflation", "crisis", "deficit"}

# asegurar minúsculas
domain_stopwords = {w.lower() for w in domain_stopwords}
keep_words = {w.lower() for w in keep_words}

stop_words = stop_words.union(domain_stopwords)
stop_words = stop_words - keep_words


# 🔹 Función para dividir textos largos
def split_text(text, max_length=500000):
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]


# 🔹 Procesar doc
def process_doc(doc):
    tokens = []
    countries = []
    orgs = []

    for token in doc:
        if token.is_alpha:
            word = token.lemma_.lower()
            if word not in stop_words:
                tokens.append(word)

    for ent in doc.ents:
        if ent.label_ == "GPE":
            countries.append(ent.text)
        elif ent.label_ == "ORG":
            orgs.append(ent.text)

    return tokens, countries, orgs


# 🔹 Aplicar procesamiento
INPUT_FILE = "data/processed/dataset.json"
OUTPUT_FILE = "data/processed/dataset_nlp.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

new_data = []

for row in data:
    text = row["texto"]

    all_tokens = []
    all_countries = []
    all_orgs = []

    # 🔥 dividir si es muy grande
    chunks = split_text(text)

    for chunk in chunks:
        doc = nlp(chunk)
        tokens, countries, orgs = process_doc(doc)

        all_tokens.extend(tokens)
        all_countries.extend(countries)
        all_orgs.extend(orgs)

    row["tokens"] = all_tokens
    row["pais"] = list(set(all_countries))
    row["organizacion"] = list(set(all_orgs))

    new_data.append(row)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(new_data, f, indent=2, ensure_ascii=False)

print("NLP completado 🚀")