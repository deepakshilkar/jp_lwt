from flask import jsonify, render_template
from reader import reader
from reader.dict_query import get_definition
from natto import MeCab
from reader.users_query import get_knowledge, add_word
import os


@reader.route('/definition/<word>')
def definition(word):
    d = get_definition(word)
    return jsonify(d)


@reader.route('/api/add_word/<word>/<level>/<user>', methods=['POST'])
def add_new_word(word, level, user):
    add_word(user, word, level)


@reader.route('/')
def reader():
    module_dir = os.path.dirname(__file__)  # get current directory
    filename = os.path.join(module_dir, 'test.txt')
    file = open(filename, "r", encoding="utf8")
    tokenized_text = []
    known_words = get_knowledge("moi")
    words = {}
    no_parsing = ["", ".", ",", " ", "。", "、", "\n"]
    nm = MeCab("-Owakati")
    for q in file.readlines():
        for n in nm.parse(q, as_nodes=True):
            tokenized_text.append(n.surface)
            if n.surface not in known_words and n.surface not in no_parsing:
                words[n.surface] = 0
            elif n.surface in known_words:
                words[n.surface] = known_words[n.surface]
        tokenized_text.append("\n")
    return render_template("reader.html",
                           words=words,
                           tokenized_text=tokenized_text)
