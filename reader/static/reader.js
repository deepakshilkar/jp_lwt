var index = 0; // current thing
var max = 12; // number of morphenes
var textview; // DOM node
var elements; // all spans array
var height;




// Hide border arround current morphene
let hide_border = (e) => {
    e.style.borderStyle = "none";
}

// Show border arround current morphene
let show_border = (e) => {
    e.style.borderStyle = "solid";
}

// Switch to next non-known morphene
let next = () => {
    hide_border(elements[index]);
    index < max - 1? index++ : index;
    show_border(elements[index]);
}

// Switch to previous non-known morphene
let prev = () => {
    hide_border(elements[index]);
    index > 0 ? index-- : index;
    show_border(elements[index]);
}

// Scroll to / Center the current morphene
let scroll_to = () => {
    var position = elements[index].offsetTop;
    window.scrollTo(0, position - height/2);
}

// Since "knowing" a word makes you need to skip things, you need to recount the number of elements, especially the max and current id
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
    }
    else
        next();
}

let on_page_loaded = () => {
    // setting variables
    textview = document.getElementById("reader")
    re_query_elements(0);
    height = window.innerHeight
        || document.documentElement.clientHeight
        || document.body.clientHeight;

    show_border(elements[index]);

    Mousetrap.bind('k', next);
    Mousetrap.bind('j', prev);
    Mousetrap.bind('l', scroll_to);
    Mousetrap.bind('q', function() {set_level(0)});
    Mousetrap.bind('s', function() {set_level(2)});
    Mousetrap.bind('d', function() {set_level(3)});
    Mousetrap.bind('f', function() {set_level(4)});
    Mousetrap.bind('a', function() {set_level(5)});
}
