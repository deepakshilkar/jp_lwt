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

let format_definition = (data) => {
    if (data.meta == 404)
        return "Word not found"
    return data.readings;
}


// https://www.html5rocks.com/en/tutorials/cors/#toc-making-a-cors-request
function createCORSRequest(method, url) {
  var xhr = new XMLHttpRequest();
  if ("withCredentials" in xhr) {

    // Check if the XMLHttpRequest object has a "withCredentials" property.
    // "withCredentials" only exists on XMLHTTPRequest2 objects.
    xhr.open(method, url, true);

  } else if (typeof XDomainRequest != "undefined") {

    // Otherwise, check if XDomainRequest.
    // XDomainRequest only exists in IE, and is IE's way of making CORS requests.
    xhr = new XDomainRequest();
    xhr.open(method, url);

  } else {

    // Otherwise, CORS is not supported by the browser.
    xhr = null;

  }
  return xhr;
}
