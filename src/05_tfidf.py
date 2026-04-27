from sklearn.feature_extraction.text import TfidfVectorizer
import json
from gensim.models import Word2Vec

# TF-IDF
with open("data/processed/dataset_nlp.json", "r") as f:
    data = json.load(f)

texts = [" ".join(row["tokens"]) for row in data]

vectorizer = TfidfVectorizer(max_features=100)
X = vectorizer.fit_transform(texts)

print(vectorizer.get_feature_names_out())

# Word2Vec
sentences = [row["tokens"] for row in data]

model = Word2Vec(sentences, vector_size=100, window=5, min_count=2)

print(model.wv.most_similar("inflation"))