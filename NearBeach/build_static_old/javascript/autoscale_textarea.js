function autoscale_textarea() {
    /*
    This function is designed to autoscale all areas that contain textarea tags.

    Method
    ~~~~~~
    1.) Define the div_sub_content that need scaling in an array
    2.) Loop through array
    3.) Find all textarea contained in that div_content
    4.) Resize to the scroll height + 12px
    5.) End Loop
    6.) If required, hide the div_content
    7.) End Loop

    Notes
    ~~~~~
    Not ALL areas require their textarea to be resized.
     */
    //[div_content_id,hide_after_applying]
    var div_content = [
        ['div_project_history',true],
        ['task_history',true],
        ['div_contact_history',false],
        ['div_organisation_contact',false]
    ];
    for (j=0; j<div_content.length; j++) {
        var div_content_object=document.getElementById(div_content[j][0]); //Has to be plural elements as there could be none
        //If div_content_object does not exist, do not do anything
        if (div_content_object) {
            var all_textareas=div_content_object.getElementsByTagName("textarea");
            for (i=0; i<all_textareas.length; i++) {
                //Default height of 12px
                all_textareas[i].style.height="12px";

                if (all_textareas[i].rows*7<=all_textareas[i].scrollHeight) {
                    all_textareas[i].style.height=all_textareas[i].scrollHeight+12+"px";
                }
            }
            //Only hide the object if true
            if (div_content[j][1]) {
                div_content_object.style = "display: none;";
            }
        }
    }
}