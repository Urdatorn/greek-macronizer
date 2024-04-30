'''
Format the crawled LSJ macrons, e.g. 

    πλάτας	n-p---fa-	πλάτη	πλᾰ́τας

and turn them into the likes of

    πλάτας	n-p---fa-	πλάτη	^3

The logic is exactly the same as in the Wiktionary crawl_format_macrons.py, and so can be reused.

'''

import csv

def filter_non_empty_fourth_column(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8', newline='') as infile, \
         open(output_file_path, 'w', encoding='utf-8', newline='') as outfile:
        
        reader = csv.reader(infile, delimiter='\t')
        writer = csv.writer(outfile, delimiter='\t')

        # Iterate through each line in the input TSV
        for line in reader:
            # Check if the line has at least four columns and the fourth column is not empty
            if len(line) >= 4 and line[3].strip():
                # Write the line to the output file if the fourth column is non-empty
                writer.writerow(line)

# Example usage
input_file_path = 'crawl_lsj/macrons_lsj_raw_old.tsv'
output_file_path = 'crawl_lsj/macrons_lsj_raw_old_filter.tsv'
#filter_non_empty_fourth_column(input_file_path, output_file_path)


###


