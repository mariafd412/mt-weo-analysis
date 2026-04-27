import json
from collections import Counter

with open("data/processed/dataset_nlp.json", "r") as f:
    data = json.load(f)

all_tokens = []

for row in data:
    all_tokens.extend(row["tokens"])

counter = Counter(all_tokens)

print("\nTOP 50 palabras:\n")
for word, freq in counter.most_common(50):
    print(word, freq)