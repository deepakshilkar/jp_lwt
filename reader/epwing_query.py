from reader.yomichan_to_dict import epwing
# import json
# from natto import MeCab


def get_definition(word):
    try:
        e = epwing[word]
    except KeyError:
        e = ["Word not Found", "", [""]]

    r = {"word": e[0], "reading": e[1], "definitions": e[2]}
    return r
