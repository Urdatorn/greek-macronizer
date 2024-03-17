# Define the paths to your input and output files
input_file_path = 'prepare_tokens/tokens/tragedies_300595_pos.txt'
output_file_path = 'prepare_tokens/tokens/tragedies_300595_pos_last.txt'

# Initialize counters for the number of lines processed
lines_processed = 0
total_lines = 0

# Open the input file for reading and the output file for writing
with open(input_file_path, 'r', encoding='utf-8') as infile:
    # Count the total number of lines in the input file
    total_lines = sum(1 for _ in infile)

# Re-open the input file to process the lines
with open(input_file_path, 'r', encoding='utf-8') as infile, open(output_file_path, 'w', encoding='utf-8') as outfile:
    for line in infile:
        # Split the line into columns based on the tab delimiter
        columns = line.strip().split('\t')
        
        # Shift the first column to the end, regardless of the total number of columns
        if columns:  # Ensure the line is not empty
            new_order = columns[1:] + [columns[0]]  # Move the first column to the end
            
            # Join the columns with a tab and write to the output file
            outfile.write('\t'.join(new_order) + '\n')
            
            # Increment the lines processed counter
            lines_processed += 1

# Print confirmation that all lines were successfully processed
print(f"All lines were successfully shifted. Total lines processed: {lines_processed} out of {total_lines}.")

# Additional debugging information
if lines_processed == total_lines:
    print("All lines in the file were processed successfully.")
else:
    print(f"Warning: Not all lines might have been processed correctly. Processed lines: {lines_processed}, Total lines in file: {total_lines}.")