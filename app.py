from flask import Flask, render_template, request, jsonify, make_response
from json import dumps
from string import Template
from collections import Counter
from datetime import datetime

app = Flask(__name__)


HTML_TEMPLATE = Template("""
<h1>Hello ${note_ID}!</h1>

<p>Hello world!</p>
""")


@app.route('/places/<p>')
def places_view(p):
    return(HTML_TEMPLATE.substitute(note_ID=p))

@app.route('/notes/<url_note_ID>')
def note_page(url_note_ID):
    return(HTML_TEMPLATE.substitute(note_ID=url_note_ID))


    """
    note_ID = "rhuahdagwhhja"
    PULL FROM DB WHERE ID = note_ID
    RETURN CONTENT
    """




@app.route('/')
def index():
    return render_template('index.html')


@app.route('/notes/', methods=['POST'])
def poast():
    print(request.form.get('letters', 0))
    # letters = list(request.form.get('letters', 0).lower())
    # charSet = Counter(letters)

    # matches = []
    # with open('scrabble.txt', 'r') as f:
    #     input = f.readlines()

    # # traverse words in list, remove \n then check if the word can be made from the letters given. return an array of matched words.
    # for word in input:
    #     word = word.replace('\n', '').lower()
    #     # if first letter isn't in the character list, skip it
    #     if word[0] not in charSet:
    #         continue

    #     if not Counter(word) - charSet:
    #         matches.append(word)
        

    # return make_response(dumps(matches))


if __name__ == '__main__':
    app.run(debug=True)
