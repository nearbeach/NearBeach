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
function assigned_user_delete(user_id) {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        url: '/assigned_user_delete/' + user_id + '/',
        data: {},
        datatype: 'HTML',
        type: 'POST',
        success: function(data) {
            //Reload assigned users
            load_assigned_user_list();
            load_assigned_user_add();
        },
        error: function() {
            alert("Sorry, but deleting the assigned user did not work");
        }
    })
}
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


function add_bug(location_id, destination,bug_id, bug_client_id) {
    //Send data to the database
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $("#id_"+bug_id+"_"+bug_client_id).html("Adding...");


    $.ajax({
        url: '/bug_add/' + location_id + '/' + destination + '/' + bug_id + '/' + bug_client_id + '/',
        data: {},
        type: 'POST',
        success: function(data) {
            //$(this).html("Added");
            load_bug_list();
            $("#id_"+bug_id+"_"+bug_client_id).html("Added");
        },
        error: function() {
            alert("We are sorry, we experienced an error trying to add your bug to the " + destination);
        },
    });
}
function enable_disable_add_customer() {
	/* Method
	 * ~~~~~~
	 * Find out if the select value is "-------", if it is then we
	 * need to disable the add campus button. If not, we need to 
	 * re-enable it again.
	 */
	var id_add_customer_select = document.getElementById("id_add_customer_select");
	var id_add_customer_submit = document.getElementById("id_add_customer_submit");

	if (id_add_customer_select.selectedIndex==0) {
		id_add_customer_submit.disabled = true;
	} else {
		id_add_customer_submit.disabled = false;
	}
}



/*
The following javascript is to fix a bug where the map only renders on the right side
of the screen. The javascript changes the position to relative. Which fixes this issue.
 */
function relayout_map() {
    //alert("WHY DO I NEED TO ADD AN ALERT?")
    var mapbox = document.getElementById("map");
    var mapbox_canvas = mapbox.getElementsByClassName("mapboxgl-canvas");

    for (var i=0; i < mapbox_canvas.length; i++) {
        mapbox_canvas[i].style.position="relative";
    }
}

function check_end_date() {
	/* Method
	 * ~~~~~~
	 * 1.) Obtain all element values
	 * 2.) Check to see if the date is actually a date
	 * 3.) (not programmed yet) Edit the day element by removing any days
	 * that are not associated with the choosen month.
	 */
	var year_element = document.getElementById("id_finish_date_year");
	var month_element = document.getElementById("id_finish_date_month");
	var day_element = document.getElementById("id_finish_date_day");
	
	fix_dates(year_element, month_element, day_element);
}


function check_start_date() {
	/* Method
	 * ~~~~~~
	 * 1.) Obtain all element values
	 * 2.) Check to see if the date is actually a date
	 * 3.) (not programmed yet) Edit the day element by removing any days
	 * that are not associated with the choosen month.
	 */
	var year_element = document.getElementById("id_start_date_year");
	var month_element = document.getElementById("id_start_date_month");
	var day_element = document.getElementById("id_start_date_day");

	fix_dates(year_element, month_element, day_element);
}


function fix_dates(year_element, month_element, day_element) {
	/* First we check Feb.
	 * 
	 * Method
	 * ~~~~~~
	 * 1.) Check to see if the year is a leap year using the following;
	 * -- default = 28
	 * -- year / 4.0 = year / 4 = 29
	 * -- year / 100.0 = year / 100 = 28
	 * -- year / 1000.0 = year / 1000 = 29
	 * 2.) If date_element.value > max_days, change value to max_days
	 */
	 if (month_element.value == 2) {
		max_day = 28;
		
		//Hide/Unhide the unrequired dates
		day_element[28].hidden = true; //29th
		day_element[29].hidden = true; //30th
		day_element[30].hidden = true; //31th
		
		// If the year can be divided by 4 cleanly, it is a leap year
		if (parseInt(year_element.value/4) == parseInt(year_element.value)/4.0) {
			max_day = 29;
			day_element[28].hidden = false; //29th
		}
		
		// Exception is on the centruary year, is not a leap year
		if (parseInt(year_element.value/100) == parseInt(year_element.value)/100.0) {
			max_day = 28;
		}
		
		// Unless it falls on a millenium year
		if (parseInt(year_element.value/1000) == parseInt(year_element.value)/1000.0) {
			max_day = 29;
			day_element[28].hidden = false; //29th
		}
		
		// nwo check to see if the day value exceeds the max value
		if (day_element.value > max_day) {
			day_element.value = max_day;
		}


	/* else if the months are;
	 * April - 4th month
	 * June - 6th month
	 * September - 9th month
	 * November - 11th month
	 * Then only 30 days
	 */		
	} else if ((month_element.value == 4) ||
		(month_element.value == 6) ||
		(month_element.value == 9) ||
		(month_element.value == 11)) {
		if (day_element.value > 30) {
				day_element.value = 30;
			}
		
		//Hide/Unhide the unrequired dates
		day_element[28].hidden = false; //29th
		day_element[29].hidden = false; //30th
		day_element[30].hidden = true; //31th
	} else {
		//The rest of the months have 31 days
		//Hide/Unhide the unrequired dates
		day_element[28].hidden = false; //29th
		day_element[29].hidden = false; //30th
		day_element[30].hidden = false; //31th
	}	
} 


