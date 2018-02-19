let api_add_word = (_word, _level) => {
    var data = new FormData()
    data.append('word', _word)
    data.append('level', _level)

    fetch('/api/add_word', {
        method: 'POST',
        body: data
    })
}
