var i = 0; // current thing
var max = 12; // number of morphenes
var textview; // DOM node
var elements; // all spans array
var height;

let hide_border = (e) => {
    e.style.borderStyle = "none";
}

let show_border = (e) => {
    e.style.borderStyle = "solid";
}

let next = () => {
    hide_border(elements[i]);
    i < max - 1? i++ : i;
    show_border(elements[i]);
}

let prev = () => {
    hide_border(elements[i]);
    i > 0 ? i-- : i;
    show_border(elements[i]);
}


let scroll_to = () => {
    var position = elements[i].offsetTop;
    console.log(position);
    window.scrollTo(0, position - height/2);
}

let on_page_loaded = () => {
    textview = document.getElementById("reader")
    elements = textview.querySelectorAll("text-view span:not(.level-5)");
    max = elements.length;
    i = 200;
    show_border(elements[i]);
    height = window.innerHeight
        || document.documentElement.clientHeight
        || document.body.clientHeight;

    Mousetrap.bind('right', next);
    Mousetrap.bind('left', prev);
    Mousetrap.bind('x', scroll_to);
}