function initiate_dates() {
	check_start_date();
	check_end_date();
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

// using jQuery to extract the CSRFToken
function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
var csrftoken = getCookie('csrftoken');


function ajax_prepare() {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
}
function enable_disable_add_campus() {
	/* Method
	 * ~~~~~~
	 * Find out if the select value is "-------", if it is then we
	 * need to disable the add campus button. If not, we need to 
	 * re-enable it again.
	 */
	var id_add_cammpus_select = document.getElementById("id_add_cammpus_select");
	var id_add_cammpus_submit = document.getElementById("id_add_cammpus_submit");
	
	if (id_add_cammpus_select.selectedIndex==0) {
		id_add_cammpus_submit.disabled = true;
	} else {
		id_add_cammpus_submit.disabled = false;
	}
}

function confirm_delete_document(document_key,location_id,destination,folder_id) {
    //bring up modal
    //wait 2 seconds
    //enable button

    $("#confirm_document_delete").modal("show");

    //$(this).find('.btn-ok').attr('href', $(e.relatedTarget).data('href'));
    if ((folder_id == null) || (folder_id == 0)) {
        $("#remove_document_confirmed").attr('onclick','delete_document("' + document_key + '","' + location_id + '","' + destination + '")');
    } else {
        $("#remove_document_confirmed").attr('onclick','delete_document("' + document_key + '","' + location_id + '","' + destination + '","' + folder_id + '")');
    }


    setTimeout(function () {
        document.getElementById("remove_document_confirmed").disabled = false;
    }, 2000);
}


function confirm_delete_folder(folder_id,location_id,destination,current_folder_id) {
    //Show the modal - confirm that the user wants to delete the folder
    $("#confirm_folder_delete").modal("show");

    //We need to pass on the information of where to go when the delete button is clicked
    if ((current_folder_id == null) || (current_folder_id == 0)) {
        $("#remove_folder_confirmed").attr('onclick','delete_folder(' + folder_id + ',' + location_id + ',"' + destination + '")');
    } else {
        $("#remove_folder_confirmed").attr('onclick','delete_folder(' + folder_id + ',' + location_id + ',"' + destination + '",' + current_folder_id + ')');
    }

    //We want to make sure the delete button is disabled for 2 seconds
    setTimeout(function () {
        document.getElementById("remove_folder_confirmed").disabled = false;
    }, 2000);
}


function delete_document(document_key,location_id,destination,folder_id) {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        url: '/delete_document/' + document_key + '/',
        data: {},
        dataType: "HTML",
        type: "POST",
        success: function(data) {
            $("#confirm_document_delete").modal("hide"); //Remove the modal
            if ((folder_id == null) || (folder_id == 0)) {
                load_document_tree_list(location_id, destination);
            } else {
                load_document_tree_list(location_id, destination, folder_id);
            }
        },
        error: function() {
            alert("Sorry, there was an issue deletng the file");
        }

    })
}


function delete_folder(folder_id,location_id,destination,current_folder_id) {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        url: '/delete_folder/' + folder_id + '/',
        data: {},
        dataType: "HTML",
        type: "POST",
        success: function(data) {
            $("#confirm_folder_delete").modal("hide"); //Remove the modal
            if ((current_folder_id == null) || (current_folder_id == 0)) {
                load_document_tree_list(location_id, destination);
            } else {
                load_document_tree_list(location_id, destination, current_folder_id);
            }
        },
        error: function() {
            alert("Sorry - could not remove folder");
        }

    })
}


function load_document_tree_list(location_id, destination, folder_id) {
    /*
    The URL changes depending on the folder_id. If the folder_id is defined then we want to include it -
    otherwise we do not.
     */
    if (folder_id == null) {
        var url = '/document_tree_list/' + location_id + '/' + destination + '/';
    } else {
        var url = '/document_tree_list/' + location_id + '/' + destination + '/' + folder_id + '/';
    }
    //Load Project History
    $.ajax({
        url: url,
        data: {},
        dataType: 'HTML',
        type: 'GET',
        success: function(data) {
            $('#document_tree_list').html(data);
        },
        error: function() {
            $('#document_tree_list').html('<h2>Document Tree</h2>Sorry, document tree encounted an error and did not load.');
        }
    });
};


function new_folder(location_id,destination,folder_id) {
    //Send data to the database
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    //Get form data
    var form_data = new FormData($('#new_folder_form')[0]);

    $.ajax({
        url: '/document_tree_folder/' + location_id + '/' + destination + '/' + folder_id + '/',
        data: form_data,
        processData: false,
        contentType: false,
        type: 'POST',
        success: function(data) {
            $("#new_folder_modal").modal("hide"); //Remove the modal
            if ((folder_id == null) || (folder_id == 0)) {
                load_document_tree_list(location_id, destination);
            } else {
                load_document_tree_list(location_id, destination, folder_id);
            }
        },
        error: function() {
            $("#new_folder_modal").modal("hide"); //Remove the modal
            alert("Sorry, there was an error uploading the document");
        }
    });
}

