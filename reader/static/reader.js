let on_page_loaded = () => {
    element = document.body.querySelector("span:not(.level-5)");
    element.className += " curr"
}
