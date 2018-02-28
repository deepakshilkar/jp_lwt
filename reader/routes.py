from flask import jsonify, render_template, request
from reader import reader
from reader.epwing_query import get_definition
from reader.users_query import get_knowledge, add_word
from reader.no_parsing import get_no_parsing
# from reader.jisho_api import jisho_get_definition
from natto import MeCab
import os
import io

@reader.route('/api/definition/<word>')
def definition(word):
    d = get_definition(word)
    return jsonify(d)


@reader.route('/api/add_word', methods=['POST'])
def add_new_word():
    user = "moi"
    word = request.form['word']
    level = request.form['level']
    add_word(user, word, level)
    return ""


@reader.route('/', methods=['GET', 'POST'])
def reader_view():
    if request.method == 'POST':
        content = io.StringIO(request.form['text'])
    else:
        module_dir = os.path.dirname(__file__)  # get current directory
        filename = os.path.join(module_dir, 'initial_text.txt')
        content = open(filename, "r", encoding="utf8")
    r = process(content)
    return render_template("reader.html",
                           words=r['words'],
                           tokenized_text=r['tokenized_text'],
                           token_count=r['token_count'])


# Helper methods

def process(x):
    tokenized_text = []
    token_count = 0
    no_parsing = get_no_parsing()
    known_words = get_knowledge("moi")
    words = {}
    nm = MeCab("-Owakati")
    for line in x.readlines():
        for n in nm.parse(line, as_nodes=True):
            tokenized_text.append(n.surface)
            if n.surface not in known_words and n.surface not in no_parsing:
                words[n.surface] = 0
            elif n.surface in known_words:
                words[n.surface] = known_words[n.surface]
            token_count += 1
        tokenized_text.append("<br>")
    return {'tokenized_text': tokenized_text,
            'words': words,
            'token_count': str(token_count)}