function new_whiteboard(location_id,destination,folder_id) {
    //Send data to the database
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    //Get form data
    var form_data = new FormData($('#new_whiteboard_form')[0]);

    //Send data
    $.ajax({
        url: '/new_whiteboard/' + location_id + '/' + destination + '/' + folder_id + '/',
        data: form_data,
        processData: false,
        contentType: false,
        type: 'POST',
        success: function(data) {
            $("#new_whiteboard_modal").modal("hide"); //Remove the modal

            //Have to reload this component
            console.log("Data: ",data);
        },
        error: function() {
            $("#new_whiteboard_modal").modal("hide"); //Remove the modal
            alert("Sorry, there was an error uploading the document");
        }
    });
}


function upload_document(location_id,destination,folder_id) {
    //Send data to the database
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });


    //Get form data
    var form_data = new FormData($('#document_upload_form')[0]);

    $.ajax({
        xhr: function() {
            var xhr = new window.XMLHttpRequest();

            // Upload progress
            xhr.upload.addEventListener("progress", function(evt){
                if (evt.lengthComputable) {
                    var percentComplete = evt.loaded / evt.total;
                    //Do something with upload progress
                    $("#document_upload_progress").css(
                        'width', percentComplete * 100 + '%'
                    );
                }
           }, false);
           return xhr;
        },

        url: '/document_tree_upload/' + location_id + '/' + destination + '/' + folder_id + '/',
        data: form_data,
        processData: false,
        contentType: false,
        type: 'POST',
        success: function(data) {
            $("#document_upload_modal").modal("hide"); //Remove the modal
            $("#document_upload_progress").css('width','0%;');
            if ((folder_id == null) || (folder_id == 0)) {
                load_document_tree_list(location_id, destination);
            } else {
                load_document_tree_list(location_id, destination, folder_id);
            }
        },
        error: function() {
            $("#document_upload_modal").modal("hide"); //Remove the modal
            alert("Sorry, there was an error uploading the document");
        }
    });
}


function upload_url(location_id, destination, folder_id) {
    //Send data to the database
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    //Get form data
    var form_data = new FormData($('#document_url_form')[0]);

    $.ajax({
        url: '/document_tree_url/' + location_id + '/' + destination + '/' + folder_id + '/',
        data: form_data,
        processData: false,
        contentType: false,
        type: 'POST',
        success: function(data) {
            $("#new_url_modal").modal("hide"); //Remove the modal
            if ((folder_id == null) || (folder_id == 0)) {
                load_document_tree_list(location_id, destination);
            } else {
                load_document_tree_list(location_id, destination, folder_id);
            }
        },
        error: function() {
            $("#document_upload_modal").modal("hide"); //Remove the modal
            alert("Sorry, there was an error uploading the document");
        }
    });


}


/*
The following code should be inputted into the object you wish to add document list to.

<h2>Document Uploads</h2>
<div class="document_tree_list" id="document_tree_list">
    <h2>Document Tree List</h2>
    Loading...
</div>
 */

function hide_unhide(object_name) {
    var object = document.getElementById(object_name);

    if (object.style.display == "none") {
        object.style.display = "block";
    } else {
        object.style.display = "none";
    }
}
var map;
function initMap(latitude,longitude,title,api_key) {
    var location = {lat: latitude, lng: longitude};
    map = new google.maps.Map(document.getElementById('map'), {
    center:location,
    zoom: 13
    });

    var marker = new google.maps.Marker({
        position: location,
        map: map,
    })
}


/*
The following script will be used to interact with the error modal.
 */

function new_error(error_string) {
    //Show the modal
    $("#error_modal").modal({
        show: true,
        keyboard: true,
        focus: true,
    });

    //Add the error to the current modal
    $("#error_modal_body").append(`<hr>${error_string}`);
}
function initMap(latitude,longitude,title,api_key) {
    mapboxgl.accessToken  = api_key;
    var map = new mapboxgl.Map({
        container: 'map', // container id
        style: 'mapbox://styles/mapbox/streets-v9', // stylesheet location
        //center: [latitude,longitude], // starting position [lng, lat]
        center: [longitude,latitude],
        zoom: 15, // starting zoom
    });
    map.on('load', function() {
        map.addLayer({
            "id": "points",
            "type": "symbol",
            "source": {
                "type": "geojson",
                "data": {
                    "type": "FeatureCollection",
                    "features": [{
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            //"coordinates": [latitude,longitude]
                            "coordinates": [longitude,latitude]
                        },
                        "properties": {
                            "title": title,
                            "icon": "marker"
                        }
                    }]
                }
            },
            "layout": {
                "icon-image": "{icon}-15",
                "text-field": "{title}",
                "text-font": ["Open Sans Semibold", "Arial Unicode MS Bold"],
                "text-offset": [0, 0.6],
                "text-anchor": "top"
            }
        })

    });

    map['scrollZoom'].disable();

    $(window).bind('mousewheel DOMMouseScroll', function(event)
    {
        if(event.ctrlKey == true) {
            map['scrollZoom'].enable();
        }
        else {
            map['scrollZoom'].disable();
        }
    });

    //Quickly, relayout the map before anyone knows
    //relayout_map();
    setTimeout(relayout_map, 500);
}


