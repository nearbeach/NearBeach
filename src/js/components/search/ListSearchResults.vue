<template>
    <div class="card search-card">
        <div class="card-body">
            <h2>{{importVariables['header']}} Search Results</h2>
            <hr>

            <!-- TABLE OF DATA -->
            <table class="table">
                <thead>
                    <tr>
                        <td width="75%">{{importVariables['header']}}</td>
                        <td width="25%">Status</td>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="result in searchResults">
                        <td>
                            <!-- LINK -->
                            <a v-bind:href="`/${destination}_information/${result[importVariables['id']]}/`">
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
        </div>
    </div>
</template>

<script>
    export default {
        name: "ListSearchResults",
        props: {
            destination: String,
            importVariables: Object,  // {header, prefix,id, title, status}
            searchResults: Array,
        }
    }
</script>

<style scoped>

</style>