function hide_unhide(object_name) {
    var object = document.getElementById(object_name);

    if (object.style.display == "none") {
        object.style.display = "block";
    } else {
        object.style.display = "none";
    }
}