/**
 * Created by luke on 11/07/17.
 */
function update_customers() {
    /*
    Issue
    ~~~~~
    We do not want the user to pick an organisation and then a customer from a different organisation. This function
    will limit which customer are seen in the "Customer" field to those only belonging to that particular organisation.
    This will work similarly to the Country/Region javascript.

    Method
    ~~~~~~
    1.) Extract out the Organisation ID from the organisation field
    2.) Loop through the customer fields and hide those who are not associated to the organisation
     */
    var organisations_id = document.getElementById('id_organisation_id').value;
    var customer_id = document.getElementById('customer_id');

    // Set customer id to ------
    customer_id.selectedIndex=0;

    /*
    Hide those values we do not want to see anymore
     */
    for (var i=1; i<customer_id.length; i++) {
        var customer_org_id = customer_id[i].getAttribute("organisation_id");
        if (customer_org_id == organisations_id) {
            customer_id[i].disabled=false;
        } else {
            customer_id[i].disabled=true;
        }
    }
}

function probability_update() {
    /*
    Issue
    ~~~~~
    Extract the probability from the dropdown box and update it in the % input

    Method
    ~~~~~~
    1.) Connect the varables to the required fields
    2.) Extract the probability value from the dropdown box
    3.) Apply it to the % input
     */
    var opportuniy_stage = document.getElementById("opportunity_stage");
    var success_probability = document.getElementById("id_opportunity_success_probability");

    success_probability.value = opportuniy_stage[opportuniy_stage.selectedIndex].getAttribute("probability");

}


function apply_organisation_customer(organisation, customer) {
    /*
    After the page loads, we will need to apply the organisation and
    if relivant the customer.
     */
    if (organisation!=null) {
        //Apply the organisation
        var select_field=document.getElementById("id_organisation_id");
        for (i=0;i<select_field.length;i++) {
            if (select_field[i].value==organisation) {
                select_field[i].selected=true;
            }
        }
    }
    if (customer!=null) {
        //Apply the customer
        var select_field=document.getElementById("customer_id");
        for (i=0;i<select_field.length;i++) {
            if (select_field[i].value==customer) {
                select_field[i].selected=true;
            }
        }
    }
}


function grant_access_checkbox(checkbox_id,div_id) {
    /*
    After the user has ticked the checkbox, we will try and find the
    checkbox the user has ticked and determine if we want to hide
    or show the div with the content.
     */
}

function select_groups(select) {
    /*
    Method
    ~~~~~~
    1.) Obtain the text for the current selection
    2.) Look at the <ul id="select_groups_ul">...</ul> and determine if the text is already present
    3.) If text is not present, add on another <li>
     */
    alert("Start");

    var select_value = select.value;
    var dataset = document.getElementById("select_groups_datalist");
    //alert(option);
    alert("Finish");

}

void function add_https() {
    /*
    When the user clicks on the organisation's website field, we want to add
    https:// at the start automatically. This is so that the customer does not
    need to enter in this required string. We only need to do this when there
    is nothing in the field
     */

}

void function paste_url() {
    /*
    When the user pastes a URL we want to double check it so that it will pass
    the validation of the form.
     */

}
function enable_disable_add_customer() {
	/* Method
	 * ~~~~~~
	 * Find out if the select value is "-------", if it is then we
	 * need to disable the add campus button. If not, we need to
	 * re-enable it again.
	 */
	var add_customer_select = document.getElementById("add_customer_select");
	var add_customer_submit = document.getElementById("add_customer_submit");

	if (add_customer_select.selectedIndex==0) {
		add_customer_submit.disabled = true;
	} else {
		add_customer_submit.disabled = false;
	}
}

function enable_disable_add_user() {
	/* Method
	 * ~~~~~~
	 * Find out if the select value is "-------", if it is then we
	 * need to disable the add campus button. If not, we need to
	 * re-enable it again.
	 */
	var add_user_select = document.getElementById("add_user_select");
	var add_user_submit = document.getElementById("add_user_submit");

	if (add_user_select.selectedIndex==0) {
		add_user_submit.disabled = true;
	} else {
		add_user_submit.disabled = false;
	}
}


function enable_disable_add_cost() {
	var cost_description = document.getElementById("id_cost_description");
	var cost_amount = document.getElementById("id_cost_amount");
	var add_cost_submit = document.getElementById("add_cost_submit");

	if ((cost_description.value != '') && (cost_amount.value != '') &&
		((cost_amount.value >= 0) || (cost_amount.value <= 0)) //Work around for if it is a number.
		) {
		add_cost_submit.disabled = false;
	} else {
		add_cost_submit.disabled = true;
	}
}

