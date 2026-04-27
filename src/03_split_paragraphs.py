import os
import json

INPUT_FOLDER = "data/processed"

def split_paragraphs(text):
    return [p.strip() for p in text.split("\n") if len(p.strip()) > 50]

def main():
    dataset = []
    parrafo_id = 0

    for file in os.listdir(INPUT_FOLDER):
        if file.endswith(".txt"):
            path = os.path.join(INPUT_FOLDER, file)

            with open(path, "r", encoding="utf-8") as f:
                text = f.read()

            paragraphs = split_paragraphs(text)

            for p in paragraphs:
                dataset.append({
                    "doc": file,
                    "parrafo_id": parrafo_id,
                    "texto": p,
                    "region": None  # lo rellenaremos con NER luego
                })
                parrafo_id += 1

    with open("data/processed/dataset.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()