import unicodedata
import csv

def normalize_tsv_to_nfc(input_file_path, output_file_path):
    """
    Normalizes each entry in a TSV file to Unicode NFC form.
    
    Args:
    input_file_path (str): The path to the input TSV file.
    output_file_path (str): The path to the output TSV file where normalized data will be saved.
    """
    with open(input_file_path, 'r', encoding='utf-8') as infile, \
         open(output_file_path, 'w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.reader(infile, delimiter='\t')
        writer = csv.writer(outfile, delimiter='\t')
        
        for row in reader:
            # Normalize each field using NFC and write to the output file
            normalized_row = [unicodedata.normalize('NFC', field) for field in row]
            writer.writerow(normalized_row)

    print(f"Normalization complete. Output saved to: {output_file_path}")

# Example usage
input_tsv_path = 'crawl_wiktionary/macrons_wiktionary_test_format.tsv'  # Update this path
output_tsv_path = 'crawl_wiktionary/macrons_wiktionary_test_format_nfc.tsv'  # Update this path
normalize_tsv_to_nfc(input_tsv_path, output_tsv_path)