function render_bug_client_bugs(data, target_id) {
    /*
    Render bug client bugs will render a simple stacked BAR CHART detailing the different stages of bugs on each of
    the different clients.

    Method
    ~~~~~~
    1. Get a unique list of the different bug status
    1. Create a simple array
    2. Create the required graphs :)
     */

    /*
    We will require to get a list of unique bug status. To do this we will first loop through ALL of the different
    bug client results and compile a unique list
     */
    var list_of_bug_status = {};
    for (row in data) {
        //Simplify the code
        var client = data[row],
            bug_status = client["bug_status"];

        //Loop through the bug status'
        for (status in bug_status) {
            //If it exists, it will only make it exist more.
            list_of_bug_status[status] = status;
        }
    }

    //Sort the bug status
    list_of_bug_status = Object.keys(list_of_bug_status).sort(function(a,b){
        return list_of_bug_status[a] - list_of_bug_status[b];
    });

    console.log("Unique bug status: ", list_of_bug_status);

    //Loop through the each bug client, and determine the value of each bug type
    var converted_data = [];
    for (row in data) {
        //Simplify the code
        var client = data[row],
            bug_status = client["bug_status"],
            basic_object = { 'bug_client_name': row };

        //Loop through the unique bug status'
        list_of_bug_status.forEach(function(status) {
            //If the count of the bug client exists, record it.
            //If not - simply put a 0
            if (bug_status[status] == undefined) {
                //We want this field to be a 0 instead of undefinded
                basic_object[status] = 0;
            } else {
                //We want the count of the object.
                basic_object[status] = bug_status[status];
            }
        });

        //Write results to the convered_data
        converted_data.push(basic_object);
    }

    //TEMP VARIABLES//
    var margin = {top: 40, right: 100, bottom: 80, left: 50},
        width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;
    //END TEMP VARIABLES//

    console.log("Converted Data: ", converted_data); //The data is now ready :)

    //Setup the x and y range
    var x = d3.scaleBand()
        .rangeRound([0, width], 0.15)
        .paddingInner(0.2)
        .paddingOuter(0.2);

    //Please note y is scale LINEAR!
    var y = d3.scaleLinear()
        .range([height, 0]);

    //Get colour ready
    var color = d3.scaleOrdinal(d3.schemePastel2);

    //Get axis ready
    var xAxis = d3.axisBottom()
        .scale(x);
    var yAxis = d3.axisLeft()
        .scale(y)
        .ticks(10);


    //Prepare the output location
    var output_location = document.getElementById(target_id);
    output_location.innerHTML = "";

    //Create the svg
    var svg = d3.select(output_location).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .attr("data-graph",output_location.id)
        .attr("class", "graph_body")
        .append("g")
        .attr("transform","translate(" + margin.left + "," + margin.top + ")");

    //Assign the colour
    color.domain(
        d3.keys(converted_data[0])
            .filter(function(key) {
                return key !== "bug_client_name";
            })
    );

    //Apply changes to the convert_data - will get it ready for the stacked graph
    converted_data.forEach(function(d) {
        var y0 = 0;
        d.operation = color.domain().map(
            function(name) {
                return {name: name, y0: y0, y1: y0 += +d[name]};
            });
        d.count = d.operation[d.operation.length - 1].y1;
        if (d.count == NaN) { d.count = 0; }
    });

    console.log("Converted data after colours: ", converted_data);

    //Set the x domain
    x.domain(
        converted_data.map(function(d) {
            return d["bug_client_name"];
        })
    );

    //Set the y domain
    y.domain([
        0,
        d3.max(converted_data, function(d) {
            return d.count; })
    ]);

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Count");

    var stack = svg.selectAll(".location")
        .data(converted_data)
        .enter().append("g")
        .attr("class", "g")
        .attr("transform", function(d) { return "translate(" + x(d["bug_client_name"]) + ",0)"; });

    stack.selectAll("rect")
        .data(function(d) { return d.operation; })
        .enter().append("rect")
        .attr("width", x.bandwidth())
        .attr("y", function(d) { return y(d.y1); })
        .attr("height", function(d) { return y(d.y0) - y(d.y1); })
        .attr("data-value", function(d) { return d.y1-d.y0; }) //The difference between the the values
        .style("fill", function(d) { return color(d.name); });

    var legend = svg.selectAll(".legend")
        .data(color.domain().slice().reverse())
        .enter().append("g")
        .attr("class", "legend")
        .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

    legend.append("rect")
        .attr("x", width + 48)
        .attr("width", 18)
        .attr("height", 18)
        .style("fill", color);

    legend.append("text")
        .attr("x", width + 48)
        .attr("y", 9)
        .attr("dy", ".35em")
        .style("text-anchor", "end")
        .text(function(d) { return d; });

    svg.append("text")
        .attr("x", (width / 2))
        .attr("y", 0 - (margin.top / 2))
        .attr("text-anchor", "middle")
        .style("font-size", "16px")
        .style("text-decoration", "underline")
        .text("Bug Client Breakdown");


    //X-axis label
    svg.append("text")
        .attr(
            "transform",
            "translate(" + (width/2) + " ," + (height + margin.top + 20) + ")"
        )
        .style("text-anchor", "middle")
        .text("Bug Client Name");

    //Y-axis label
    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left)
        .attr("x",0 - (height / 2))
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .text("Count of Bugs");
}
function render_folders(document_folders_results, current_folder) {
	/*
	Render folder function renders each folder. It is a recursive function.
	Each folder it will render it will give an id of the folder number with
	the suffix _folder
	i.e 1_folder

	Step 1
	~~~~~~
	We currently only want the folder for the current location.
	 */
	var folder_results = document_folders_results.filter(function(i, n) {
		return (i.fields.parent_folder_id == current_folder);
	});
	/*
	Step 2
	~~~~~~
	We will loop through each of the folder resules. Make sure that there are
	no sub folder. If there are any sub folder we will call this function
	recursovly with the sub folder information.
	 */
	var content_string = '';
	for (var i=0; i<folder_results.length; i++) {
		content_string += '<li><label>' + folder_results[i].fields.folder_description + '</label>';
		content_string += '<input type="checkbox" id="' + folder_results[i].pk + '_checkbox">';
		content_string += '<ul id="' + folder_results[i].pk + '_folder">';
		content_string += render_folders(document_folders_results, folder_results[i].pk);
		content_string += '</ul></li>';

		/*
		Minor step
		~~~~~~~~~~
		We are now adding the folder to the new_document_location select
		*/
		var new_document_location = document.getElementById("parent_folder_id");
		var folder_location = document.getElementById("folder_location");
		var opt = document.createElement('option');
		opt.value = folder_results[i].pk;
		opt.innerHTML = folder_results[i].fields.folder_description;
		new_document_location.appendChild(opt);
		//folder_location.appendChild(opt);

		//Ok, I am cheating here.
		//Bug with JAVASCRIPT - will now allow me to append the same opt twice.
		var folder_location = document.getElementById("folder_location");
		var opt2 = document.createElement('option');
		opt2.value = folder_results[i].pk;
		opt2.innerHTML = folder_results[i].fields.folder_description;
		folder_location.appendChild(opt2);

	}
	return content_string;

}

