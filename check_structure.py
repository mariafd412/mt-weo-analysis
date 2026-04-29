import json

# Verificar estructura de lda_results.json
with open('data/processed/lda_results.json', 'r', encoding='utf-8') as f:
    lda = json.load(f)

print("=== LDA RESULTS ===")
print("Claves:", list(lda.keys()))
print("num_topics:", lda.get('num_topics'))
print("coherence_score:", lda.get('coherence_score'))
print("\nTopics type:", type(lda.get('topics')))
if lda.get('topics'):
    print("Num topics:", len(lda['topics']))
    print("First topic:", json.dumps(lda['topics'][0], indent=2, ensure_ascii=False))

# Verificar dataset con encoding fix
print("\n=== DATASET WITH SENTIMENT ===")
with open('data/processed/dataset_with_sentiment.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("Type:", type(data).__name__)
if isinstance(data, list):
    print("Length:", len(data))
    if data:
        print("\nFirst item:")
        print(json.dumps(data[0], indent=2, ensure_ascii=False))
else:
    print("Keys:", list(data.keys())[:10])
