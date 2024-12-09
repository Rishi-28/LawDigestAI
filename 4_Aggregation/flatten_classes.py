import pandas as pd
import ast  # To safely evaluate citation dictionaries from strings

def flatten_citations_from_file(input_csv, output_csv):
    """Read the generated file, flatten citations, and save to a new CSV."""
    # Step 1: Read the CSV file into a DataFrame
    df = pd.read_csv(input_csv)

    # Step 2: Initialize an empty list to store flattened citation data
    flattened_data = []

    # Step 3: Loop through each row in the DataFrame
    for index, row in df.iterrows():
        filename = row['filename']
        citations = ast.literal_eval(row['citations'])  # Convert string to list of dicts

        # Step 4: Flatten each citation
        for citation in citations:
            flattened_data.append({
                'filename': filename,
                'citation_id': citation.get('id', None),
                'class': citation.get('class', None),
                'tocase': citation.get('tocase', None),
                'AustLII': citation.get('AustLII', None),
                'text': citation.get('text', None)
            })

    # Step 5: Create a new DataFrame from the flattened data
    flattened_df = pd.DataFrame(flattened_data)

    # Step 6: Save the flattened DataFrame to a new CSV file
    flattened_df.to_csv(output_csv, index=False)

    print(f"Flattened data saved to '{output_csv}'.")

if __name__ == "__main__":
    # Specify input and output file paths here
    input_csv = '2_Generation/extracted_data/parsed_citation_classes.csv'  # Input CSV file path
    output_csv = '2_Generation/extracted_data/flattened_citation_classes.csv'     # Output CSV file path

    # Run the flattening function with the specified paths
    flatten_citations_from_file(input_csv, output_csv)
