function on_page_load() {
    /* When the page loads, I want it to automatically disable ALL but the first option
     * for the regions. That way no one can do the sneaky and select an OPTION then a
     * country that does not contain that region... sneaky robots
     */
    var campus_region_select = document.getElementById("campus_region_id").getElementsByTagName("option");

    for (var i=1; i<campus_region_select.length; i++) {
        campus_region_select[i].disabled = true;
    }
}

function country_changed() {

}