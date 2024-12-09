import os
import re
import time

def read_file_with_encoding(filepath):
    """Handle multiple encodings gracefully."""
    encodings = ['utf-8', 'ISO-8859-1', 'windows-1252']
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            continue  # Try the next encoding
    # If all encodings fail, open with 'errors=ignore'
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
        return file.read()

def fix_xml_file(filepath):
    """Fix malformed XML tags in the file and save the corrected content."""
    content = read_file_with_encoding(filepath)

    # Fix malformed <citation "id=cX"> to <citation id="cX">
    fixed_content = re.sub(r'<citation "id=(.*?)">', r'<citation id="\1">', content)

    # Fix malformed <catchphrase "id=cX"> to <catchphrase id="cX">
    fixed_content = re.sub(r'<catchphrase "id=(.*?)">', r'<catchphrase id="\1">', fixed_content)

    # Fix malformed <sentence "id=sX"> to <sentence id="sX">
    # fixed_content = re.sub(r'<sentence "id=(.*?)">', r'<sentence id="\1">', fixed_content)

    # Save the corrected content back to the file
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(fixed_content)

def fix_folder_xml(folder_path):
    """Process all XML files in the folder, track progress, and measure time."""
    start_time = time.time()
    total_files = len([f for f in os.listdir(folder_path) if f.endswith('.xml')])
    processed_files = 0

    print(f"Starting the process for {total_files} XML files...\n")

    for filename in os.listdir(folder_path):
        if filename.endswith('.xml'):
            filepath = os.path.join(folder_path, filename)
            # print(f"Processing file {processed_files + 1} of {total_files}: {filename}...")

            try:
                fix_xml_file(filepath)
                processed_files += 1
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nProcessed {processed_files} files in {folder_path} in {elapsed_time:.2f} seconds.")

if __name__ == "__main__":
    # Provide the folder path containing XML files
    CC_folder_path = os.path.join('2_Generation', 'raw_data', 'citations_class')
    FT_folder_path = os.path.join('2_Generation', 'raw_data', 'fulltext')
    
    # Start the process of fixing XML files
    fix_folder_xml(CC_folder_path)
    fix_folder_xml(FT_folder_path)
