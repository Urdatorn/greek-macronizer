import os
from bs4 import BeautifulSoup

def find_syllable_lengths(html_content, input_word):
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Define a list to hold the results
    syllable_lengths = []
    
    # Iterate through each 'word' class in the HTML
    for word_div in soup.find_all(class_="word"):
        # Extract the syllables and their classes
        syllables = [(syll.text, 'long' if 'long' in syll['class'] else 'short') for syll in word_div.find_all('span')]
        
        # Join the syllables to form the complete word
        reconstructed_word = ''.join(syll[0] for syll in syllables)
        print(reconstructed_word)
        
        # Check if the reconstructed word matches the input word
        if reconstructed_word == input_word:
            # Map the syllable lengths to the desired format (_ for long, ^ for short)
            formatted_syllables = [[syll[0], '_' if syll[1] == 'long' else '^'] for syll in syllables]
            syllable_lengths.append(formatted_syllables)
    
    return syllable_lengths

# Example usage
html_content = '''
<div class="latin" id="latindiv"><div class="line hexameter" data-number="1" data-metre="hexameter"><span class="word"><span class="syll long">ἀρ</span><span class="syll short">χό</span><span class="syll short">με</span><span class="syll long">νος</span></span><span> </span><span class="word"><span class="syll short">σέ</span><span class="syll short">ο,</span></span><span> </span><span class="word"><span class="syll long">Φοῖ</span><span class="syll short">βε,</span></span><span> </span><span class="word"><span class="syll short">πα</span><span class="syll long">λαι</span><span class="syll short">γε</span><span class="syll short">νέ</span><span class="syll long">ων</span></span><span> </span>
'''

input_word = "ἀρχόμενος"
matches = find_syllable_lengths(html_content, input_word)

for match in matches:
    print(match)