function add_new_document() {
	new_document_dialog = document.getElementById("overlay_new_document");
	new_document_dialog.style.visibility = (new_document_dialog.style.visibility == "visible") ? "hidden" : "visible";
}

function add_new_folder() {
    new_folder_dialog = document.getElementById("overlay_new_folder");
    new_folder_dialog.style.visibility = (new_folder_dialog.style.visibility == "visible") ? "hidden" : "visible";
}

function render_documents(document_results, site_url) {
	for (var i=0; i<document_results.length; i++) {
		var content_string = '<a href="';
		if ((document_results[i][3] == '') || (document_results[i][3] == null)) {
            content_string += document_results[i][2];

        } else {
			content_string += site_url + document_results[i][3];
		}
		content_string += '" target="_blank">';
		content_string += document_results[i][1];
		content_string += '</a>';

		if ((document_results[i][4] == null) || (document_results[i][4] == "")) {
			destination_folder = document.getElementById("root_folder");
		} else {
			destination_folder = document.getElementById(document_results[i][4] + "_folder");
		}
		destination_folder.innerHTML = destination_folder.innerHTML + '<br/>' + content_string;

	}
}

function upload_or_link() {
    overlay_upload = document.getElementById("overlay_upload");
    overlay_link = document.getElementById("overlay_link");
    upload_type = document.getElementById("upload_type");


    if (upload_type.selectedIndex == 0) {
        overlay_upload.style.display = "block";
        overlay_link.style.display = "none";
    } else {
        overlay_upload.style.display = "none";
        overlay_link.style.display = "block";
    }

    //Check to make sure if submit needs to be enabled
    enable_submit()
}

function enable_submit() {
	/*
	So I didn't like the spaghetti if statements left here. So I invented this simple
	boolean way to disable and enable the submit button.

	It works by checking to see if there are values in the required fields. It will
	activate the button if either one of the two conditions is met. Simple.
	 */
	id_document = Boolean(document.getElementById("id_document").value != "");
	id_document_url_location = Boolean(document.getElementById("id_document_url_location").value != "");
	id_document_description = Boolean(document.getElementById("id_document_description").value != "");
	id_new_folder = Boolean(document.getElementById("id_folder_description").value == "");

	new_document = document.getElementById("new_document");
	new_folder = document.getElementById("new_folder");
	new_document.disabled = !Boolean((id_document && id_document_description) || (id_document_url_location && id_document_description));
	new_folder.disabled = id_new_folder;
}

