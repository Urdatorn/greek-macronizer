from flask import Flask, render_template
import csv

app = Flask(__name__)

@app.route('/')
def dictionary():
    # Path to your dictionary file
    dictionary_path = 'prepare_tokens/tokens/tokens.txt'
    
    # Read the dictionary file
    dictionary_data = []
    with open(dictionary_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            dictionary_data.append(row)
    
    # Pass the data to the frontend
    return render_template('dictionary.html', dictionary_data=dictionary_data)

if __name__ == '__main__':
    app.run(debug=True)
