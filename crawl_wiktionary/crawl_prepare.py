'''
USING  greek_accentuation TO REFORMAT MACRONS/BREVES

Most important here is to handle the polytonic Greek dichrona with combining longum/macron (U+0304) or breve/brachy/vrachy (U+0306):

Ᾱ, Ῑ, Ῡ
Ᾰ, Ῐ, Ῠ

as well as when these are combined with accents, e.g.

Ᾱ́, Ῑ́, 

or, most precariously, both with accents and spiritus, e.g.

Ῠ̔́.

They will probably have to be decomposed.

The goal is that if a polytonic character has a macron, 
it is written in the output as without the macron and followed by _ (underscore), e.g. 

input Ᾱ => output A_
input Ᾱ́ => output Ά_

Analogously, if a polytonic character has a breve,
it is written in the output as without the breve and followed by ^ (exponential/caret), e.g.

input Ᾰ => output A

'''

import crawl_format_macrons
import crawl_beta
import crawl_stars
import crawl_sort
import crawl_remove_duplicates

input_file_path = 'crawl/macrons_wiktionary_unicode.txt'
output_file_path = 'crawl/macrons_wiktionary.txt'

crawl_format_macrons.process_file(input_file_path, 'crawl/macrons_wiktionary_format.txt')
crawl_beta.translate_to_beta_code('crawl/macrons_wiktionary_format.txt', 'crawl/macrons_wiktionary_beta.txt')
crawl_stars.remove_stars('crawl/macrons_wiktionary_beta.txt', 'crawl/macrons_wiktionary_stars.txt')
crawl_remove_duplicates.remove_duplicates('crawl/macrons_wiktionary_stars.txt', 'crawl/macrons_wiktionary_dup.txt')
crawl_sort.sort_file('crawl/macrons_wiktionary_dup.txt', output_file_path)

print(f"Succé!")