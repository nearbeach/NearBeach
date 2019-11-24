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