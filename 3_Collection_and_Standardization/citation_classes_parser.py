import os
import re
import time
import pandas as pd

def read_file_with_encoding(filepath):
    """Handle multiple encodings gracefully."""
    encodings = ['utf-8', 'ISO-8859-1', 'windows-1252']
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            continue
    # If all encodings fail, open with 'errors=ignore'
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
        return file.read()

def extract_value(text, tag):
    """Extract the first occurrence of a value enclosed by a given tag."""
    pattern = f'<{tag}>(.*?)</{tag}>'
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else None

def extract_catchphrases(text):
    """Extract all <catchphrase> elements and return as a list."""
    pattern = re.compile(r'<catchphrase\s+id="(.*?)">(.*?)</catchphrase>', re.DOTALL)
    return [match.group(2).strip() for match in pattern.finditer(text)]

def extract_sentences(text):
    """Extract all <sentence> elements and join them into a single paragraph."""
    pattern = re.compile(r'<sentence\s+id="(.*?)">(.*?)</sentence>', re.DOTALL)
    sentences = [match.group(2).strip() for match in pattern.finditer(text)]
    return ' '.join(sentences)

def parse_file(filepath):
    """Parse the XML file as raw text and extract relevant data."""
    content = read_file_with_encoding(filepath)

    # Extract required fields
    case_name = extract_value(content, 'name')
    AustLII_link = extract_value(content, 'AustLII')
    catchphrases = extract_catchphrases(content)
    sentences = extract_sentences(content)

    return {
        'filename': os.path.basename(filepath),
        'name': case_name,
        'AustLII': AustLII_link,
        'catchphrases': catchphrases,
        'sentences': sentences
    }

def parse_folder(folder_path):
    """Parse all XML files in the folder."""
    start_time = time.time()
    total_files = len([f for f in os.listdir(folder_path) if f.endswith('.xml')])
    data = []

    print(f"Parsing {total_files} XML files...\n")

    for filename in os.listdir(folder_path):
        if filename.endswith('.xml'):
            filepath = os.path.join(folder_path, filename)
            print(f"Parsing {len(data) + 1}/{total_files}: {filename}")

            try:
                parsed_data = parse_file(filepath)
                data.append(parsed_data)
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    elapsed_time = time.time() - start_time
    print(f"\nParsed {len(data)} files in {elapsed_time:.2f} seconds.")
    return data

if __name__ == "__main__":
    # Relative path to the folder
    folder_path = os.path.join('2_Generation', 'raw_data', 'fulltext')

    # Parse the folder and save to CSV
    data = parse_folder(folder_path)
    df = pd.DataFrame(data)
    dest_folder_path = '2_Generation/extracted_data/parsed_fulltext_cases.csv'
    df.to_csv(dest_folder_path, index=False)
    print("\nData saved to ", dest_folder_path)
