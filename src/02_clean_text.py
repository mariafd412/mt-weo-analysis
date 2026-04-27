import re
import os

INPUT_FOLDER = "data/processed"
OUTPUT_FOLDER = "data/processed"

def clean_text(text):
    # eliminar saltos de línea múltiples
    text = re.sub(r"\n+", "\n", text)

    # eliminar espacios múltiples
    text = re.sub(r"\s+", " ", text)

    # eliminar caracteres raros
    text = re.sub(r"[^\x00-\x7F]+", " ", text)

    return text

def main():
    for file in os.listdir(INPUT_FOLDER):
        if file.endswith(".txt"):
            path = os.path.join(INPUT_FOLDER, file)

            with open(path, "r", encoding="utf-8") as f:
                text = f.read()

            clean = clean_text(text)

            with open(path, "w", encoding="utf-8") as f:
                f.write(clean)

            print(f"Limpio: {file}")

if __name__ == "__main__":
    main()