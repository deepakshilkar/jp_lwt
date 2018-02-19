import json
import requests


def jisho_get_definition(word):
    url = 'http://jisho.org/api/v1/search/words?keyword='
    url += word
    response = requests.get(url)
    if response.status_code == 200:
        return json.loads(response.content)
    else:
        return {'meta': 999}