function enable_disable_add_customer() {
	/* Method
	 * ~~~~~~
	 * Find out if the select value is "-------", if it is then we
	 * need to disable the add campus button. If not, we need to
	 * re-enable it again.
	 */
	var add_customer_select = document.getElementById("add_customer_select");
	var add_customer_submit = document.getElementById("add_customer_submit");

	if (add_customer_select.selectedIndex==0) {
		add_customer_submit.disabled = true;
	} else {
		add_customer_submit.disabled = false;
	}
}
function Search_Active_Projects() {
	//Varables used in the function
	var input, filter, table, tr, column_project, column_task, column_description, i;
	
	//Get the value from the search box
	input = document.getElementById("Search_Active_Projects");
	
	//We want to compare apples with apples, make all uppercase
	filter = input.value.toUpperCase();

	//Get reference to the table
	table = document.getElementById("Active_Projects_Table");

	//Separate the table into it's separate elements
	tr = table.getElementsByTagName("tr");

	//The loop will go through and check the filter against each value
	//Any row that does not contain the filter value it will hide
	//by using the display = 'none'
	for (i = 0; i < tr.length; i++) {
		column_project = tr[i].getElementsByTagName("td")[0];
		column_task = tr[i].getElementsByTagName("td")[1];
		column_description = tr[i].getElementsByTagName("td")[2];
		if (column_project || column_task || column_description) {
			if (column_project.innerHTML.toUpperCase().indexOf(filter) > -1 ||
				column_task.innerHTML.toUpperCase().indexOf(filter) > -1 ||
				column_description.innerHTML.toUpperCase().indexOf(filter) > -1	) {
				tr[i].style.display = "";
			} else {
				tr[i].style.display = "none";
			}
		}
	}
}


//Functions
function enable_disable_add_customer() {
	/* Method
	 * ~~~~~~
	 * Find out if the select value is "-------", if it is then we
	 * need to disable the add campus button. If not, we need to
	 * re-enable it again.
	 */
	var add_customer_select = document.getElementById("add_customer_select");
	var add_customer_submit = document.getElementById("add_customer_submit");

	if (add_customer_select.selectedIndex==0) {
		add_customer_submit.disabled = true;
	} else {
		add_customer_submit.disabled = false;
	}
}

function enable_disable_add_user() {
	/* Method
	 * ~~~~~~
	 * Find out if the select value is "-------", if it is then we
	 * need to disable the add campus button. If not, we need to
	 * re-enable it again.
	 */
	var add_user_select = document.getElementById("add_user_select");
	var add_user_submit = document.getElementById("add_user_submit");

	if (add_user_select.selectedIndex==0) {
		add_user_submit.disabled = true;
	} else {
		add_user_submit.disabled = false;
	}
}


function enable_disable_add_cost() {
	var cost_description = document.getElementById("id_cost_description");
	var cost_amount = document.getElementById("id_cost_amount");
	var add_cost_submit = document.getElementById("add_cost_submit");

	if ((cost_description.value != '') && (cost_amount.value != '')) {
		add_cost_submit.disabled = false;
	} else {
		add_cost_submit.disabled = true;
	}
}


function load_timesheet(location, destination) {
    $.ajax({
        url: `/timesheet/${ location }/${ destination }/`,
        data: {},
        dataType: 'HTML',
        type: 'GET',
        success: function(data) {
            //Insert the data
            $("#timesheet").html(data);

            //Initiate the data
            timesheet_setup();
        },
        error: function() {
            alert("Sorry, timesheet could not load");
        }
    })
}

