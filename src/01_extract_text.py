import fitz  # PyMuPDF
import os

INPUT_FOLDER = "data/raw"
OUTPUT_FOLDER = "data/processed"

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""

    for page in doc:
        text += page.get_text()

    return text

def main():
    for file in os.listdir(INPUT_FOLDER):
        if file.endswith(".pdf"):
            path = os.path.join(INPUT_FOLDER, file)
            print(f"Procesando {file}...")

            text = extract_text_from_pdf(path)

            output_file = file.replace(".pdf", ".txt")
            output_path = os.path.join(OUTPUT_FOLDER, output_file)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)

if __name__ == "__main__":
    main()