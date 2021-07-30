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
                    {{result[importVariables['status']]}}
                </td>
            </tr>
        </tbody>
    </table>
</template>

<script>
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
        methods: {}
    }
</script>
