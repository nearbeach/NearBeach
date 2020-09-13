/**
 * Created by luke on 2/07/17.
 */
function update_filter() {
    //Varibales used in the function
    var input,
        filter,
        tr,
        i;

    //Get the value from the search box
    input = document.getElementById("filter_tables");

    //We want to compare apples with apples, make all uppercase
    filter = input.value.toUpperCase();

    //Get all table rows
    tr = document.getElementsByTagName("tr");

    for (i = 0; i < tr.length; i++) {
        //If the <tr> contains any values of the filter OR has class header, we want to show
        if (tr[i].innerHTML.toUpperCase().indexOf(filter) > -1 || tr[i].className=="header") {
            tr[i].style.display = "";
        } else {
            tr[i].style.display = "none";
        }
    }
}