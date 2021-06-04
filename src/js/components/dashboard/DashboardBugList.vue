<template>
    <div class="card">
        <div class="card-body">
            <h2>Active Bugs</h2>
            <hr>

            <div id="active_bug_graph"></div>
        </div>
    </div>
</template>

<script>
    const axios = require('axios');
    import * as d3 from "d3";

    // Mixins
    import errorModalMixin from "../../mixins/errorModalMixin";

    export default {
        name: "DashboardBugList",
        props: {
            rootUrl: {
                type: String,
                default: "/",
            },
        },
        data() {
            return {
                bugResults: [],
            }
        },
        mixins: [
            errorModalMixin,
        ],
        methods: {
            getBugData: function() {
                axios.post(
                    `${this.rootUrl}dashboard/get/bug_list/`
                ).then(response => {
                    //Update Bug Response
                    this.bugResults = response['data'];

                    //Start rendering the graph
                    this.renderGraph();
                }).catch(error => {
                    this.showErrorModal(error, 'Dashboard Unassigned Objects');
                });
            },
            renderGraph: function() {
                //Declare size variables
                var margin = {top: 10, right: 30, bottom: 20, left: 50},
                    width = 460 - margin.left - margin.right,
                    height = 400 - margin.top - margin.bottom;

                //Clear the destination
                var outward_location = document.getElementById("active_bug_graph");
                outward_location.innerHTML = "";


                //Start Rendering SVG
                var svg = d3.select(outward_location)
                    .append('svg')
                    .attr('width',width + margin.left + margin.right)
                    .attr('height',height + margin.top + margin.bottom)
                    .attr("class", "graph_body")
                    .append('g')
                    .attr('id','active_bug_d3')
                    .attr("transform","translate(" + margin.left + "," + margin.top + ")");


                //Setup the x and y domain and range
                var x = d3.scaleBand()
                    .rangeRound([0, width], 0.15)
                    .paddingInner(0.2)
                    .paddingOuter(0.2);

                var y = d3.scaleLinear()
                    .range([height, 0]);


                //Get axis ready
                var xAxis = d3.axisBottom()
                    .scale(x);

                var yAxis = d3.axisLeft()
                    .scale(y)
                    .ticks(10);


                //Get colour ready
                var color = d3.scaleOrdinal(d3.schemePastel2);


                //Render the Elements
                svg.selectAll("#active_bug_d3")
                    .data(this.bugResults)
                    .enter()
                    .append("rect")
                    .attr("x",(d) => {
                        return 1;
                    })
                    .attr("y",(d) => {
                        console.log("Y: ",y(d['bug_status__count']))
                        return y(d['bug_status__count']);
                    })
                    .attr("height",(d) => {
                        return 50;
                    })
                    .attr("width","50")


                //Render the X-AXIS
                svg.append("g")
                    .attr("class", "x-axis")
                    .attr("transform", "translate(0," + height + ")")
                    .call(xAxis);

                //Render the Y-AXIS
                svg.append("g")
                    .attr("class", "y-axis")
                    .call(yAxis)
                    .append("text")
                    .attr("transform", "rotate(-90)")
                    .attr("y", 6)
                    .attr("dy", ".71em")
                    .style("text-anchor", "end")
                    .text("Count");
            }
        },
        mounted() {
            this.getBugData();
        }
    }
</script>

<style scoped>

</style>
