# Input file path
input_file_name = "tokens/tragedies_300595_pos.txt"  # Replace with your file path

# Output file in the current working directory
output_file_name = "tokens/tragedies_300595.txt"  # Replace with your desired output file name

# Read the input file and process it
with open(input_file_name, 'r', encoding='utf-8') as input_file, \
     open(output_file_name, 'w', encoding='utf-8') as output_file:
    for line in input_file:
        # Split the line into rows based on tab delimiter
        rows = line.strip().split('\t')
        
        # Check if there are at least three rows
        if len(rows) >= 3:
            # Join the rows starting from the second row
            processed_line = '\t'.join(rows[1:])
            
            # Write the processed line to the output file
            output_file.write(processed_line + '\n')

# The processed data has been written to the output file
print(f"Processed data has been written to {output_file_name}")