function timesheet_setup() {
    /* This function will finish setting up the timesheet - i.e. setup the datetime functions*/
    $( "#id_timesheet_date" ).datetimepicker({
        scrollInput: false,
        format: "Y-m-d",
        timepicker:false,
    });


    $("#id_timesheet_start_time").datetimepicker({
        scrollInput: false,
        'scrollDefault': 'now',
        datepicker:false,
        format:'H:i',
        allowTimes: [
            '00:00','00:05','00:10','00:15','00:20','00:25','00:30','00:35','00:40','00:45','00:50','00:55',
            '01:00','01:05','01:10','01:15','01:20','01:25','01:30','01:35','01:40','01:45','01:50','01:55',
            '02:00','02:05','02:10','02:15','02:20','02:25','02:30','02:35','02:40','02:45','02:50','02:55',
            '03:00','03:05','03:10','03:15','03:20','03:25','03:30','03:35','03:40','03:45','03:50','03:55',
            '04:00','04:05','04:10','04:15','04:20','04:25','04:30','04:35','04:40','04:45','04:50','04:55',
            '05:00','05:05','05:10','05:15','05:20','05:25','05:30','05:35','05:40','05:45','05:50','05:55',
            '06:00','06:05','06:10','06:15','06:20','06:25','06:30','06:35','06:40','06:45','06:50','06:55',
            '07:00','07:05','07:10','07:15','07:20','07:25','07:30','07:35','07:40','07:45','07:50','07:55',
            '08:00','08:05','08:10','08:15','08:20','08:25','08:30','08:35','08:40','08:45','08:50','08:55',
            '09:00','09:05','09:10','09:15','09:20','09:25','09:30','09:35','09:40','09:45','09:50','09:55',
            '10:00','10:05','10:10','10:15','10:20','10:25','10:30','10:35','10:40','10:45','10:50','10:55',
            '11:00','11:05','11:10','11:15','11:20','11:25','11:30','11:35','11:40','11:45','11:50','11:55',
            '12:00','12:05','12:10','12:15','12:20','12:25','12:30','12:35','12:40','12:45','12:50','12:55',
            '13:00','13:05','13:10','13:15','13:20','13:25','13:30','13:35','13:40','13:45','13:50','13:55',
            '14:00','14:05','14:10','14:15','14:20','14:25','14:30','14:35','14:40','14:45','14:50','14:55',
            '15:00','15:05','15:10','15:15','15:20','15:25','15:30','15:35','15:40','15:45','15:50','15:55',
            '16:00','16:05','16:10','16:15','16:20','16:25','16:30','16:35','16:40','16:45','16:50','16:55',
            '17:00','17:05','17:10','17:15','17:20','17:25','17:30','17:35','17:40','17:45','17:50','17:55',
            '18:00','18:05','18:10','18:15','18:20','18:25','18:30','18:35','18:40','18:45','18:50','18:55',
            '19:00','19:05','19:10','19:15','19:20','19:25','19:30','19:35','19:40','19:45','19:50','19:55',
            '20:00','20:05','20:10','20:15','20:20','20:25','20:30','20:35','20:40','20:45','20:50','20:55',
            '21:00','21:05','21:10','21:15','21:20','21:25','21:30','21:35','21:40','21:45','21:50','21:55',
            '22:00','22:05','22:10','22:15','22:20','22:25','22:30','22:35','22:40','22:45','22:50','22:55',
            '23:00','23:05','23:10','23:15','23:20','23:25','23:30','23:35','23:40','23:45','23:50','23:55'
        ],
        defaultTime: '08:45',
        onSelectTime: function(){
            //Make sure the start time is not greater than the end time
            var start_time = $("#id_timesheet_start_time").val(),
                end_time = $("#id_timesheet_end_time").val();

            if (start_time > end_time) {
                $("#id_timesheet_end_time").val(start_time);
            }
        }
    });

    $("#id_timesheet_end_time").datetimepicker({
        scrollInput: false,
        'scrollDefault': 'now',
        datepicker:false,
        format:'H:i',
        allowTimes: [
            '00:00','00:05','00:10','00:15','00:20','00:25','00:30','00:35','00:40','00:45','00:50','00:55',
            '01:00','01:05','01:10','01:15','01:20','01:25','01:30','01:35','01:40','01:45','01:50','01:55',
            '02:00','02:05','02:10','02:15','02:20','02:25','02:30','02:35','02:40','02:45','02:50','02:55',
            '03:00','03:05','03:10','03:15','03:20','03:25','03:30','03:35','03:40','03:45','03:50','03:55',
            '04:00','04:05','04:10','04:15','04:20','04:25','04:30','04:35','04:40','04:45','04:50','04:55',
            '05:00','05:05','05:10','05:15','05:20','05:25','05:30','05:35','05:40','05:45','05:50','05:55',
            '06:00','06:05','06:10','06:15','06:20','06:25','06:30','06:35','06:40','06:45','06:50','06:55',
            '07:00','07:05','07:10','07:15','07:20','07:25','07:30','07:35','07:40','07:45','07:50','07:55',
            '08:00','08:05','08:10','08:15','08:20','08:25','08:30','08:35','08:40','08:45','08:50','08:55',
            '09:00','09:05','09:10','09:15','09:20','09:25','09:30','09:35','09:40','09:45','09:50','09:55',
            '10:00','10:05','10:10','10:15','10:20','10:25','10:30','10:35','10:40','10:45','10:50','10:55',
            '11:00','11:05','11:10','11:15','11:20','11:25','11:30','11:35','11:40','11:45','11:50','11:55',
            '12:00','12:05','12:10','12:15','12:20','12:25','12:30','12:35','12:40','12:45','12:50','12:55',
            '13:00','13:05','13:10','13:15','13:20','13:25','13:30','13:35','13:40','13:45','13:50','13:55',
            '14:00','14:05','14:10','14:15','14:20','14:25','14:30','14:35','14:40','14:45','14:50','14:55',
            '15:00','15:05','15:10','15:15','15:20','15:25','15:30','15:35','15:40','15:45','15:50','15:55',
            '16:00','16:05','16:10','16:15','16:20','16:25','16:30','16:35','16:40','16:45','16:50','16:55',
            '17:00','17:05','17:10','17:15','17:20','17:25','17:30','17:35','17:40','17:45','17:50','17:55',
            '18:00','18:05','18:10','18:15','18:20','18:25','18:30','18:35','18:40','18:45','18:50','18:55',
            '19:00','19:05','19:10','19:15','19:20','19:25','19:30','19:35','19:40','19:45','19:50','19:55',
            '20:00','20:05','20:10','20:15','20:20','20:25','20:30','20:35','20:40','20:45','20:50','20:55',
            '21:00','21:05','21:10','21:15','21:20','21:25','21:30','21:35','21:40','21:45','21:50','21:55',
            '22:00','22:05','22:10','22:15','22:20','22:25','22:30','22:35','22:40','22:45','22:50','22:55',
            '23:00','23:05','23:10','23:15','23:20','23:25','23:30','23:35','23:40','23:45','23:50','23:55'
        ],
        defaultTime: '17:00',
        onSelectTime: function(){
            //Make sure the start time is not greater than the end time
            var start_time = $("#id_timesheet_start_time").val(),
                end_time = $("#id_timesheet_end_time").val();

            if (start_time > end_time) {
                $("#id_timesheet_start_time").val(end_time);
            }
        }
    });

    //Set default dates
    $("#id_timesheet_start_time").val("08:45");
    $("#id_timesheet_end_time").val("17:00");
}