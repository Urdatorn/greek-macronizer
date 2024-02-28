# Import necessary libraries
import requests
from bs4 import BeautifulSoup

# Function to get the word from the LSJ website
def get_word_from_lsj(greek_word):
    # URL construction
    url = f"https://lsj.gr/wiki/{greek_word}"
    
    # Send a request to the website
    response = requests.get(url)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Search for the <span> element with the specified title
        span_elements = soup.find_all('span', title="Look up on Google")
        if span_elements:
            # Iterate through all found elements (there might be more than one)
            for span_element in span_elements:
                word = span_element.get_text()
                print(word)
        else:
            print("Couldn't find the span element with the specified title.")
    else:
        print("Failed to fetch the webpage or the page doesn't exist.")

# Test the function with an example Greek polytonic word
test_word = "νεανίας"  # You can replace tahis with any Greek polytonic word
get_word_from_lsj(test_word)
