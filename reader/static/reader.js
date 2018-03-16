var index = 0; // current thing
var max; // number of morphenes
var textview; // DOM node
var elements; // all spans array
var height;
var token_count;


// Load a file
let load_file = () => {
    document.getElementById("file_choose").click();
}

// Read a file and send it to the server for processing then update view
let read_file = (e) => {
    var file = e.target.files[0];
    var new_page;
    if (!file) {
        return;
    }
    document.getElementById("reader").innerHTML = "Loading, Please Wait... (Huge files may take a few seconds)"
    var reader = new FileReader();
    reader.onload = function(e) {
        var contents = e.target.result;
        new_page = api_read_file(contents);
    };
    reader.readAsText(file);
}

// Hide border arround current morphene
let hide_border = (e) => {
    e.style.borderStyle = "none";
}

// Show border arround current morphene
let show_border = (e) => {
    e.style.borderStyle = "solid";
}


let show_definition = (e) => {
    api_get_definition(e.innerHTML);
}

// Switch to next non-known morphene
let next = () => {
    hide_border(elements[index]);
    index < max - 1? index++ : index;
    new_e = elements[index];
    show_border(new_e);
    show_definition(new_e);
}

// Switch to previous non-known morphene
let prev = () => {
    hide_border(elements[index]);
    index > 0 ? index-- : index;
    new_e = elements[index];
    show_border(new_e);
    show_definition(new_e);
}

// Scroll to / Center the page to the current morphene
let scroll_to = () => {
    var position = elements[index].offsetTop;
    window.scrollTo(0, position - height/2);
}

// Since "knowing" a word makes you need to skip things, you need to count the number of elements again, especially the max and current id
let re_query_elements = (offset) => {
    elements = textview.querySelectorAll("text-view span:not(.level-5)");
    max = elements.length;

    index = index - offset;
}

// set a word to a given level, call api, update database and classes
// Is this repaint-optimized? TODO
let set_level = (level) => {
    e = elements[index];
    word = e.innerHTML;
    offset = 0;
    for (i = 0; i < max; i++){
        if (elements[i].innerHTML == word){
            elements[i].className = "level-" + level;
            if (i < index){
                offset++;
            }
        }
    }
    api_add_word(word, level);
    if(level == 5){
        hide_border(e);
        re_query_elements(offset);
        show_border(elements[index]);
        show_definition(elements[index]);
    }
    else
        next();
    update_header();
}

let update_header = () => {
    let unknown_count = document.querySelectorAll(".level-0").length;
    header = "Total words: " + token_count + " / ";
    header += "Unknown (Blue) words: " + Math.ceil((unknown_count / token_count ) * 100) + "%"
    document.getElementById("header").innerHTML = header;
}

let on_page_loaded = () => {
    // setting variables
    index = 0; // (in case of file change)
    textview = document.getElementById("reader")
    re_query_elements(0);
    height = window.innerHeight
        || document.documentElement.clientHeight
        || document.body.clientHeight;

    token_count = document.getElementById("token_count").innerHTML;

    show_border(elements[index]);
    show_definition(elements[index]);
    update_header();


    // Event Handlers
    Mousetrap.bind('k', next);
    Mousetrap.bind('j', prev);
    Mousetrap.bind('l', scroll_to);
    Mousetrap.bind('q', () => {set_level(1)});
    Mousetrap.bind('s', () => {set_level(2)});
    Mousetrap.bind('d', () => {set_level(3)});
    Mousetrap.bind('f', () => {set_level(4)});
    Mousetrap.bind('g', () => {set_level(5)});
    document.getElementById("header_button")
        .addEventListener("click", load_file, false);
    document.getElementById("file_choose")
        .addEventListener('change', read_file, false);
}
