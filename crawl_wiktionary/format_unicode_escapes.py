def format_dictionary(input_file_path, output_file_path):
    # Read the input file content
    with open(input_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Open the output file to write the reformatted dictionary
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for line in lines:
            # Check if the line contains dictionary entries
            if ':' in line and '+' in line.split(':')[0]:
                # Split the line into key and rest (value and comment)
                key, rest = line.split(':', 1)
                # Reformat the key by replacing '0x' with '\u' and ensuring correct hex length
                formatted_keys = ''.join(['\\u' + part[2:].zfill(4).upper() for part in key.replace(' ', '').replace("'", "").split('+')])
                # Write the formatted key with unchanged rest to the output file
                file.write(f"    '{formatted_keys}':{rest}")
            else:
                # Write lines that are not part of the dictionary unchanged
                file.write(line)

# Example usage
input_file_path = 'crawl_wiktionary/macrons_map_complete.py'  # Input file containing the dictionary
output_file_path = 'crawl_wiktionary/macrons_map_complete2.py'  # Output file for the formatted dictionary
format_dictionary(input_file_path, output_file_path)
