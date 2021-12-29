<template>
    <!-- TABLE OF DATA -->
    <table class="table">
        <thead>
            <tr>
                <td width="75%">{{importVariables['header']}}</td>
                <td width="25%">Status</td> 
            </tr>
        </thead>
        <tbody>
            <tr v-for="result in searchResults" :key="result['pk']">
                <td>
                    <!-- LINK -->
                    <a v-bind:href="`${rootUrl}${destination}_information/${result[importVariables['id']]}/`">
                        <p>{{result[importVariables['title']]}}</p>
                        <div class="spacer"></div>
                        <p class="small-text">
                            {{importVariables['prefix']}}{{result[importVariables['id']]}}
                        </p>
                    </a>
                </td>
                <td>
                    <!-- STATUS -->
                    <p>{{result[importVariables['status']]}}</p>
                    <div class="spacer"></div>
                    <p class="small-text">
                      {{formatDates(result[importVariables['end_date']])}}
                    </p>
                </td>
            </tr>
        </tbody>
    </table>
</template>

<script>
    const { DateTime } = require("luxon");

    export default {
        name: "RenderObjectTable",
        props: {
            destination: String,
            importVariables: Object,  // {header, prefix,id, title, status}
            rootUrl: {
                type: String,
                default: "/",
            },
            searchResults: Array,
        },
        data() {
            return {}
        },
        methods: {
            formatDates(date) {
                //Escape if date is undefined
                if (date === undefined) return "";

                //Convert the date from string to ISO standard
                let convert_date = DateTime.fromISO(date);
                return convert_date.toHTTP();
            }
        }
    }
</script>
