import os
import re
import pandas as pd
from xml.etree import ElementTree as ET

def read_file_with_encoding(filepath):
    """Handle multiple encodings gracefully."""
    encodings = ['utf-8', 'ISO-8859-1', 'windows-1252']
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            continue
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
        return file.read()

def extract_values(text, tag):
    """Extract all occurrences of a tag and return them as a list."""
    return [element.text.strip() for element in text.findall(tag) if element.text]

def parse_file(filepath):
    """Parse the XML file and extract the relevant data."""
    content = read_file_with_encoding(filepath)
    
    try:
        root = ET.fromstring(content)
        case_name = root.findtext('name')
        AustLII_link = root.findtext('AustLII')
        
        # Extract all <catchphrase> elements into a list
        catchphrases = extract_values(root.find('catchphrases'), 'catchphrase')
        
        # Combine all <sentence> elements into a single paragraph
        sentences = ' '.join(extract_values(root.find('sentences'), 'sentence'))

        return {
            'filename': os.path.basename(filepath),
            'name': case_name,
            'AustLII': AustLII_link,
            'catchphrases': catchphrases,
            'sentences': sentences
        }
    except ET.ParseError as e:
        print(f"Error parsing file {filepath}: {e}")
        return None

def parse_folder(folder_path):
    """Parse all XML files in the folder and return a DataFrame."""
    parsed_data = []
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.xml'):
            filepath = os.path.join(folder_path, filename)
            print(f"Parsing {filename}...")
            parsed_case = parse_file(filepath)
            if parsed_case:
                parsed_data.append(parsed_case)
    
    # Convert the parsed data into a DataFrame
    df = pd.DataFrame(parsed_data)
    return df

if __name__ == "__main__":
    # Specify the folder path containing your XML files
    folder_path = os.path.join('2_Generation', 'raw_data', 'fulltext')  # Adjust the path as needed
    
    # Parse the folder and get the DataFrame
    df = parse_folder(folder_path)
    
    # Save the DataFrame to a CSV file
    df.to_csv('2_Generation/extracted_data/parsed_fulltext_cases.csv', index=False)
    print("Data saved to 2_Generation/extracted_data/parsed_fulltext_cases.csv")
