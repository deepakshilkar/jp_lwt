from flask import jsonify, render_template, request
from reader import reader
from reader.dict_query import get_definition
from reader.users_query import get_knowledge, add_word
from reader.no_parsing import get_no_parsing
from natto import MeCab
import os


@reader.route('/definition/<word>')
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


@reader.route('/')
def reader():
    module_dir = os.path.dirname(__file__)  # get current directory
    filename = os.path.join(module_dir, 'test.txt')
    file = open(filename, "r", encoding="utf8")
    tokenized_text = []
    no_parsing = get_no_parsing()
    known_words = get_knowledge("moi")
    words = {}
    nm = MeCab("-Owakati")
    for line in file.readlines():
        for n in nm.parse(line, as_nodes=True):
            tokenized_text.append(n.surface)
            if n.surface not in known_words and n.surface not in no_parsing:
                words[n.surface] = 0
            elif n.surface in known_words:
                words[n.surface] = known_words[n.surface]
        tokenized_text.append("<br>")
    return render_template("reader.html",
                           words=words,
                           tokenized_text=tokenized_text)
