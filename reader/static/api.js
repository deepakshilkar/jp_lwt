let api_add_word = (_word, _level) => {
    var data = new FormData()
    data.append('word', _word)
    data.append('level', _level)

    fetch('/api/add_word', {
        method: 'POST',
        body: data
    })
}


let api_get_definition = (word) => {
    fetch('/api/definition/' + word)
        .then(function(response){
            response.json().then(function(data){
                def = document.body.querySelectorAll("definitions");
                definition = format_definition(data);
                Array.prototype.map.call(def, function(x){
                    apply_definition(x, definition);
                });
            });
        });
}

let apply_definition = (x, definition) => {
    x.innerHTML = definition;
}

let format_definition = (json) => {
    let definition = "";
    definition += "<span class = 'word'>"
    definition += json.word;
    definition += "</span>"
    definition += "<br>"
    for (i = 0; i < json.definitions.length; i++){
        definition += "<span class = 'definition'>"
        console.log(json.definitions[i]);
        definition += json.definitions[i].replace(/\n/g,"<br>");
        definition += "</span>"
    }
    return definition;
}
